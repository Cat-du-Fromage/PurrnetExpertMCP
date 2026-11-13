// EDUCATIONAL ONLY — NOT COMPILED AGAINST UNITY IN THIS RELEASE.
// PurrNet NetworkAnimator is the documented API for synchronized triggers.
// Call TriggerPunch ONLY from the authoritative controller under your Network Rules.
using PurrNet;
using UnityEngine;

public class ExampleNetworkAnimator : MonoBehaviour
{
    [SerializeField] private NetworkAnimator networkAnimator;

    public void TriggerPunch()
    {
        if (networkAnimator == null)
        {
            Debug.LogError("Assign NetworkAnimator on the same object as Animator.");
            return;
        }
        networkAnimator.SetTrigger("Punch");
    }
}
