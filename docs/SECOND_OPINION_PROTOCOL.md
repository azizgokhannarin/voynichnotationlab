# Second-opinion protocol

A second model may be used as an adversarial reviewer, but it should not be told which
interpretation we prefer before it evaluates the evidence.

## Procedure

1. Freeze the table/result being reviewed.
2. Present observations and known confounds only.
3. Do **not** say which hypothesis originated the experiment.
4. Ask the reviewer to:
   - rank at least three explanations;
   - identify hidden confounds;
   - propose the strongest falsification test;
   - distinguish known facts from inference.
5. Record model name/version, date, exact prompt, and full response.
6. Do not merge the reviewer's interpretation into project conclusions automatically.

The purpose is not voting between models. It is to expose assumptions we may have missed.
