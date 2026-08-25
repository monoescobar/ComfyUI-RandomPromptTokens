import importlib.util
import json
import math
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("random_prompt_tokens_local", ROOT / "nodes.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
RandomPromptTokens = MODULE.RandomPromptTokens


class RandomPromptTokensTests(unittest.TestCase):
    def test_positive_seed_is_reproducible_and_repeated_tokens_match(self):
        node = RandomPromptTokens()
        kwargs = {"options_001": "red\nblue", "options_002": "silk\nwool"}
        first = node.randomize("^001, ^002, then ^001", 42, **kwargs)
        second = node.randomize("^001, ^002, then ^001", 42, **kwargs)
        self.assertEqual(first, second)
        resolved, report_text = first
        report = json.loads(report_text)
        self.assertEqual(resolved.split(", ")[0], resolved.split("then ")[1])
        self.assertEqual(report["seed_used"], 42)

    def test_missing_tokens_are_visible_and_reported(self):
        resolved, report_text = RandomPromptTokens().randomize("look ^003", 7)
        self.assertEqual(resolved, "look !MISSING:^003!")
        self.assertEqual(json.loads(report_text)["missing_tokens"], ["^003"])

    def test_empty_lines_are_ignored(self):
        resolved, report_text = RandomPromptTokens().randomize(
            "^001", 9, options_001="\n satin \n\n"
        )
        self.assertEqual(resolved, "satin")
        self.assertEqual(json.loads(report_text)["option_counts"]["^001"], 1)

    def test_cache_contract_matches_seed_semantics(self):
        self.assertTrue(math.isnan(RandomPromptTokens.IS_CHANGED("x", 0)))
        self.assertEqual(RandomPromptTokens.IS_CHANGED("x", 123), 123)

    def test_registered_interface_and_notes_are_complete(self):
        self.assertTrue(RandomPromptTokens.DESCRIPTION)
        self.assertEqual(len(RandomPromptTokens.RETURN_TYPES), 2)
        self.assertEqual(len(RandomPromptTokens.RETURN_NAMES), 2)
        self.assertEqual(len(RandomPromptTokens.OUTPUT_TOOLTIPS), 2)
        required = RandomPromptTokens.INPUT_TYPES()["required"]
        self.assertEqual(list(required)[:2], ["text", "seed"])
        self.assertEqual(len(required), 22)
        for _, specification in required.items():
            self.assertTrue(specification[1].get("tooltip"))


if __name__ == "__main__":
    unittest.main()
