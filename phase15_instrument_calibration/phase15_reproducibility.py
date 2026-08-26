#!/usr/bin/env python3
"""Executable Phase-15 controls frozen after v4.4.

The original transient Phase-15 script was not archived.  This file is therefore an explicit,
versioned reproduction implementation, not a claim of byte-for-byte recovery of that script.
All learned objects are fit on TRAIN only; all reported predictive scores use VALIDATION only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mutual_info_score

SEED = 20260826
SCHEMA = "PHASE15_LINE_CORPUS_v2"
INSTRUMENT_SCHEMA = "PHASE15_EXECUTABLE_INSTRUMENT_v2"
CLUSTERS = 12
MIN_TYPE_COUNT = 4
CONTEXT_VOCAB = 64
SHUFFLES = 200
ALPHA = 0.5

INCLUDED_CREMMA_DIRS = (
    "Arras-861", "BGO-511", "BIS-193", "Latin6395", "Latin8236",
    "LaurentianusPluteus33.31", "LaurentianusPluteus39.34",
    "LaurentianusPluteus53.08", "LaurentianusPluteus53.09", "Mazarine915",
    "PalLat373", "Phi_10a135", "SBB_PK_Hdschr25", "UBL758",
)

EXPECTED = {
    "rf1b_sha256": "e7d3238e35743e06c63367a933909ec37b1e2de7ada3a1b449447eafa1918782",
    "latinise_sha256": "74553e781f8b0fc43b5a35d76d315932f5323ae9cfd9903f3cc69c8fcd494388",
    "cremma_commit": "e681b1077cddafebb51018a19cce503431139e4f",
    "cremma_xml_files": 90,
    "cremma_lines": 4422,
    "cremma_content_manifest": "e27810f6bd0e0039ff5a30adedb8ab895f9eb77a1773288db188fdb9618e5e79",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def stable_u64(text: str) -> int:
    return int.from_bytes(hashlib.sha256(text.encode("utf-8")).digest()[:8], "big")


def canonical_hash(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8")


def allocate_splits(items: list[str], salt: str) -> dict[str, str]:
    """Deterministic 60/20/20 allocation, with all three splits for n >= 3."""
    order = sorted(items, key=lambda x: (stable_u64(f"{SEED}:{salt}:{x}"), x))
    n = len(order)
    if n >= 3:
        n_train = max(1, int(round(0.60 * n)))
        n_val = max(1, int(round(0.20 * n)))
        if n_train + n_val >= n:
            n_train = n - 2
            n_val = 1
    elif n == 2:
        n_train, n_val = 1, 1
    else:
        n_train, n_val = n, 0
    out = {}
    for i, item in enumerate(order):
        out[item] = "train" if i < n_train else ("validation" if i < n_train + n_val
                                                   else "final_test")
    return out


def corpus_payload(name: str, source: dict, records: list[dict]) -> dict:
    records = sorted(records, key=lambda r: (r["document"], r["page"], r["order"], r["line_id"]))
    body = {"schema": SCHEMA, "name": name, "source": source, "records": records}
    body["corpus_sha256"] = canonical_hash(body)
    return body


def corpus_counts(corpus: dict) -> dict:
    by_split = defaultdict(lambda: Counter())
    manuscripts = defaultdict(set)
    pages = defaultdict(set)
    for r in corpus["records"]:
        s = r["split"]
        by_split[s]["lines"] += 1
        by_split[s]["tokens"] += len(r["tokens"])
        manuscripts[s].add(r["document"])
        pages[s].add((r["document"], r["page"]))
    return {s: {"lines": c["lines"], "tokens": c["tokens"],
                "manuscripts": len(manuscripts[s]), "pages": len(pages[s])}
            for s, c in sorted(by_split.items())}


def verify_git_commit(root: Path, expected: str) -> None:
    if not (root / ".git").exists():
        return
    actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"],
                                     text=True).strip()
    if actual != expected:
        raise ValueError(f"CREMMA commit mismatch: expected {expected}, got {actual}")


def cremma_content_manifest(root: Path, files: list[Path]) -> str:
    rows = [f"{sha256_file(p)}  {p.relative_to(root).as_posix()}" for p in files]
    raw = ("\n".join(sorted(rows)) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def build_cremma(root: Path) -> dict:
    verify_git_commit(root, EXPECTED["cremma_commit"])
    files = []
    split_map = {}
    for document in INCLUDED_CREMMA_DIRS:
        rels = [p.relative_to(root).as_posix() for p in sorted((root / "data" / document).glob("*.xml"))]
        if not rels:
            raise ValueError(f"missing CREMMA manuscript directory: {document}")
        split_map.update({(document, rel): split for rel, split in
                          allocate_splits(rels, document).items()})
        files.extend(root / rel for rel in rels)
    if len(files) != EXPECTED["cremma_xml_files"]:
        raise ValueError(f"CREMMA XML count mismatch: {len(files)}")
    manifest = cremma_content_manifest(root, files)
    if manifest != EXPECTED["cremma_content_manifest"]:
        raise ValueError(f"CREMMA content manifest mismatch: {manifest}")

    records = []
    for path in sorted(files):
        rel = path.relative_to(root).as_posix()
        document = path.parent.name
        split = split_map[(document, rel)]
        xml_root = ET.parse(path).getroot()
        order = 0
        for node in xml_root.iter():
            if not node.tag.endswith("TextLine"):
                continue
            text = []
            for child in node.iter():
                if child.tag.endswith("String"):
                    value = (child.attrib.get("CONTENT") or "").strip()
                    if value:
                        text.append(value)
            if not text:
                continue
            joined = " ".join(text)
            tokens = joined.split()
            if not tokens:
                continue
            records.append({"document": document, "page": rel, "order": order,
                            "line_id": node.attrib.get("ID", f"line-{order}"),
                            "split": split, "tokens": tokens})
            order += 1
    if len(records) != EXPECTED["cremma_lines"]:
        raise ValueError(f"CREMMA non-empty line mismatch: {len(records)}")
    source = {"repository": "https://github.com/HTR-United/CREMMA-Medieval-LAT",
              "tag": "0.1.0", "commit": EXPECTED["cremma_commit"],
              "selected_content_manifest_sha256": manifest,
              "manuscripts": list(INCLUDED_CREMMA_DIRS), "xml_files": len(files)}
    return corpus_payload("CREMMA_1300_1499_FULLSIZE_v1", source, records)


def build_voynich(repo: Path, rf1b: Path) -> dict:
    if sha256_file(rf1b) != EXPECTED["rf1b_sha256"]:
        raise ValueError("RF1b SHA-256 mismatch")
    search = repo / "phase5" / "search"
    sys.path.insert(0, str(search))
    from build_c1_structural_stream import parse_rf1b  # type: ignore
    stream, _ = parse_rf1b(rf1b, repo / "phase5" / "voynich_page_split_manifest.csv")
    records = []
    for page in stream:
        for order, line in enumerate(page["lines"]):
            records.append({"document": "Voynich_RF1b", "page": page["page"], "order": order,
                            "line_id": line["line"], "split": page["split"],
                            "tokens": [t["surface"] for t in line["tokens"]]})
    source = {"url": "https://www.voynich.nu/data/RF1b-e.txt",
              "sha256": EXPECTED["rf1b_sha256"], "representation": "C1-STRUCT-v1 split"}
    return corpus_payload("VOYNICH_RF1B_FROZEN_v1", source, records)


WORD = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žẞßŒœÆæſ]+(?:['’\-][A-Za-zÀ-ÖØ-öø-ÿĀ-žẞßŒœÆæſ]+)*")


def latin_doc_selected(attrs: dict[str, str]) -> bool:
    date = attrs.get("date", "")
    years = [int(x) for x in re.findall(r"(?<!\d)(1[1-6]\d{2})(?!\d)", date)]
    if years:
        return max(years) >= 1300 and min(years) <= 1500
    cents = [int(x) for x in re.findall(r"(?:cent\.\s*)?(1[3-6])",
                                        attrs.get("century", ""), re.I)]
    return bool(cents and min(cents) >= 14 and max(cents) <= 15)


def latinise_words(repo: Path, path: Path) -> list[tuple[str, ...]]:
    if sha256_file(path) != EXPECTED["latinise_sha256"]:
        raise ValueError("LatinISE SHA-256 mismatch")
    sys.path.insert(0, str(repo / "phase5" / "search"))
    from historical_normalizers import normalize  # type: ignore
    words = []
    keep = False
    with path.open(encoding="utf-8", errors="ignore") as stream:
        for line in stream:
            line = line.rstrip("\n")
            if line.startswith("<doc"):
                attrs = dict(re.findall(r'(\w+)="([^"]*)"', line))
                keep = latin_doc_selected(attrs)
            elif line.startswith("</doc"):
                keep = False
            elif keep and line and not line.startswith("<"):
                token = line.split("\t", 1)[0].strip()
                if WORD.fullmatch(token):
                    units = normalize(token, "LAT")
                    if units:
                        words.append(tuple(units))
    return words


def split_units(word: tuple[str, ...]) -> list[tuple[str, ...]]:
    if len(word) < 3:
        return [word]
    midpoint = len(word) / 2
    candidates = list(range(1, len(word)))
    vowels = {"A", "E", "I", "O", "U"}
    candidates.sort(key=lambda i: (0 if word[i - 1] in vowels else 1,
                                   abs(i - midpoint), i))
    cut = candidates[0]
    return [word[:cut], word[cut:]]


def build_strong_renderer(repo: Path, latinise: Path, voynich: dict,
                          n_lines: int = 4200) -> dict:
    words = latinise_words(repo, latinise)
    if not words:
        raise ValueError("no selected LatinISE words")
    freq = Counter(words)
    n_nom = max(1, math.ceil(0.08 * len(freq)))
    nomenclators = {w for w, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n_nom]}

    train_lengths = [len(r["tokens"]) for r in voynich["records"]
                     if r["split"] == "train" and r["tokens"]]
    rng = random.Random(SEED)
    layouts = []
    while len(layouts) < n_lines:
        epoch = list(train_lengths)
        rng.shuffle(epoch)
        layouts.extend(epoch)
    layouts = layouts[:n_lines]

    chunk_inventory = set()
    for w in words:
        if w not in nomenclators:
            chunk_inventory.update(split_units(w))
    chunk_code = {c: f"C{i:05d}" for i, c in enumerate(sorted(chunk_inventory))}
    nom_code = {w: f"N{i:05d}" for i, w in enumerate(sorted(nomenclators))}

    def surface(base: str, key: str, occurrence: int) -> str:
        variants = 1 + stable_u64(f"variants:{key}") % 3
        which = stable_u64(f"{SEED}:{occurrence}:{key}") % variants
        return f"{base}v{which}"

    records = []
    word_i = 0
    occurrence = 0
    split_for_line = allocate_splits([f"line-{i:05d}" for i in range(n_lines)], "renderer")
    for line_i, plain_length in enumerate(layouts):
        rendered = []
        for _ in range(plain_length):
            word = words[word_i % len(words)]
            word_i += 1
            if word in nomenclators:
                units = [(nom_code[word], "N:" + ".".join(word))]
            else:
                units = [(chunk_code[c], "C:" + ".".join(c)) for c in split_units(word)]
            for base, key in units:
                rendered.append(surface(base, key, occurrence))
                occurrence += 1
                if rng.random() < 0.20:
                    rendered.append(f"NULL{rng.randrange(4)}")
        if rendered:
            rendered[-1] += "_LF"
        line_id = f"line-{line_i:05d}"
        records.append({"document": "LatinISE_strong_renderer", "page": f"block-{line_i // 50:03d}",
                        "order": line_i % 50, "line_id": line_id,
                        "split": split_for_line[line_id], "tokens": rendered})
    source = {"hidden_content": "LatinISE v6 selected 1300-1500 sequence",
              "latinise_sha256": EXPECTED["latinise_sha256"], "surface_lines": n_lines,
              "renderer": {"nomenclator_top_type_fraction": 0.08,
                           "chunks": "one or two deterministic phonographic chunks",
                           "homophony": "one to three deterministic forms per content chunk",
                           "null_probability_after_content_chunk": 0.20,
                           "null_types": 4, "line_final_variant": True,
                           "layout": "Voynich TRAIN plaintext-word line lengths"},
              "seed": SEED}
    return corpus_payload("LATINISE_STRONG_RENDERER_REPRO_v2", source, records)


class FrozenClasses:
    def __init__(self):
        self.mapping: dict[str, str] = {}
        self.context_vocabulary: list[str] = []
        self.frequent_types: list[str] = []

    def fit(self, records: list[dict]) -> "FrozenClasses":
        counts = Counter(t for r in records for t in r["tokens"])
        self.frequent_types = sorted(t for t, n in counts.items() if n >= MIN_TYPE_COUNT)
        context = [t for t, _ in counts.most_common(CONTEXT_VOCAB)]
        self.context_vocabulary = context
        if len(self.frequent_types) < 2:
            raise ValueError("too few frequent types to induce classes")
        idx = {t: i for i, t in enumerate(context)}
        width = 2 * (len(context) + 3)
        rows = {t: np.zeros(width, dtype=float) for t in self.frequent_types}
        frequent = set(self.frequent_types)
        for r in records:
            toks = r["tokens"]
            for i, tok in enumerate(toks):
                if tok not in frequent:
                    continue
                left = "<BOS>" if i == 0 else toks[i - 1]
                right = "<EOS>" if i + 1 == len(toks) else toks[i + 1]
                li = idx.get(left, len(context) + (0 if left == "<BOS>" else 2))
                ri = idx.get(right, len(context) + (1 if right == "<EOS>" else 2))
                rows[tok][li] += 1
                rows[tok][len(context) + 3 + ri] += 1
        matrix = np.vstack([rows[t] for t in self.frequent_types])
        sums = matrix.sum(axis=1, keepdims=True)
        matrix = matrix / np.maximum(sums, 1)
        norms = np.linalg.norm(matrix, axis=1, keepdims=True)
        matrix = matrix / np.maximum(norms, 1e-12)
        k = min(CLUSTERS, len(self.frequent_types))
        labels = KMeans(n_clusters=k, random_state=SEED, n_init=20).fit_predict(matrix)
        self.mapping = {t: f"C{int(label):02d}" for t, label in zip(self.frequent_types, labels)}
        return self

    def transform(self, token: str) -> str:
        return self.mapping.get(token, "RARE")


def split_records(corpus: dict, split: str) -> list[dict]:
    return [r for r in corpus["records"] if r["split"] == split]


def class_lines(records: list[dict], frozen: FrozenClasses) -> list[list[str]]:
    return [[frozen.transform(t) for t in r["tokens"]] for r in records if r["tokens"]]


def mi_at_lag(lines: list[list[str]], lag: int) -> float:
    left, right = [], []
    for line in lines:
        if len(line) > lag:
            left.extend(line[:-lag])
            right.extend(line[lag:])
    return float(mutual_info_score(left, right)) if left else float("nan")


def class_order(lines: list[list[str]]) -> dict:
    observed = [mi_at_lag(lines, lag) for lag in range(1, 6)]
    rng = np.random.default_rng(SEED)
    null = np.zeros((SHUFFLES, 5), dtype=float)
    arrays = [np.asarray(x, dtype=object) for x in lines]
    for rep in range(SHUFFLES):
        shuffled = [rng.permutation(x).tolist() for x in arrays]
        null[rep] = [mi_at_lag(shuffled, lag) for lag in range(1, 6)]
    mean = null.mean(axis=0)
    sd = null.std(axis=0, ddof=1)
    z = (np.asarray(observed) - mean) / np.maximum(sd, 1e-15)
    return {"observed_mi": observed, "shuffle_mean": mean.tolist(),
            "shuffle_sd": sd.tolist(), "shuffle_z": z.tolist(), "shuffles": SHUFFLES}


def pos_bucket(i: int, n: int) -> str:
    return str(min(4, int(5 * i / max(1, n))))


def line_len_bucket(n: int) -> str:
    return "S" if n <= 5 else ("M" if n <= 10 else ("L" if n <= 15 else "XL"))


def token_len_bucket(n: int) -> str:
    return "1-2" if n <= 2 else ("3-4" if n <= 4 else ("5-6" if n <= 6 else "7+"))


def sample_rows(records: list[dict], frozen: FrozenClasses, mode: str,
                skip_line_start: bool = False) -> tuple[list[dict], list[str]]:
    X, y = [], []
    carry_key = None
    continuous: list[str] = []
    for r in records:
        key = (r["document"], r["page"])
        if key != carry_key:
            continuous = []
            carry_key = key
        toks = r["tokens"]
        cls = [frozen.transform(t) for t in toks]
        for i, target in enumerate(cls):
            if skip_line_start and i == 0:
                continuous.append(target)
                continuous = continuous[-4:]
                continue
            line_prev = lambda lag: cls[i - lag] if i >= lag else f"<BOS{lag}>"
            cont_prev = lambda lag: continuous[-lag] if len(continuous) >= lag else f"<DOCBOS{lag}>"
            position = {"line_start": str(i == 0), "pos": pos_bucket(i, len(cls)),
                        "line_len": line_len_bucket(len(cls))}
            continuous_f = {"cont_prev1": cont_prev(1), "cont_prev2": cont_prev(2),
                            "cont_prev3": cont_prev(3)}
            local = dict(position)
            local.update({"line_prev1": line_prev(1),
                          "prev_tok_len": token_len_bucket(len(toks[i - 1])) if i else "BOS",
                          "prev_first": toks[i - 1][0] if i and toks[i - 1] else "BOS",
                          "prev_last": toks[i - 1][-1] if i and toks[i - 1] else "BOS"})
            if mode == "position": features = position
            elif mode == "continuous": features = continuous_f
            elif mode == "local": features = local
            elif mode == "hybrid":
                features = dict(local); features.update(continuous_f)
                features.update({"line_prev2": line_prev(2), "line_prev3": line_prev(3)})
            elif mode == "distant_local": features = local
            elif mode == "distant":
                features = dict(local)
                features.update({"line_prev2": line_prev(2), "line_prev3": line_prev(3),
                                 "line_prev4": line_prev(4)})
            else: raise ValueError(mode)
            X.append({f"{k}={v}": 1.0 for k, v in features.items()})
            y.append(target)
            continuous.append(target)
            continuous = continuous[-4:]
        # line starts skipped above still need the remaining classes in continuous order.
        if skip_line_start and len(cls) == 1:
            pass
    return X, y


def fit_model(train: list[dict], validation: list[dict], frozen: FrozenClasses,
              mode: str, skip_line_start: bool = False) -> dict:
    Xtr, ytr = sample_rows(train, frozen, mode, skip_line_start)
    Xv, yv = sample_rows(validation, frozen, mode, skip_line_start)
    vectorizer = DictVectorizer(sparse=True)
    A = vectorizer.fit_transform(Xtr)
    B = vectorizer.transform(Xv)
    model = LogisticRegression(solver="lbfgs", C=1.0, max_iter=1000, random_state=SEED)
    model.fit(A, ytr)
    prob = model.predict_proba(B)
    class_index = {c: i for i, c in enumerate(model.classes_)}
    ptrue = np.array([prob[i, class_index[y]] if y in class_index else 1e-15
                      for i, y in enumerate(yv)])
    bits = float(np.mean(-np.log2(np.clip(ptrue, 1e-15, 1.0))))
    pred = model.classes_[np.argmax(prob, axis=1)]
    return {"bits_per_token": bits, "accuracy": float(np.mean(pred == np.asarray(yv))),
            "validation_samples": len(yv), "encoded_feature_count": len(vectorizer.feature_names_),
            "coefficient_count": int(model.coef_.size)}


def distribution(first_counts: Counter, conditional: dict[str, Counter], key: str,
                 target: str, classes: list[str]) -> float:
    counts = conditional.get(key, Counter())
    return (counts[target] + ALPHA) / (sum(counts.values()) + ALPHA * len(classes))


def line_reset(train: list[dict], validation: list[dict], frozen: FrozenClasses) -> dict:
    classes = sorted(set(frozen.mapping.values()) | {"RARE"})
    first = Counter()
    conditional = defaultdict(Counter)
    for records in (train,):
        previous = None; key = None
        for r in records:
            current_key = (r["document"], r["page"])
            cls = [frozen.transform(t) for t in r["tokens"]]
            if not cls: continue
            first[cls[0]] += 1
            if previous is not None and current_key == key:
                conditional[previous][cls[0]] += 1
            previous, key = cls[-1], current_key
    total_first = sum(first.values())
    reset_losses, cond_losses, deltas = [], [], []
    previous = None; key = None
    for r in validation:
        current_key = (r["document"], r["page"])
        cls = [frozen.transform(t) for t in r["tokens"]]
        if not cls: continue
        if previous is not None and current_key == key:
            target = cls[0]
            p0 = (first[target] + ALPHA) / (total_first + ALPHA * len(classes))
            p1 = distribution(first, conditional, previous, target, classes)
            l0, l1 = -math.log2(p0), -math.log2(p1)
            reset_losses.append(l0); cond_losses.append(l1); deltas.append(l0 - l1)
        previous, key = cls[-1], current_key
    rng = np.random.default_rng(SEED)
    arr = np.asarray(deltas)
    means = [float(np.mean(rng.choice(arr, size=len(arr), replace=True))) for _ in range(2000)]
    return {"validation_same_page_line_starts": len(arr),
            "reset_prior_bits_per_start": float(np.mean(reset_losses)),
            "previous_line_conditioned_bits_per_start": float(np.mean(cond_losses)),
            "cross_line_gain_bits_per_start": float(np.mean(arr)),
            "bootstrap_gain_ci95": [float(np.quantile(means, 0.025)),
                                    float(np.quantile(means, 0.975))]}


def run_instrument(corpus: dict) -> dict:
    train = split_records(corpus, "train")
    validation = split_records(corpus, "validation")
    if not train or not validation:
        raise ValueError("TRAIN and VALIDATION are required")
    frozen = FrozenClasses().fit(train)
    order = class_order(class_lines(validation, frozen))
    models = {name: fit_model(train, validation, frozen, mode)
              for name, mode in (("POSITION", "position"), ("CONTINUOUS", "continuous"),
                                 ("LINE_LOCAL", "local"), ("HYBRID", "hybrid"))}
    local = fit_model(train, validation, frozen, "distant_local", skip_line_start=True)
    distant = fit_model(train, validation, frozen, "distant", skip_line_start=True)
    counts = corpus_counts(corpus)
    val = counts.get("validation", {})
    fullsize_gate = {"train_plus_validation_lines_at_least_3000":
                     counts.get("train", {}).get("lines", 0) + val.get("lines", 0) >= 3000,
                     "validation_tokens_at_least_5000": val.get("tokens", 0) >= 5000,
                     "validation_lines_at_least_500": val.get("lines", 0) >= 500,
                     "train_validation_manuscripts_at_least_8":
                     len({r["document"] for r in train + validation}) >= 8}
    return {"schema": INSTRUMENT_SCHEMA, "seed": SEED, "corpus": corpus["name"],
            "corpus_sha256": corpus["corpus_sha256"], "counts": counts,
            "fullsize_power_gate": {"checks": fullsize_gate, "pass": all(fullsize_gate.values())},
            "class_induction": {"clusters_requested": CLUSTERS,
                                "frequent_type_count": len(frozen.frequent_types),
                                "mapped_class_count": len(set(frozen.mapping.values())) + 1,
                                "minimum_type_count": MIN_TYPE_COUNT,
                                "context_vocabulary": CONTEXT_VOCAB},
            "class_order": order, "line_reset": line_reset(train, validation, frozen),
            "distant_context": {"local": local, "local_plus_lags_2_4": distant,
                                "gain_bits_per_token": local["bits_per_token"] - distant["bits_per_token"]},
            "model_competition": {"models": models,
                                  "line_local_minus_continuous_gain_bits_per_token":
                                  models["CONTINUOUS"]["bits_per_token"] - models["LINE_LOCAL"]["bits_per_token"],
                                  "hybrid_minus_line_local_gain_bits_per_token":
                                  models["LINE_LOCAL"]["bits_per_token"] - models["HYBRID"]["bits_per_token"]},
            "interpretation_lock": "Descriptor only; no H_C/H_D/H_G ranking is permitted."}


def command_build(args) -> None:
    repo = Path(args.repo).resolve()
    out = Path(args.out)
    if args.kind == "voynich": corpus = build_voynich(repo, Path(args.source))
    elif args.kind == "cremma": corpus = build_cremma(Path(args.source))
    else:
        if not args.voynich_corpus:
            raise ValueError("--voynich-corpus is required for strong-renderer")
        voynich = json.loads(Path(args.voynich_corpus).read_text(encoding="utf-8"))
        corpus = build_strong_renderer(repo, Path(args.source), voynich)
    write_json(out, corpus)
    print(json.dumps({"out": str(out), "corpus_sha256": corpus["corpus_sha256"],
                      "counts": corpus_counts(corpus)}, indent=2))


def command_analyze(args) -> None:
    corpus = json.loads(Path(args.corpus).read_text(encoding="utf-8"))
    expected = corpus.pop("corpus_sha256")
    actual = canonical_hash(corpus)
    corpus["corpus_sha256"] = expected
    if actual != expected:
        raise ValueError(f"corpus canonical hash mismatch: {actual} != {expected}")
    result = run_instrument(corpus)
    write_json(Path(args.out), result)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("kind", choices=("voynich", "cremma", "strong-renderer"))
    build.add_argument("--repo", required=True)
    build.add_argument("--source", required=True)
    build.add_argument("--voynich-corpus")
    build.add_argument("--out", required=True)
    build.set_defaults(func=command_build)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("--corpus", required=True)
    analyze.add_argument("--out", required=True)
    analyze.set_defaults(func=command_analyze)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
