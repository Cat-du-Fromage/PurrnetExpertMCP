"""Extract C# declaration evidence from installed packages using Tree-sitter."""

import re
from pathlib import Path

import tree_sitter_c_sharp
from tree_sitter import Language, Parser

from .paths import read_file, walk

CSHARP = Language(tree_sitter_c_sharp.language())
TYPE_NODES = frozenset({
    "class_declaration", "struct_declaration", "interface_declaration",
    "record_declaration", "enum_declaration", "delegate_declaration",
})
MEMBER_NODES = frozenset({
    "method_declaration", "property_declaration", "event_declaration", "event_field_declaration",
})
MAX_RESULTS = 12


def symbol_parts(symbol: str) -> list[tuple[str, int | None]]:
    parts = []
    for part in symbol.strip().removeprefix("global::").split("."):
        match = re.fullmatch(r"([A-Za-z_]\w*)(?:<\s*([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*>)?", part)
        if not match:
            raise ValueError("Use a type or qualified member name, e.g. SyncVar<T> or NetworkManager.StartClient.")
        parts.append((match[1], match[2].count(",") + 1 if match[2] else None))
    return parts


def node_text(node) -> str:
    return node.text.decode("utf-8", errors="replace") if node else ""


def name_and_arity(node):
    parameters = next((child for child in node.named_children if child.type == "type_parameter_list"), None)
    return (
        node_text(node.child_by_field_name("name")),
        sum(child.type == "type_parameter" for child in parameters.named_children) if parameters else 0,
    )


def declarations(tree, parts):
    root = tree.root_node
    file_namespace = next((n for n in root.named_children if n.type == "file_scoped_namespace_declaration"), None)
    namespace = node_text(file_namespace.child_by_field_name("name")) if file_namespace else ""
    stack = [(root, namespace, (), False)]
    while stack:
        node, ns, parents, conditional = stack.pop()
        kind = node.type
        if kind == "namespace_declaration":
            name = node_text(node.child_by_field_name("name"))
            ns = ".".join(filter(None, (ns, name)))
        if kind.startswith("preproc_"):
            conditional = True
        if kind in TYPE_NODES or kind in MEMBER_NODES:
            names = [name_and_arity(node)]
            if kind == "event_field_declaration":
                names = [
                    name_and_arity(child)
                    for variable in node.named_children if variable.type == "variable_declaration"
                    for child in variable.named_children if child.type == "variable_declarator"
                ]
            for name in names:
                qualified = [(piece, 0) for piece in ns.split(".") if piece] + list(parents) + [name]
                tail = qualified[-len(parts):]
                if len(tail) == len(parts) and all(
                    expected == actual and (arity is None or arity == actual_arity)
                    for (expected, arity), (actual, actual_arity) in zip(parts, tail)
                ):
                    yield node, ns, parents, name, conditional
            if kind in TYPE_NODES:
                parents = (*parents, names[0])
            else:
                continue
        if kind in TYPE_NODES or kind in {"compilation_unit", "declaration_list", "namespace_declaration"} or kind.startswith("preproc_"):
            stack.extend((child, ns, parents, conditional) for child in reversed(node.named_children))


def declaration_evidence(blob, candidate, path, package):
    node, ns, parents, (name, arity), conditional = candidate
    kind = node.type.removesuffix("_declaration")
    children = node.named_children
    start = next((child for child in children if child.type not in {"attribute_list", "comment"}), node)
    body = next(
        (child for child in children if child.type in {"block", "arrow_expression_clause", "declaration_list", "enum_member_declaration_list"}),
        None,
    )
    end_byte = body.start_byte if body else node.end_byte
    end_row = body.start_point.row if body else node.end_point.row
    signature = blob[start.start_byte:end_byte].decode("utf-8", errors="replace").strip()
    attributes = [
        node_text(attribute.child_by_field_name("name")).split(".")[-1].removeprefix("global::")
        for child in children if child.type == "attribute_list"
        for attribute in child.named_children if attribute.type == "attribute"
    ]
    verified = bool(signature) and not node.has_error and not conditional and "#if" not in signature and len(signature) <= 1200
    type_names = [item[0] for item in parents]
    if node.type in TYPE_NODES:
        type_names.append(name)
    revision = package["lock_revision"]
    suffix = package["active_source"]["path"].rpartition("@")[2].lower()
    if package["active_source"]["origin"] != "cache" or not revision or not (
        re.fullmatch(r"[0-9a-f]{7,40}", suffix) and revision.startswith(suffix)
    ):
        revision = None
    return {
        "namespace": ns or None, "type": ".".join(type_names) or None, "name": name, "kind": kind,
        "generic_arity": arity, "signature": signature if verified else None,
        "fragment": signature[:1200], "confidence": "syntax_verified" if verified else "signature_unverified",
        "conditional": conditional, "obsolete_attribute": any(a in ("Obsolete", "ObsoleteAttribute") for a in attributes),
        "path": path, "line_start": start.start_point.row + 1, "line_end": end_row + 1,
        "package": package["package"], "package_version": package["version"],
        "version_source": package["version_source"], "package_revision": revision, "source": "installed_csharp",
    }


def lookup_installed(symbol: str, context: dict) -> dict:
    parts = symbol_parts(symbol)
    identifier = re.compile(rb"\b" + re.escape(parts[-1][0].encode("utf-8")) + rb"\b")
    root = Path(context["project"])
    parser = Parser(CSHARP)
    results = []
    fallback = []
    files = total_bytes = skipped = 0
    truncated = False
    packages = [context["purrnet"], context["purrdiction"], *context["associated_packages"]]
    roots = [(p, path) for p in packages if p for path in p["csharp_source_roots"]]
    seen = set()
    try:
        for package, relative in roots:
            for path in walk(root, root / relative, depth=16, budget=30_000, exclude=frozenset({".git"})):
                if path.suffix.lower() != ".cs" or path in seen:
                    continue
                seen.add(path)
                files += 1
                if files > 8000 or total_bytes > 40_000_000:
                    raise ValueError("C# scan budget reached")
                try:
                    blob = read_file(root, path, 1_500_000)
                except (OSError, ValueError):
                    skipped += 1
                    continue
                total_bytes += len(blob)
                match = identifier.search(blob)
                if not match:
                    continue
                tree = parser.parse(blob)
                filename = path.relative_to(root).as_posix()
                for candidate in declarations(tree, parts):
                    if len(results) >= MAX_RESULTS:
                        raise ValueError("C# result limit reached")
                    results.append(declaration_evidence(blob, candidate, filename, package))
                if tree.root_node.has_error and len(fallback) < 3:
                    left = blob.rfind(b"\n", 0, match.start()) + 1
                    right = blob.find(b"\n", match.end())
                    line = blob.count(b"\n", 0, left) + 1
                    fallback.append({
                        "fragment": blob[left:right if right != -1 else len(blob)][:500].decode("utf-8", errors="replace"),
                        "confidence": "signature_unverified", "path": filename, "line_start": line,
                        "line_end": line, "package": package["package"], "package_version": package["version"],
                        "source": "installed_csharp",
                    })
    except ValueError:
        truncated = True
    results = results or fallback
    if any(item["confidence"] == "syntax_verified" for item in results):
        status = "declarations_found"
    elif results:
        status = "signature_unverified"
    elif not files or truncated or skipped:
        status = "requires_source_inspection"
    else:
        status = "not_found"
    return {
        "symbol": symbol, "status": status, "results": results, "truncated": truncated,
        "files_scanned": min(files, 8000), "files_skipped": skipped,
        "source_roots": [path for _, path in roots][:50],
        "scope": "Local declarations only. Unity compilation, inherited/generated APIs and overload binding require project validation.",
    }
