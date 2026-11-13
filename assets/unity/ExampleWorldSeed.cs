// PurrNet example. Not compiled in Unity.
// Check named ObserversRpc options in the installed version.
using PurrNet;
using UnityEngine;

public class ExampleWorldSeed : NetworkBehaviour
{
    public int CurrentSeed { get; private set; }

    protected override void OnSpawned(bool asServer)
    {
        if (!asServer)
            return;

        // The server selects the seed, including on a dedicated server without a local client.
        BroadcastSeed(Random.Range(1, int.MaxValue));
    }

    [ObserversRpc(runLocally: true, bufferLast: true)]
    private void BroadcastSeed(int value)
    {
        CurrentSeed = value;
        Debug.Log($"PurrNet example world seed: {CurrentSeed}");
    }
}
