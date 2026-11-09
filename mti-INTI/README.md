# Cimory Sales App — Scale-out Storyboard

**"Prompt as Source"** workspace. The prompts in [`storyboard.md`](storyboard.md) are
the source of truth; the generated video is the *build artifact*.

## What this is

A scene-by-scene, model-agnostic prompt deck for a **Zack D Films–style 3D
animation** that explains a business **scale-out** scenario for the Cimory sales
app (milk, yogurt, RTE sausages). One scene specifically illustrates how
**scaling down** server capacity trickles down into a degraded user experience,
measured in minutes.

## Files

| File | Purpose |
| --- | --- |
| `storyboard.md` | The single source: master brief, style bible, shared negative prompt, and seven scene prompts. |
| `keyframes/` | Intermediate still images: `00-lookdev.md` (style lock) + one start/end frame prompt per scene. |
| `shots/manifest.yaml` | Machine-readable shot manifest (id, duration, camera, keyframes, seed, status). |
| `drafts/` | Versioned, first-pass video clips (naming + workflow in `drafts/README.md`). |

## Pipeline

```
storyboard.md ──(text)→ keyframes/*.md ──(image model)→ keyframes/out/*.png
      │                                                     │
      └────────────(derive)→ shots/manifest.yaml ───────────┘
                                      │
                                      └──(video model)→ drafts/*.mp4 → final master
```

1. **Storyboard** — write the scenes in `storyboard.md` (source of truth).
2. **Keyframes** — generate `00-lookdev` + per-scene start/end frames; these pin
   the look and motion.
3. **Manifest** — `shots/manifest.yaml` records each shot's keyframes, seed, and
   status so re-rolls are tracked.
4. **Drafts** — generate clips into `drafts/`, log the seed, re-roll only bad scenes.

## How to feed the prompts

Two paths, both model-agnostic (Veo, Sora, Runway, Kling, Pika, Luma, …).

### Path A — text only

Each scene block is self-contained so you can copy it **on its own** or paste
the whole deck **in order**.

1. Open [`storyboard.md`](storyboard.md).
2. Copy the **style bible** (look, camera, lighting) — prepend it to any scene
   prompt if your model does not carry style across a batch.
3. For each scene, copy the `Prompt` field into your video model's text prompt.
4. Copy the shared + scene `Negative prompt` into the model's negative-prompt
   field (where supported).

### Path B — keyframe-conditioned (recommended for consistency)

1. Generate the **look-dev** frame from `keyframes/00-lookdev.md`, then the
   **start/end** frames for each scene from `keyframes/01-*.md` … `07-*.md`
   (see `keyframes/README.md` for the exact flow and filenames).
2. Feed each scene's text `Prompt` **plus** its `keyframe_start`/`keyframe_end`
   images (from `shots/manifest.yaml`) into an image-to-video model.
3. Save the output to `drafts/` using `scene-<id>-<seed>-v<version>.mp4`, then
   log the `seed` and update `status` back in the manifest.
4. Re-roll only the bad scenes; assemble the `keep` clips into the final master.

## Conventions

- **Model-agnostic:** prompts are rich prose, not vendor-specific syntax.
- **English throughout:** video models respond best to English; keep
  `Cimory` and product terms intact.
- **Self-contained scenes:** each scene restates the essential look so it can
  be generated standalone or as a batch.
- **One job per scene:** every scene has a single `Goal` — if a prompt tries to
  do two things, split the scene.
- **Numbers over adjectives:** prefer concrete reads ("3 minutes") over vague
  ones ("very slow").

## Style

Dark navy background, glowing neon cyan/blue accents, warm orange for warnings,
floating holographic UI, smooth camera with punch-ins, pop-in captions.
