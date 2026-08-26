# Phase 20 cross-phase synthesis and identifiability audit

This phase fits no model and opens no final-test data. It hash-verifies the
frozen Phase 13–19 decision files, classifies each claim under the frozen audit
rubric, evaluates the prior four-part STOP rule and decides whether any bounded
next experiment is authorized.

Generate the matrix and decision:

```bash
python3 phase20_synthesis_audit/synthesize_evidence.py \
  --repo . \
  --manifest phase20_synthesis_audit/SOURCE_DECISION_MANIFEST_v1.json \
  --matrix-out phase20_synthesis_audit/CROSS_PHASE_EVIDENCE_MATRIX_v1.json \
  --decision-out phase20_synthesis_audit/IDENTIFIABILITY_STOP_DECISION_v1.json
```

Run `python3 test_synthesis_audit.py` from this directory. The audit may close
bounded subclasses but may not rank H_C, H_D or H_G.
