# Drafts

Versioned, first-pass video clips generated from the prompts. These are the
*raw outputs* before editing, not the final master.

## Naming convention

```
drafts/scene-<id>-<seed>-v<version>.mp4
```

Examples:

```
drafts/scene-05-8123456-v1.mp4   # first pass of the scale-down scene
drafts/scene-05-8123456-v2.mp4   # re-roll of the same scene, same seed
drafts/scene-05-9988777-v1.mp4   # new seed for a different take
```

## Workflow

1. For each shot in `shots/manifest.yaml`, generate a clip with the model of
   choice (text prompt or start/end keyframes).
2. Record the `seed` and `status` back into the manifest — `todo` → `draft` →
   `keep`.
3. Re-roll only the bad scenes; never regenerate the whole video.

`drafts/` media files (`.mp4`, `.mov`, `.webm`) are gitignored. This directory
exists so the convention and `.gitkeep` are committed.
