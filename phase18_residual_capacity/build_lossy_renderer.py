#!/usr/bin/env python3
"""Build the preregistered aligned LatinISE heavy-suspension positive control."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path


SEED = 20260826
SCHEMA = "PHASE18_ALIGNED_LINE_CORPUS_v1"


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def suspended_token(word: tuple[str, ...], line_final: bool) -> str:
    """Extreme suspension: retain only the normalized onset and a generic mark."""
    token = f"{word[0].lower()}ꝰ"
    return token + "·" if line_final else token


def build(repo: Path, latinise: Path, voynich_path: Path, n_lines: int = 4200) -> dict:
    sys.path.insert(0, str(repo / "phase15_instrument_calibration"))
    import phase15_reproducibility as p15  # type: ignore

    words = p15.latinise_words(repo, latinise)
    if not words:
        raise ValueError("no selected LatinISE words")
    voynich = json.loads(voynich_path.read_text(encoding="utf-8"))
    if voynich.get("corpus_sha256") != "5fdf577932f21b6da59b7ae12f5bb5451d9bb5b574d81c1affd8b646364b9997":
        raise ValueError("unexpected frozen Voynich Phase-15 corpus")

    train_lengths = [len(r["tokens"]) for r in voynich["records"]
                     if r["split"] == "train" and r["tokens"]]
    rng = random.Random(SEED)
    layouts: list[int] = []
    while len(layouts) < n_lines:
        epoch = list(train_lengths)
        rng.shuffle(epoch)
        layouts.extend(epoch)
    layouts = layouts[:n_lines]

    line_ids = [f"line-{i:05d}" for i in range(n_lines)]
    split_map = p15.allocate_splits(line_ids, "phase18-lossy-renderer")
    records = []
    word_i = 0
    for line_i, line_length in enumerate(layouts):
        source_words = [words[(word_i + j) % len(words)] for j in range(line_length)]
        word_i += line_length
        tokens = [suspended_token(word, j + 1 == line_length)
                  for j, word in enumerate(source_words)]
        line_id = line_ids[line_i]
        records.append({
            "document": "LatinISE_heavy_suspension",
            "page": f"block-{line_i // 50:03d}",
            "order": line_i % 50,
            "line_id": line_id,
            "split": split_map[line_id],
            "tokens": tokens,
            "hidden_words": [".".join(word) for word in source_words],
            "hidden_onsets": [word[0] for word in source_words],
        })

    body = {
        "schema": SCHEMA,
        "name": "LATINISE_HEAVY_SUSPENSION_ALIGNED_v1",
        "source": {
            "hidden_content": "LatinISE v6 selected 1300-1500 sequence",
            "latinise_sha256": p15.EXPECTED["latinise_sha256"],
            "layout": "Voynich TRAIN plaintext-word line lengths; no Voynich token identities",
            "surface_lines": n_lines,
            "renderer": {
                "mapping": "first normalized source unit + generic suspension mark",
                "many_to_one": True,
                "surface_tokens_per_source_word": 1,
                "line_final_variant": "append middle dot to final surface token",
                "null_insertion": False,
            },
            "seed": SEED,
        },
        "records": records,
    }
    body["corpus_sha256"] = canonical_hash(body)
    return body


def counts(corpus: dict) -> dict:
    out = {}
    for split in ("train", "validation", "final_test"):
        records = [r for r in corpus["records"] if r["split"] == split]
        out[split] = {"lines": len(records),
                      "tokens": sum(len(r["tokens"]) for r in records)}
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--latinise", required=True)
    parser.add_argument("--voynich", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--lines", type=int, default=4200)
    args = parser.parse_args()
    corpus = build(Path(args.repo), Path(args.latinise), Path(args.voynich), args.lines)
    write_json(Path(args.out), corpus)
    print(json.dumps({"out": args.out, "corpus_sha256": corpus["corpus_sha256"],
                      "counts": counts(corpus)}, indent=2))


if __name__ == "__main__":
    main()

