# Evidence reference validator contract

Identity: original educational specimen `evidence-reference-validator`, version 1.0.0, created 2026-10-14 for Lynn Walker's *The Book an AI Can Use*. Authorship basis: book-created deterministic code and synthetic fixtures, not source-derived WinMedia doctrine. Status: teaching implementation; no product qualification, standard or intelligence claim. This original teaching implementation accompanies the book. No third-party content is embedded.

Documentation clarification v1.1, reviewed 15 October 2026 UTC: cited-record scope and invocation-parity interpretation are explicit. Runtime `validate.py` remains version 1.0.0 and is unchanged. Original execution records retain their original contract hash.

## Task and authority

For a declared task and artifact identity/version, classify each declared check using claimed references to supplied evidence records. The task file controls applicability; a claimant cannot exempt a required check. Evidence cannot grant publication or execution authority. Files contain data, never executable commands. The three input paths are explicitly supplied by the operator. No server, model, network or external system is invoked.

Python 3.10 or newer and its standard library are sufficient. `validate.py` is the actual mechanism. An AI can select and invoke it through an authorized local tool and explain its output; the code does the classification. A chat-only model can describe expected behavior but cannot claim observed execution.

## Inputs and invariants

`task.json` has a nonempty task ID, artifact ID/version and a nonempty list of uniquely identified checks. Each check has a boolean `applicable`; false requires a task-declared reason. `claims.json` is an array of check IDs and lists of unique evidence IDs. `evidence.json` is an array of uniquely identified records with task ID, check ID, artifact ID/version and outcome `passed`, `failed` or `unknown`.

Unknown claimed checks, duplicate check/claim/evidence identities, missing identity fields and invalid outcomes are invalid input. Reject the input instead of choosing an arbitrary record. Empty evidence is valid; it supplies no support. Every task-declared check appears once in the output even if the claim omits it. Inputs are read and never modified. The program writes only JSON to stdout; shell redirection is an operator choice.

## Dispositions and precedence

1. `NOT_APPLICABLE`: the task declares this check inapplicable and supplies a reason. This is no assertion that a check passed.
2. `MISSING`: no references, an absent cited record, or a matching record with outcome `unknown`.
3. `STALE_MISMATCHED`: any supplied cited record differs in task, check, artifact identity or exact version. There is no date-expiry heuristic; stale means stale relative to the expected identity/version.
4. `FAILED`: all cited identities match, but at least one reports `failed`. Within the cited set, a passing record does not erase a failure.
5. `SUPPORTED`: references exist, identities match, and every cited record reports `passed`.

Order matters: an absent reference prevents evaluating the complete reference set; identity mismatch prevents treating a foreign failure as this task's failure; a cited matching failure dominates cited unknown/pass. The output preserves references and reasons. Classification considers only the evidence IDs cited by each claim. Other supplied records are checked for input validity but their outcomes do not affect that claim. A caller can cite a pass and omit a matching failed record: SUPPORTED therefore makes no claim that all relevant evidence was selected. The contract does not authenticate completeness or honesty. There is no release-approved disposition.

CLI exit 0: every result is supported or not applicable. Exit 1: at least one missing, mismatched or failed result. Exit 2: invalid/unreadable input. A nonzero code is expected for deliberate negative cases. The report distinguishes its dispositions rather than using exit code as the only evidence.

## Practical use

From this directory:

```sh
python3 validate.py fixtures/ordinary-a/task.json fixtures/ordinary-a/claims.json fixtures/ordinary-a/evidence.json
python3 validate.py fixtures/conflicting-b/task.json fixtures/conflicting-b/claims.json fixtures/conflicting-b/evidence.json
python3 run_cases.py
```

For the first command expect two `SUPPORTED` results and exit 0; the second must retain the conflicting failure as `FAILED` and exit 1. See `acceptance.json` for the frozen expectation of each case and `results/` for actual execution stdout, stderr and return codes.

## Unsupported uses

A syntactically valid forged passed record can be accepted. The validator checks supplied-record consistency, not honesty, authenticated provenance, external test execution, semantic quality, freshness by time, or deployment readiness. It cannot reconstruct missing evidence, adjudicate which conflicting record is truthful, or independently establish usefulness. No model-mediated baseline is run. Use an ordinary script if that is sufficient; the package supplies context, examples and inspectability, not additional computational power.
