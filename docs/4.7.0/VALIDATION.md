# Validation — Teacher & Student Portals 4.7.0

Tested locally on **PHP 8.4.24**, **MariaDB 11.8.6** and **Apache 2.4.68 / PHP FastCGI**. Database-backed learning and concurrency suites also passed on a separate **MariaDB 10.11.18** server. Databases used private Unix sockets; no production host, database, funds or AI provider account was used.

| Suite | Result |
|---|---|
| Teacher/Student domain, permissions, state transitions and simulated AI | 131 assertions passed |
| HTTP routes, all 31 areas, legacy-form restrictions and real file uploads | 55 assertions passed |
| Parallel CBT start, library issue, club approval and AI quota | 4 independent-worker checks passed |
| Actual ZIP installation, explicit activation, all views, rollback and reinstall under Apache | 44 assertions passed |
| Update engine safety regression | 24 assertions passed |
| Existing Family Space / Finance integration regression | 61 assertions passed |
| Read-only integrity monitor, old/new release baselines | 6 assertions passed |
| PHP syntax | 18 application/helper/test PHP files passed |
| MariaDB 10.11 learning suite | 131 assertions passed |
| MariaDB 10.11 concurrency suite | 4 checks passed |
| ZIP entry membership, hashes and private-file exclusions | Both new packages passed |

Primary runtime: **325 passing assertions/checks**, plus PHP syntax and archive validation. Second MariaDB version: **135 repeated learning/concurrency checks**. No check was skipped or substituted with a zero-test result. Raw outputs are stored in `docs/4.7.0/test-output/`. Historical 4.6.4/4.6.5 ZIP hashes remain unchanged.

## What was exercised

- Canonical `ecosystem_links` identity for CBT/LMS; parent identity rejected as a student; unlinked/ambiguous access denied; active-account and revoked-allocation checks.
- Teacher class, subject and current-session bounds, including same-school unrelated classes and another tenant. Teacher and student views exclude unrelated/private/draft/future content.
- Attendance into the existing register; lesson/homework and syllabus updates into Academics; course creation/publication and assignment visibility, deadlines and graded-work locks.
- Teacher question-bank creation and authoring, denial of another teacher's bank and published-bank changes; no answer explanation leaked in student exam rendering.
- Score CSV parsing, range/duplicate/class validation, all-or-nothing transaction rollback, submit/approve protection, administrator-reviewed corrections and immutable publication locks.
- Parent messaging into existing Family Space records, parent/child relationship checks, resource URL validation, confidential incident reporting, leave and professional-development review, private study planning and existing LMS badges.
- Club eligibility/capacity and library issue/return state transitions, including repeat-issue/return rejection and foreign-book denial. Parallel workers enforce last-copy and last-place constraints.
- CBT class/window/publication/code/ownership/attempt checks, resume, saved answers, objective scoring, immutable submission and parallel-start serialization.
- Simulated AI disabled/default/missing-key states, redaction without school-record transmission, prompt/output moderation, fail-closed moderation handling, risk/cheating refusal, active-exam blocking, daily quota and concurrent quota reservation. External provider calls were mocked; real school account availability, billing and actual model response quality were not tested.
- Real HTTP multipart CSV preview and confirmation, valid protected homework attachments, owner download and unrelated-student denial. Legacy LMS resubmission cannot erase a grade; teacher/student legacy Welfare POSTs cannot bypass the new scoped workflow.
- Frontend install starting at the immutable working 4.6.5 release. The 4.6.6 support package leaves index.php byte-for-byte unchanged. The 4.7.0 package matches its manifest, preserves existing Family/Finance/config bytes, requires explicit school-admin schema activation, and serves all portal views under Apache. Rollback restores the exact known working 4.6.5 entry point, retains both modules, keeps the homepage/Family Space available, and allows reinstall with retained additive tables.
- Synthetic student records, authentication hashes, Finance invoice records and Family posts remain unchanged by the learning suite except for the explicitly exercised legitimate workflow writes. No real school database was available for a production-sized migration test.

## Publication and deployment limits

These ZIPs are tested, installable **staging candidates** for the working 4.6.5 baseline. Production installation remains an operator action through cPanel/the frontend updater. Follow DEPLOYMENT.md, restore a real staging database, check actual PHP extensions/ownership/quota and verify the school's allocations and student links before production deployment.

Live AI requires the school's own private provider key, outbound HTTPS and explicit school enablement. AI safeguard layers reduce risk; they are not a guarantee that every sensitive prompt or model error will be caught. Results, drafts and AI output still need human review as described in the feature guide.

No new claim is made about permanent prevention of host-driven deletion/quarantine. The previously repaired atomic replacement, verified backups, persistent recovery journal and retention of new dependencies remain in place. Runtime monitoring is read-only and now recognises learning_portal.php when declared by the installed release manifest.

Large production datasets, custom schema variants, browser-specific visual/accessibility acceptance and every possible hosting/network/process failure were not exhaustively tested. All observed selected-suite failures were diagnosed and corrected before the final passing run; test-harness corrections did not weaken application assertions.
