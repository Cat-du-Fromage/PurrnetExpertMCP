# Optional Roslyn syntax audit (experimental)

The Python guard is only text/brace based. This optional C# project uses Roslyn
syntax trees to follow same-class helper calls across `partial` files; it is a
first migration step, **not a semantic analyzer with Unity assembly resolution**.

Prerequisites: .NET 8 SDK and NuGet package access for `Microsoft.CodeAnalysis.CSharp`.

```bash
dotnet run --project scripts/roslyn/PurrNetReplayAudit.csproj -- /path/to/UnityProject
```

**Not compiled or executed in the packaging environment** (`dotnet`/Unity are
not available). No claim of complete replay safety; manually inspect Unity
version-specific APIs, generated RPC code, virtual dispatch, delegates,
coroutines, lambdas, context and asynchronous operations. Prefer building a
Unity project and running host/remote/rollback tests.
