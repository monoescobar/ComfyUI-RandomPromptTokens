import json
import random
import re
import secrets
from typing import Dict, List, Tuple


TOKEN_RE = re.compile(r"\^(\d{3})(?!\d)")
OPTION_FIELD_COUNT = 20
MAIN_TEXT_LINES = 20
OPTION_LINES = 5


def _option_lines(value: str) -> List[str]:
    """Return non-empty option lines while keeping each choice intact."""
    return [line.strip() for line in str(value or "").splitlines() if line.strip()]


def _field_name(number: int) -> str:
    return f"options_{number:03d}"


class RandomPromptTokens:
    """Replace ^001-style tokens with seeded random multiline options."""

    CATEGORY = "🎬 Escobarte/Text & Prompt"
    SEARCH_ALIASES = [
        "RandomPromptTokens",
        "Random Prompt",
        "Prompt Randomizer",
        "Random Text",
        "Prompt Tokens",
    ]
    FUNCTION = "randomize"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("resolved_text", "selection_report")

    @classmethod
    def INPUT_TYPES(cls):
        required = {
            "text": (
                "STRING",
                {
                    "default": "I like color ^001, and number ^002.",
                    "multiline": True,
                    "lines": MAIN_TEXT_LINES,
                    "dynamicPrompts": False,
                },
            ),
            "seed": (
                "INT",
                {
                    "default": 0,
                    "min": 0,
                    "max": 2147483647,
                    "step": 1,
                },
            ),
        }
        for number in range(1, OPTION_FIELD_COUNT + 1):
            required[_field_name(number)] = (
                "STRING",
                {
                    "default": "",
                    "multiline": True,
                    "lines": OPTION_LINES,
                    "placeholder": "One option per line",
                    "dynamicPrompts": False,
                },
            )
        return {"required": required}

    def randomize(self, text: str, seed: int, **kwargs):
        source = str(text or "")
        requested_tokens = sorted({int(match) for match in TOKEN_RE.findall(source)})

        # Seed 0 means a fresh random result. A positive seed makes the run reproducible.
        seed_used = int(seed) if int(seed) != 0 else secrets.randbits(63)
        rng = random.Random(seed_used)

        choices: Dict[str, str] = {}
        missing: List[str] = []
        available: Dict[int, List[str]] = {}

        for number in requested_tokens:
            field = kwargs.get(_field_name(number), "") if number <= OPTION_FIELD_COUNT else ""
            options = _option_lines(field)
            available[number] = options
            token = f"^{number:03d}"
            if not options:
                missing.append(token)
                choices[token] = f"!MISSING:{token}!"
            else:
                # Choose once per token so repeated placeholders stay consistent.
                choices[token] = rng.choice(options)

        resolved = TOKEN_RE.sub(lambda match: choices[f"^{int(match.group(1)):03d}"], source)
        report = {
            "seed_input": int(seed),
            "seed_used": seed_used,
            "repeated_tokens_reuse_same_value": True,
            "tokens_found": [f"^{number:03d}" for number in requested_tokens],
            "selected_values": choices,
            "missing_tokens": missing,
            "option_counts": {
                f"^{number:03d}": len(options) for number, options in available.items()
            },
        }
        return (resolved, json.dumps(report, ensure_ascii=False, indent=2))


NODE_CLASS_MAPPINGS = {
    "RandomPromptTokens": RandomPromptTokens,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomPromptTokens": "Random Prompt Tokens",
}
