# ComfyUI-RandomPromptTokens

A small, independent ComfyUI custom-node package for building prompts from reusable random option lists.

Current package version: `1.1.0`.

## Node

The package adds one node:

`Random Prompt Tokens`

It accepts one large multiline main text field and twenty separate multiline option fields named `options_001` through `options_020`.

The main prompt editor opens at twenty visible lines and can be vertically resized. Each option editor opens at seven visible lines; longer option lists scroll inside the field so the node does not become endlessly tall. A small frontend extension applies these dimensions to both new and already-saved node instances.

Use tokens in the main text like this:

```text
I like color ^001, number ^002, and a cinematic mood that feels ^003.
```

Then put one choice per line in the matching fields:

```text
options_001:
crimson
electric blue
deep emerald
```

```text
options_002:
7
23
108
```

```text
options_003:
quiet and mysterious
epic and luminous
surreal but elegant
```

The output might be:

```text
I like color electric blue, number 23, and a cinematic mood that feels surreal but elegant.
```

Each token is selected once per execution. If `^001` appears several times, every occurrence receives the same selected value. This keeps a generated prompt internally consistent.

## Seed behavior

- `seed = 0`: choose fresh random values on each execution.
- Any positive seed: produce repeatable selections for the same text and option lists.

The node explicitly opts out of ComfyUI output caching when the seed is zero.
This means pressing Queue again really does make a new choice even when no
visible input changed. Positive seeds retain normal deterministic caching.

The second output is a JSON selection report containing the seed actually used, selected values, token counts, and missing tokens. It is useful for reproducing or debugging a generated prompt.

## Missing options

If the main text references a token whose field is empty, the node leaves a visible marker:

```text
!MISSING:^003!
```

The same token is also listed in the selection report.

## Why there are twenty fields

ComfyUI normally builds a node's visible inputs when the node loads. For a reliable first version, this package provides twenty fixed option fields and only uses the ones referenced by the current text. A later version can add more fields or explore dynamic widget behavior.

## Installation

Open a terminal in `ComfyUI/custom_nodes` and clone the repository:

```powershell
git clone https://github.com/monoescobar/ComfyUI-RandomPromptTokens.git
```

The installed folder will be:

```text
ComfyUI/custom_nodes/ComfyUI-RandomPromptTokens
```

Restart ComfyUI. The node appears under:

```text
🎬 Escobarte/Text & Prompt/Random Prompt Tokens
```

To install future updates, open a terminal in the installed folder and run:

```powershell
git pull
```

No extra Python packages are required. The package is independent of `ComfyUI-Ideogram4-CinematicJSON` and `ComfyUI-Pixaroma-260117`.

## Node notes

- Supported placeholders are `^001` through `^020`.
- A token may appear more than once; one value is chosen and reused everywhere.
- Empty lines in option fields are ignored.
- A referenced empty or unavailable field becomes `!MISSING:^NNN!` instead of
  silently disappearing.
- The node never edits source files and never performs network requests.
- `selection_report` is intended for metadata, debugging, and exact reruns.

See [docs/NODE_REFERENCE.md](docs/NODE_REFERENCE.md) for the complete input,
output, caching, and compatibility contract.

## Development and verification

Run the dependency-free test suite from the repository root:

```powershell
python -m unittest discover -s tests -v
```

GitHub Actions runs the same suite and compiles the Python package on every
push and pull request.

## Typical wiring

```text
Random Prompt Tokens.resolved_text
    -> Gemma / text prompt input

Random Prompt Tokens.selection_report
    -> optional text display, logging, or metadata node
```
