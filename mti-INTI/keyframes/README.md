# Keyframes

Intermediate representation between the text `storyboard.md` and the final
video: **still images** that (a) lock the visual style and (b) give
image-to-video models a concrete start/end anchor per scene.

## Why

Text-only prompts drift in color, look, and composition between scenes. Two
frames per scene pin the motion: the model animates *from* the start frame *to*
the end frame instead of improvising.

## Files

| File | What it produces |
| --- | --- |
| `00-lookdev.md` | One style-lock hero image — reuse as the reference for every scene. |
| `01-hook.md` … `07-outro.md` | Start + end frame prompt per scene. |

## How to generate

1. Run each `.md` prompt in an image model (Midjourney, Flux, DALL·E, Imagen,
   etc.).
2. Save outputs to `keyframes/out/` using the naming below.
3. Use `00-lookdev.png` as the style reference (e.g. `--sref`, image reference,
   or a style-consistency input) when generating every scene keyframe.

```
keyframes/out/
├── 00-lookdev.png
├── 01-hook-start.png
├── 01-hook-end.png
├── 02-baseline-start.png
├── 02-baseline-end.png
├── …
└── 07-outro-end.png
```

The `keyframes/out/` directory is gitignored — the `.md` prompts are the source;
the PNGs are regenerable artifacts.
