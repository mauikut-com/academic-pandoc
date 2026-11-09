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

## How to feed the prompts

Each scene block is self-contained so you can copy it **on its own** or paste
the whole deck **in order**.

1. Open [`storyboard.md`](storyboard.md).
2. Copy the **style bible** (look, camera, lighting) — prepend it to any scene
   prompt if your model does not carry style across a batch.
3. For each scene, copy the `Prompt` field into your video model's text prompt.
4. Copy the shared + scene `Negative prompt` into the model's negative-prompt
   field (where supported).

Works across Veo, Sora, Runway, Kling, Pika, Luma, and similar text-to-video
tools.

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
