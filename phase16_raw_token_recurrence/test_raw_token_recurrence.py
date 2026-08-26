#!/usr/bin/env python3
from __future__ import annotations

import json
import random
import unittest

import raw_token_recurrence as instrument


def fixture() -> dict:
    records = [
        {"document": "d", "page": "p1", "order": 0, "line_id": "l1",
         "split": "validation", "tokens": ["A", "a", "á", "á"]},
        {"document": "d", "page": "p1", "order": 1, "line_id": "l2",
         "split": "validation", "tokens": ["x", "x", "y"]},
        {"document": "d", "page": "p2", "order": 0, "line_id": "l3",
         "split": "validation", "tokens": ["x", "z", "x", "z"]},
        {"document": "d", "page": "sealed", "order": 0, "line_id": "l4",
         "split": "final_test", "tokens": ["SECRET"]},
    ]
    body = {"schema": "PHASE15_LINE_CORPUS_v2", "name": "fixture",
            "source": {"kind": "test"}, "records": records}
    body["corpus_sha256"] = instrument.canonical_hash(body)
    return body


class RawTokenInstrumentTests(unittest.TestCase):
    def test_exact_identity_is_not_normalized(self):
        layout = instrument.Layout(instrument.validation_records(fixture()))
        self.assertEqual(layout.vocabulary_size, 7)

    def test_final_test_is_not_loaded(self):
        records = instrument.validation_records(fixture())
        self.assertEqual({r["page"] for r in records}, {"p1", "p2"})
        self.assertNotIn("SECRET", {t for r in records for t in r["tokens"]})

    def test_nulls_preserve_line_lengths_and_document_marginals(self):
        layout = instrument.Layout(instrument.validation_records(fixture()))
        original = sorted(t for line in layout.lines for t in line)
        lengths = list(map(len, layout.lines))
        for family in instrument.VARYING:
            shuffled = instrument.shuffled_lines(layout, family, random.Random(123))
            self.assertEqual(list(map(len, shuffled)), lengths)
            self.assertEqual(sorted(t for line in shuffled for t in line), original)

    def test_nested_null_invariants(self):
        layout = instrument.Layout(instrument.validation_records(fixture()))
        observed = instrument.metric_vector(layout, layout.lines)
        page = instrument.metric_vector(
            layout, instrument.shuffled_lines(layout, "page_shuffle", random.Random(9)))
        line = instrument.metric_vector(
            layout, instrument.shuffled_lines(layout, "line_shuffle", random.Random(9)))
        for name in ("page_repeat_mass", "page_pair_concentration",
                     "page_frequency_fano", "page_return_gap1", "page_return_gap2_4"):
            self.assertEqual(observed[name], page[name])
        for name in ("page_repeat_mass", "line_repeat_mass",
                     "page_pair_concentration", "line_pair_concentration",
                     "page_frequency_fano", "line_frequency_fano",
                     "page_return_gap1", "page_return_gap2_4"):
            self.assertEqual(observed[name], line[name])

    def test_seed_stream_has_prefix_property(self):
        seed = instrument.stable_u64(f"{instrument.SEED}:fixture:document_shuffle")
        a = random.Random(seed)
        b = random.Random(seed)
        self.assertEqual([a.random() for _ in range(1000)],
                         [b.random() for _ in range(1000)])
        self.assertEqual(a.random(), b.random())

    def test_erratum_resolves_holm_floor(self):
        self.assertGreaterEqual(len(instrument.METRICS) / 1001, 0.01)
        self.assertLess(len(instrument.METRICS) / 2001, 0.01)

    def test_json_roundtrip_keeps_decomposed_unicode(self):
        corpus = fixture()
        again = json.loads(json.dumps(corpus, ensure_ascii=False))
        token = again["records"][0]["tokens"][3]
        self.assertEqual(token, "á")
        self.assertNotEqual(token, "á")


if __name__ == "__main__":
    unittest.main()
