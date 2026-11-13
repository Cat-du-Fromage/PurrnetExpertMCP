// Optional Roslyn SYNTAX audit, not an Unity semantic compilation.
// Supply a Unity project root as the sole arg. Does not execute project code.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

if (args.Length != 1 || !Directory.Exists(args[0]))
{
    Console.Error.WriteLine("usage: dotnet run --project scripts/roslyn/PurrNetReplayAudit.csproj -- <Unity-project-root>");
    return 2;
}
string root = Path.GetFullPath(args[0]);
var files = Directory.EnumerateFiles(root, "*.cs", SearchOption.AllDirectories)
    .Where(p => !p.Substring(root.Length).Split(Path.DirectorySeparatorChar)
        .Any(x => x is "Library" or "PackageCache" or ".git" or "Temp"))
    .Where(p => new FileInfo(p).Length < 2_000_000)
    .OrderBy(p => p).ToList();

var classes = new Dictionary<string,List<ClassDeclarationSyntax>>(StringComparer.Ordinal);
foreach (string file in files)
{
    var tree = CSharpSyntaxTree.ParseText(File.ReadAllText(file), path:file);
    foreach (var c in tree.GetRoot().DescendantNodes().OfType<ClassDeclarationSyntax>())
    {
        // Include parent namespace to avoid collisions for common type names.
        string ns = string.Join(".",c.Ancestors().OfType<BaseNamespaceDeclarationSyntax>().Reverse().Select(x=>x.Name.ToString()));
        string id = ns + ":" + c.Identifier.ValueText;
        if (!classes.TryGetValue(id, out var group)) classes[id]=group=new();
        group.Add(c);
    }
}

int findings=0;
foreach (var group in classes)
{
    bool predicted=group.Value.Any(c => c.BaseList?.Types.Any(t =>
        t.Type.ToString().Contains("PredictedIdentity",StringComparison.Ordinal) ||
        t.Type.ToString().Contains("DeterministicIdentity",StringComparison.Ordinal) ||
        t.Type.ToString().Contains("PredictedModule",StringComparison.Ordinal)) == true);
    if (!predicted) continue;
    var methods=group.Value.SelectMany(c=>c.Members.OfType<MethodDeclarationSyntax>())
        .GroupBy(m=>m.Identifier.ValueText).ToDictionary(g=>g.Key,g=>g.ToList());
    var audioFields=group.Value.SelectMany(c=>c.Members.OfType<FieldDeclarationSyntax>())
        .Where(f=> new[]{"AudioSource","ParticleSystem","VisualEffect"}.Any(t=>f.Declaration.Type.ToString().Contains(t)))
        .SelectMany(f=>f.Declaration.Variables.Select(v=>v.Identifier.ValueText)).ToHashSet();
    foreach (var rootMethod in methods.Where(kv=>kv.Key is "Simulate" or "LateSimulate").SelectMany(kv=>kv.Value))
    {
        var visited=new HashSet<MethodDeclarationSyntax>();
        void Explore(MethodDeclarationSyntax m, string trace)
        {
            if (!visited.Add(m) || trace.Split(" -> ").Length > 15)return;
            foreach (var call in m.DescendantNodes().OfType<InvocationExpressionSyntax>())
            {
                string expr=call.Expression.ToString();
                string member=call.Expression switch
                {
                    IdentifierNameSyntax id=>id.Identifier.ValueText,
                    MemberAccessExpressionSyntax ma=>ma.Name.Identifier.ValueText,
                    _=>""
                };
                string receiver=call.Expression is MemberAccessExpressionSyntax access?access.Expression.ToString():"";
                string? reason=null;
                if (receiver is "Input" or "Time" or "UnityEngine.Random" or "Random" or "PlayerPrefs" or "Analytics" or "UnityWebRequest" ||
                    receiver.StartsWith("Input.") || receiver.StartsWith("Time."))reason="live input/time/network/persistence in replay";
                if (member is "Instantiate" or "Destroy")reason="ordinary Unity spawn/despawn in replay";
                if ((member is "Play" or "PlayOneShot" or "Emit") &&
                    (audioFields.Contains(receiver)||receiver is "AudioSource" or "ParticleSystem"))reason="audio/particles in replay";
                else if (member is "Play" or "PlayOneShot" or "Emit")reason="possible visual-only side effect (inspect receiver type)";
                if (member is "Send" or "SendAsync" && receiver.Contains("UnityWebRequest"))reason="network request in replay";
                if (reason is not null)
                {
                    var loc=call.GetLocation().GetLineSpan();
                    Console.WriteLine($"REVIEW {loc.Path}:{loc.StartLinePosition.Line+1} via {trace}: {reason} [{expr}]");
                    findings++;
                }
                if (call.Expression is IdentifierNameSyntax idName && methods.TryGetValue(idName.Identifier.ValueText,out var callee))
                    foreach (var target in callee) Explore(target,trace+" -> "+idName.Identifier.ValueText);
            }
        }
        Explore(rootMethod,rootMethod.Identifier.ValueText);
    }
}
Console.WriteLine($"Roslyn syntax issues: {findings}. Advisory only; no semantic model resolving Unity symbols, async delegates, dispatch, or generated code.");
return findings>0?1:0;
