// EDUCATIONAL DATA SHAPES ONLY — NOT A COMPLETE CONTROLLER, NOT UNITY-COMPILED.
// Before use confirm PurrDiction version, IPredictedData/IMath codegen and namespace.
// No Unity GameObject/Transform in rollback STATE. See best-practices docs.
using UnityEngine;
using PurrNet.Prediction;

public struct ExampleMoveInput : IPredictedData
{
    public Vector2 move;
    public bool jump;
    public void Dispose() { }
}

public struct ExampleMoveState : IPredictedData<ExampleMoveState>
{
    public Vector3 position;
    public Vector3 velocity;
    public float jumpCooldown;
    public void Dispose() { }
}
