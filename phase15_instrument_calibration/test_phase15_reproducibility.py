#!/usr/bin/env python3
import copy
import unittest
from collections import Counter

import phase15_reproducibility as p


class Phase15ReproducibilityTests(unittest.TestCase):
    def test_split_is_deterministic_and_complete(self):
        items = [f"page-{i}" for i in range(10)]
        first = p.allocate_splits(items, "fixture")
        second = p.allocate_splits(list(reversed(items)), "fixture")
        self.assertEqual(first, second)
        self.assertEqual(set(first), set(items))
        self.assertEqual(Counter(first.values()), Counter({"train": 6, "validation": 2,
                                                          "final_test": 2}))

    def test_corpus_hash_detects_mutation(self):
        records = [{"document": "D", "page": "P", "order": 0, "line_id": "L",
                    "split": "train", "tokens": ["a", "b"]}]
        corpus = p.corpus_payload("fixture", {"source": "fixture"}, records)
        expected = corpus.pop("corpus_sha256")
        self.assertEqual(expected, p.canonical_hash(corpus))
        changed = copy.deepcopy(corpus)
        changed["records"][0]["tokens"][0] = "x"
        self.assertNotEqual(expected, p.canonical_hash(changed))

    def test_line_parser_preserves_unicode_tokens(self):
        value = "trũ sacrm̃ pnĩe ⁊ ꝯt̾tio"
        self.assertEqual(value.split(), ["trũ", "sacrm̃", "pnĩe", "⁊", "ꝯt̾tio"])


if __name__ == "__main__":
    unittest.main()
