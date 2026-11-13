#!/usr/bin/env python3
"""Offline diagnostic for intended purrnet-expert vs edgegap-purrnet routing.

This cannot cause a model/agent to load an unselected skill. Run live routing evals separately.
"""
from __future__ import annotations
import argparse
import json
import re
from trigger_probe import detect
from route_docs import norm

# Provider specificity must trump a generic PurrNet host/server symptom, but only
# where Edgegap operations are actually requested. Merely naming Edgegap in a negative
# comparison or discussing a pre-existing host bug is insufficient.
EDGEGAP_WORDS = ("edgegap", "arbitrium", "registry.edgegap.com", "edgegap sdk")
EDGEGAP_TASKS = (
    "deploy", "deploi", "heberg", "hosting", "host my", "cloud", "matchmak", "find match", "conteneur", "container",
    "docker", "allocation", "app version", "registry", "port externe", "external port", "self stop", "self-stop",
    "dedicated server on edgegap", "serveur dedie sur edgegap", "edgegap server", "edgegap deployment", "edgegap matchmaker",
)
OTHER_STACKS = ("fishnet", "mirror", "netcode for gameobjects", "ngo", "unreal engine", "unreal", "godot", "photon fusion")


def choose(prompt: str, purrnet_project: bool = False) -> dict:
    q = norm(prompt)
    foreign = any(re.search(r"\b" + re.escape(s) + r"\b", q) for s in OTHER_STACKS)
    if re.search(r"\b(?:not|without|sans|pas(?:\s+de)?|not using)\s+purrnet\b", q):
        return {"choice": None, "reason": "Explicitly excludes PurrNet", "caveat": "Proxy only"}
    explicit_purrnet = any(s in q for s in ("purrnet", "purrdiction", "dev.purrnet.purrnet"))
    if foreign and not (explicit_purrnet or purrnet_project):
        return {"choice": None, "reason": "Other netcode, not known PurrNet project", "caveat": "Proxy only"}
    has_edgegap = any(s in q for s in EDGEGAP_WORDS)
    edgegap_work = any(s in q for s in EDGEGAP_TASKS)
    if has_edgegap and edgegap_work and (explicit_purrnet or purrnet_project):
        return {"choice": "edgegap-purrnet", "also_consult": "purrnet-expert for gameplay changes", "reason": "Edgegap-specific deployment workflow", "caveat": "Proxy only"}
    native = detect(prompt, purrnet_project)
    return {"choice": "purrnet-expert" if native["should_suggest_skill"] else None,
            "reason": native["reason"], "caveat": "Proxy only"}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("prompt")
    p.add_argument("--purrnet-project", action="store_true")
    a = p.parse_args(argv)
    print(json.dumps(choose(a.prompt, a.purrnet_project), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
