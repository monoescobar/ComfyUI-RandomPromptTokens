# Node reference

## Random Prompt Tokens

Internal node type: `RandomPromptTokens`

Category: `🎬 Escobarte/Text & Prompt`

The node resolves fixed placeholders in a multiline string from independent
multiline option lists. It has no network, filesystem, model, image, or video
side effects.

### Inputs

| Input | Type | Contract |
| --- | --- | --- |
| `text` | `STRING` | Main text containing zero or more `^NNN` placeholders. |
| `seed` | `INT` | `0` is fresh per execution; positive values are deterministic. |
| `options_001` … `options_020` | `STRING` | One intact option per non-empty line. |

Only `^001` through `^020` have option fields. A syntactically valid token
outside that range is reported as missing.

### Outputs

| Output | Type | Contract |
| --- | --- | --- |
| `resolved_text` | `STRING` | Text with each requested token replaced once and reused consistently. |
| `selection_report` | `STRING` | Human-readable JSON audit record. |

The report contains `seed_input`, `seed_used`, `tokens_found`,
`selected_values`, `missing_tokens`, and `option_counts`.

### Failure and cache behavior

Missing values are explicit: `^003` becomes `!MISSING:^003!`. This avoids
quietly producing an incomplete production prompt.

ComfyUI normally caches node outputs when inputs do not change. The node's
`IS_CHANGED` contract returns NaN only when `seed` is zero, forcing the fresh
mode to execute again. Positive seeds preserve deterministic behavior.

### Compatibility promise

The internal type name, input order, output order, token syntax, and JSON keys
are treated as stable workflow contracts. Changes to them require a documented
migration and a major version increment.
