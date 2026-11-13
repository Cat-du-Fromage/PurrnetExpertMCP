# NetworkAudioSource

Official: `plug-n-play-components/network-audio-source.md`.

- Add `AudioSource` and `NetworkAudioSource` on the same GameObject. Choose Inspector `_ownerAuth`: owner-driven by default, or server-driven; uncontrolled method calls can silently do nothing.
- If clips change **at runtime** or `PlayOneShot(AudioClip, float)` uses dynamic clips, register those AudioClip assets in **NetworkAssets**. An immutable clip baked into a prefab does not need the extra registry.
- Public wrapper methods include `Play`, `Stop`, `Pause`, `UnPause`, `PlayOneShot`; setters include `clip`, `volume`, `pitch`, `loop`, `mute`, `spatialBlend`, distance and time. Check installed API for overloads.
- Do **not** call normal audio playback from replayable PurrDiction `Simulate`; drive one-shot effects from PredictedEvent, verified view, or external classic events.
- Test late join for looping/current state, one-shot while clients observe, ownership change, dynamically referenced clips; avoid assuming all past transient sounds are replayed.
