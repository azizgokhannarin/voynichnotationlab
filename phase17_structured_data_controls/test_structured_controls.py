#!/usr/bin/env python3
from __future__ import annotations

import unittest
from collections import Counter

import build_structured_controls as builder
import evaluate_structured_controls as evaluator


class StructuredControlTests(unittest.TestCase):
    def setUp(self):
        self.specs = [
            {"line_id": "line-0000", "page": "page-000", "order": 0, "length": 4},
            {"line_id": "line-0001", "page": "page-000", "order": 1, "length": 2},
        ]

    def test_deterministic_shuffle_preserves_each_line_inventory(self):
        lines = [["a", "a", "b", "c"], ["x", "y"]]
        first = builder.deterministic_shuffle(lines, "test", self.specs)
        second = builder.deterministic_shuffle(lines, "test", self.specs)
        self.assertEqual(first, second)
        for left, right in zip(lines, first):
            self.assertEqual(Counter(left), Counter(right))

    def test_mushroom_raw_and_qualified_have_frozen_lengths(self):
        rows = [[chr(97 + ((i + j) % 20)) for j in range(23)] for i in range(4)]
        raw, _ = builder.mushroom_line_inventories(rows, self.specs, False)
        qualified, _ = builder.mushroom_line_inventories(rows, self.specs, True)
        self.assertEqual(list(map(len, raw)), [4, 2])
        self.assertEqual(list(map(len, qualified)), [4, 2])
        self.assertEqual(raw[0][0], "a")
        self.assertEqual(qualified[0][0], "F00:a")

    def test_corpus_payload_contains_validation_only(self):
        corpus = builder.corpus_payload("control", self.specs,
                                        [["a", "a", "b", "c"], ["x", "y"]],
                                        {"source": "fixture"})
        self.assertEqual({record["split"] for record in corpus["records"]}, {"validation"})
        body = dict(corpus)
        expected = body.pop("corpus_sha256")
        self.assertEqual(builder.canonical_hash(body), expected)

    def test_exact_inventory_pair_gate(self):
        left = builder.corpus_payload("a", self.specs,
                                      [["a", "a", "b", "c"], ["x", "y"]], {})
        right = builder.corpus_payload("b", self.specs,
                                       [["c", "a", "b", "a"], ["y", "x"]], {})
        self.assertTrue(builder.exact_line_inventory_equal(left, right))

    @staticmethod
    def fake_metric(ratio: float, significant: bool) -> dict:
        return {"observed_to_null_ratio": ratio, "significant_holm_0_01": significant,
                "z": 0.0, "holm_adjusted_p": 0.5}

    def test_full_phenotype_rule(self):
        result = {"null_families": {
            "document_shuffle": {"metrics": {
                "page_repeat_mass": self.fake_metric(1.2, True),
                "line_repeat_mass": self.fake_metric(1.4, True)}},
            "page_shuffle": {"metrics": {
                "line_repeat_mass": self.fake_metric(1.1, True)}},
            "line_shuffle": {"metrics": {
                "line_identity_gap1": self.fake_metric(1.0, False),
                "line_identity_gap2_4": self.fake_metric(1.0, False),
                "line_identity_gap5_16": self.fake_metric(1.0, False)}},
        }}
        self.assertTrue(evaluator.phenotype(result)["full_phenotype_match"])

    def test_any_significant_line_gap_breaks_match(self):
        result = {"null_families": {
            "document_shuffle": {"metrics": {
                "page_repeat_mass": self.fake_metric(1.2, True),
                "line_repeat_mass": self.fake_metric(1.4, True)}},
            "page_shuffle": {"metrics": {
                "line_repeat_mass": self.fake_metric(1.1, True)}},
            "line_shuffle": {"metrics": {
                "line_identity_gap1": self.fake_metric(0.5, True),
                "line_identity_gap2_4": self.fake_metric(1.0, False),
                "line_identity_gap5_16": self.fake_metric(1.0, False)}},
        }}
        self.assertFalse(evaluator.phenotype(result)["full_phenotype_match"])


if __name__ == "__main__":
    unittest.main()
