# The Book an AI Can Use — Example code

Code and synthetic examples for Lynn Walker’s *The Book an AI Can Use: From Reading Information to Performing Reliable Work*, published by WinMedia.

## Start here

Use the `book-v1.0` branch for the first-edition examples. [Download the first-edition ZIP](https://github.com/lynnmedia/the-book-an-ai-can-use/archive/refs/heads/book-v1.0.zip) and extract it. You can also select `book-v1.0` using the branch selector, then choose **Code → Download ZIP**. The runnable example requires Python 3.10 or newer, using only its standard library. There is no dependency installation, model subscription, account, or network call.

From the extracted repository folder:

```sh
cd validator
cd fixtures/ordinary-a
python3 ../../validate.py task.json claims.json evidence.json
```

Expect two `SUPPORTED` results and exit 0. Then run a deliberate negative case:

```sh
cd ../conflicting-b
python3 ../../validate.py task.json claims.json evidence.json
```

Expect `FAILED` for tests, `SUPPORTED` for citations, and exit 1. The negative exit is intentional. In a POSIX shell, `echo $?` immediately after a command shows the exit status. In PowerShell use `$LASTEXITCODE`. If your Windows installation uses the Python launcher, replace `python3` with `py -3`.

Return to the validator directory and run all frozen cases:

```sh
cd ../..
python3 run_cases.py
```

Expect nine cases passed and both boundary observations true. The runner creates `validator/results/` with fresh outputs and runtime information. Work in a copy of the download when experimenting.

## What the code does

The validator classifies references to supplied evidence against expected task, check, artifact, version, and outcome. Read [the contract](validator/CONTRACT.md) and [invocation instructions](validator/INVOKE.md). It reads the three supplied JSON files and prints a report; it does not modify them or perform release actions.

`SUPPORTED` means all cited matching records report passed. It does not establish that the records are genuine, that all relevant evidence was selected, that tests ran, or that a release is authorized. Fabricated passes and uncited failures are deliberate boundary exercises, not authenticated real-world events.

## Files

- `validator/validate.py`: complete teaching implementation, runtime version 1.0.0.
- `validator/fixtures/`: nine frozen synthetic inputs.
- `validator/acceptance.json`: expected dispositions and exit codes.
- `validator/run_cases.py`: execution runner, entry-point parity, and two boundary observations.
- `case-studies/srow.md`: recorded instruction-directed rewrite, failure, and checker limit.
- `case-studies/awb.md`: recorded installation diagnostic and five outcomes.

The two case studies are documented examples. This repository does not distribute the AWB application, governed Machine Edition archives, private Book Factory records, or customer data. They are not required to run the validator. The renderer discussed in Chapter 7 remains a proposed design, not a supplied executable.

The book contains the explanations, essential inputs and outputs, and evidence limits. These files make execution convenient. They do not add a separate product or service.

Publisher: https://winmedia.com

## Rights

The repository owner supplied the root MIT license. It applies to the original teaching software, its contract/invocation documentation, and synthetic fixtures under `validator/`. The case-study narratives are Copyright © 2026 Lynn Walker, all rights reserved. The book, governed Machine Edition sources, and Audit Workbench application are not distributed or licensed by this repository.
