#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

import numpy as np

import latent_state as ls


def template(pages: int = 8, lines: int = 8, tokens: int = 8) -> list[dict]:
    result = []
    for p in range(pages):
        page_lines = []
        for line in range(lines):
            contexts = np.asarray([ls.visible_context(i, tokens) for i in range(tokens)],
                                  dtype=np.int16)
            page_lines.append({"line_id": f"p{p}-l{line}", "contexts": contexts,
                               "symbols": np.zeros(tokens, dtype=np.int16)})
        result.append({"page": f"p{p}", "lines": page_lines})
    return result


class LatentStateTests(unittest.TestCase):
    def test_context_bounds(self):
        values = {ls.visible_context(i, n) for n in range(1, 25) for i in range(n)}
        self.assertGreater(len(values), 4)
        self.assertGreaterEqual(min(values), 0)
        self.assertLess(max(values), ls.CONTEXTS)

    def test_zero_state_generator_is_deterministic(self):
        base = np.full((ls.CONTEXTS, ls.VOCABULARY), 1 / ls.VOCABULARY)
        first = ls.simulated_pages(template(), base, np.random.default_rng(44), False)
        second = ls.simulated_pages(template(), base, np.random.default_rng(44), False)
        for p1, p2 in zip(first, second):
            for l1, l2 in zip(p1["lines"], p2["lines"]):
                np.testing.assert_array_equal(l1["symbols"], l2["symbols"])
                self.assertEqual(l1["true_state"], 0)

    def test_k1_probabilities_normalize(self):
        base = np.full((ls.CONTEXTS, ls.VOCABULARY), 1 / ls.VOCABULARY)
        pages = ls.simulated_pages(template(), base, np.random.default_rng(1), False)
        counts, _ = ls.line_count_matrices(pages)
        fitted = ls.fit_k1(counts)
        np.testing.assert_allclose(fitted.sum(axis=1), 1.0)

    def test_injected_state_is_detectable_on_fixture(self):
        base = np.full((ls.CONTEXTS, ls.VOCABULARY), 1 / ls.VOCABULARY)
        train = ls.simulated_pages(template(20, 10, 10), base,
                                   np.random.default_rng(10), True)
        validation = ls.simulated_pages(template(10, 10, 10), base,
                                        np.random.default_rng(11), True)
        score = ls.fit_and_score(train, validation)
        self.assertGreater(score["gain_bits_per_token"], 0.05)
        self.assertGreater(ls.viterbi_accuracy(validation, score["k2"]), 0.75)

    def test_bootstrap_is_deterministic(self):
        first = ls.bootstrap_gain([1.0, -0.5, 2.0], [10, 10, 20])
        second = ls.bootstrap_gain([1.0, -0.5, 2.0], [10, 10, 20])
        self.assertEqual(first, second)

    def test_calibration_hash_detects_mutation(self):
        value = {"schema": ls.SCHEMA_CALIBRATION, "calibration_passed": True,
                 "voynich_validation_authorized": True, "corpus_sha256": "x",
                 "final_test_used": False}
        value["calibration_sha256"] = ls.canonical_hash(value)
        corpus = {"corpus_sha256": "x"}
        ls.verify_calibration(value, corpus)
        changed = copy.deepcopy(value)
        changed["final_test_used"] = True
        with self.assertRaises(ValueError):
            ls.verify_calibration(changed, corpus)


if __name__ == "__main__":
    unittest.main()

