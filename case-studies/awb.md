# Recorded Audit Workbench installation case

Audit Workbench (AWB) is a repository-auditing application. Chapter 5 examines its `check-installation` capability within its installation-support package. The recorded use concerned AWB 0.2.7, method `awb-companion-v1`, built from unchanged source on Linux x86_64 with Node 24.19.0.

The actual CLI launched and probed the local UI on a temporary loopback port; no startup stub supplied its responses. Damage was confined to a disposable package copy and diagnostic state was isolated.

| Controlled case | Exit | Recorded result |
| --- | ---: | --- |
| Initial check | 0 | Installation and operation verified; first task false; unlicensed. |
| Required stylesheet removed from disposable copy | 2 | Assets failed; installation and operation no longer verified. |
| Stylesheet restored and session rechecked | 0 | Installation and operation recovered; first task still false. |
| Unused valid-format session ID requested | 2 | `SESSION_NOT_FOUND`. |
| First-task sample attempted without entitlement | 2 | Blocked; next action `START_TRIAL`; first task still false. |

No trial was activated, no audit ran, and no remote model call occurred. Local loopback HTTP probes did occur. The case demonstrates selected diagnostic behavior in one source-build environment, not archive authenticity, macOS qualification, audit correctness, field reliability, or measured support-cost reduction.

The application and its proprietary implementation are not included. Re-running AWB is not a prerequisite for the book’s independently runnable Python teaching exercise. Chapter 5 gives the commands, essential receipt fields, failure, recovery, and interpretation.

Copyright © 2026 Lynn Walker. All rights reserved. This case-study narrative is outside the teaching software’s MIT license.
