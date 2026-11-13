// Demo PurrNet uniquement, non compilée dans Unity ici.
// Vérifier la compatibilité de la version installée et configurer Network Rules.
using PurrNet;
using UnityEngine;

public class ExampleNetworkCounter : NetworkBehaviour
{
    [SerializeField] private int maxValue = 100;
    private SyncVar<int> _count = new(0);

    public int Count => _count.value;

    // Appeler depuis une UI du propriétaire autorisé (après spawn).
    public void RequestIncrement()
    {
        IncrementOnServer();
    }

    [ServerRpc]
    private void IncrementOnServer()
    {
        // Démo : limite de valeur, PAS une protection contre le spam.
        if (_count.value >= maxValue)
            return;

        _count.value += 1;
    }
}
