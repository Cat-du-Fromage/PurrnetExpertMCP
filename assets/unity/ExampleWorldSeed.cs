// Demo PurrNet uniquement, non compilée dans Unity ici.
// Vérifier les options nommées de ObserversRpc dans la version installée.
using PurrNet;
using UnityEngine;

public class ExampleWorldSeed : NetworkBehaviour
{
    public int CurrentSeed { get; private set; }

    protected override void OnSpawned(bool asServer)
    {
        if (!asServer)
            return;

        // Le serveur choisit la graine même en dedicated (sans client local).
        BroadcastSeed(Random.Range(1, int.MaxValue));
    }

    [ObserversRpc(runLocally: true, bufferLast: true)]
    private void BroadcastSeed(int value)
    {
        CurrentSeed = value;
        Debug.Log($"PurrNet example world seed: {CurrentSeed}");
    }
}
