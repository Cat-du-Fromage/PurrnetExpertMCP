# NetworkReflection, NetworkBones, NetworkOwnershipToggle

Official: `plug-n-play-components/network-reflection-auto-sync.md`, `network-bones.md`, `network-ownership-toggle.md`.

## NetworkReflection
- Can inspect another component (including built-in Unity components) and select properties to synchronize automatically; Inspector has Owner Auth. Good for simple state mirroring, **not** a license to send every property every frame.
- Audit generated traffic, serialization support, lifecycle and authority. Avoid for sensitive, high-frequency or predictable simulation state without measurements.

## NetworkBones
- Consider for networked bone/hierarchy pose instead of manually making RPC calls per bone. Verify supported setup and chosen update rate in the installed package and docs; profile payload cost as bone count rises.

## NetworkOwnershipToggle
- Consider for enabling local scripts/cameras/input based on ownership instead of scattering `isOwner` branches. Verify precise activation semantics during host, owner transfer, spawn/despawn and reconnect.

Do not infer methods from class names. Both NetworkBones and NetworkOwnershipToggle must be inspected in local package before authoring code.
