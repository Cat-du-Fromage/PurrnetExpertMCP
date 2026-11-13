// PurrNet example. Not compiled in Unity.
// Check the installed version and configure Network Rules.
using PurrNet;
using UnityEngine;

public class ExampleNetworkCounter : NetworkBehaviour
{
    [SerializeField] private int maxValue = 100;
    private SyncVar<int> _count = new(0);

    public int Count => _count.value;

    // Call from the authorized owner's UI after spawning.
    public void RequestIncrement()
    {
        IncrementOnServer();
    }

    [ServerRpc]
    private void IncrementOnServer()
    {
        // Clamp the value. Rate limiting requires a separate check.
        if (_count.value >= maxValue)
            return;

        _count.value += 1;
    }
}
