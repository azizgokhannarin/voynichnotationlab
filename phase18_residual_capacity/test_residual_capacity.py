#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

import build_lossy_renderer as renderer
import residual_capacity as capacity


def fixture(pattern: bool, n_train: int = 160, n_validation: int = 40) -> dict:
    records = []
    for i in range(n_train + n_validation + 20):
        split = "train" if i < n_train else ("validation" if i < n_train + n_validation
                                               else "final_test")
        if pattern:
            tokens = ["a", "b", "a", "b"]
        else:
            tokens = [["a", "b", "c", "d"][(i * 7 + j * 3) % 4] for j in range(4)]
        records.append({"document": "D", "page": f"P{i // 4:03d}", "order": i % 4,
                        "line_id": f"L{i:03d}", "split": split, "tokens": tokens})
    body = {"schema": "fixture", "name": "fixture", "source": {}, "records": records}
    body["corpus_sha256"] = capacity.canonical_hash(body)
    return body


class ResidualCapacityTests(unittest.TestCase):
    def test_canonical_hash_detects_mutation(self):
        corpus = fixture(True)
        capacity.verify_corpus_hash(corpus)
        changed = copy.deepcopy(corpus)
        changed["records"][0]["tokens"][0] = "x"
        with self.assertRaises(ValueError):
            capacity.verify_corpus_hash(changed)

    def test_internal_selection_is_deterministic(self):
        records = capacity.split_records(fixture(True), "train")
        first = capacity.internal_train_split(records)
        second = capacity.internal_train_split(list(reversed(records)))
        self.assertEqual({r["line_id"] for r in first[0]}, {r["line_id"] for r in second[0]})
        self.assertEqual({r["line_id"] for r in first[1]}, {r["line_id"] for r in second[1]})

    def test_deterministic_surface_has_low_residual_capacity(self):
        result = capacity.analyze(fixture(True), "deterministic")
        self.assertLess(result["residual_capacity"]["bits_per_token"], 1.0)
        self.assertFalse(result["final_test_used"])

    def test_oov_spelling_code_is_finite_and_charged(self):
        records = capacity.split_records(fixture(True), "train")
        model = capacity.SurfaceCode("UNIGRAM_OPEN").fit(records)
        bits, escaped = model.token_bits(["unseen-token"], 0)
        self.assertTrue(escaped)
        self.assertGreater(bits, 1.0)
        self.assertTrue(bits < float("inf"))

    def test_suspension_is_many_to_one_and_line_sensitive(self):
        self.assertEqual(renderer.suspended_token(("A", "B"), False), "aꝰ")
        self.assertEqual(renderer.suspended_token(("A", "Z"), False), "aꝰ")
        self.assertEqual(renderer.suspended_token(("A", "B"), True), "aꝰ·")

    def test_edit_distance_one_excludes_identity(self):
        self.assertTrue(capacity.edit_distance_one("aꝰ", "bꝰ"))
        self.assertFalse(capacity.edit_distance_one("aꝰ", "aꝰ"))


if __name__ == "__main__":
    unittest.main()

