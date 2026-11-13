# Voice chat: PurrVoice, Dissonance, permissions

Official: `tools/purrvoice-voice-chat/README.md`, `microphone-input.md`, `muting.md`, `filters.md`, `lip-sync.md`, `providers/`, `integrations/dissonance.md`.

- PurrVoice docs are marked **Early Access** as reviewed; do not promise that all users can install it or that APIs are stable. Verify package entitlement/version and platform device support before writing code.
- Input devices: current docs show `AudioDevices.devices` and `PurrVoicePlayer.ChangeMicrophone(...)`; validate nonempty list, device hotplug and permissions. Use the local player's PurrVoicePlayer.
- Separate sender/server/receiver voice filters, mutable runtime parameters and privacy. Mute and push-to-talk must be enforced at the right layer, not only as a local UI toggle.
- For Dissonance integration, use current `integrations/dissonance.md` and installed integration; old Stray FAQ claims may be outdated. Test transport and headless compatibility.
- Voice routing must follow lobby/team/observer rules if relevant; keep moderation/privacy consent and platform microphone permissions explicit. Do not leak microphone buffer via gameplay RPC logs.
- Test two remote clients, device switching, mute, filter on/off, reconnect, silent headless server, WebGL/mobile support if targeted.
