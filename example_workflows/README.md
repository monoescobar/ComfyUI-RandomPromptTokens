# Example wiring

1. Add `Random Prompt Tokens` from `🎬 Escobarte/Text & Prompt`.
2. Put the reusable prompt in `text`.
3. Write one option per line in the matching `options_001`, `options_002`, and later fields.
4. Use `seed = 0` for a new combination each run, or a positive seed for repeatable results.
5. Connect `resolved_text` to the Gemma/VLM text input.
6. Connect `selection_report` to a text viewer or log node when you want to record the selected choices.

Example:

```text
text:
Create a professional cinematic still with ^001 lighting, ^002 camera movement, and ^003 atmosphere.

options_001:
soft dawn light
hard tungsten side light
cool moonlight with warm practicals

options_002:
slow forward dolly
low tracking view
wide upward-looking perspective

options_003:
subtle atmospheric haze
rain-slick reflections
floating dust and volumetric beams
```
