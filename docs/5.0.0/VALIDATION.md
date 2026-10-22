# Validation — School Intelligence 5.0.0

Executed locally on 2026-10-22 with **PHP 8.4.24**, **MariaDB 11.8.6 and 10.11.18**, **Node 24.19.0**, and **Apache 2.4.68 / FastCGI**. All school/account/payment/provider data are synthetic. No production cPanel, server logs, live payment, real recipient or live AI account was accessed.

| Executed suite | Passed assertions | Evidence under test-output/ |
|---|---:|---|
| Intelligence domain: all fixed report SQL, permissions, scheduled exports, retention, forecasts, Copilot scope/approval/quota, signed WhatsApp/STOP, pickup, offline replay/conflicts/published protection, CA/exam reports, curricula, timetable, wallet journals, scholarships, rights, accreditation, HQ consent and plugin scopes | 115 | intelligence.txt |
| HTTP manager/family/teacher/student screens, scoped exports/cards/JSON endpoints, CSRF, static offline shell, direct PHP source guards and actual CLI worker | 78 | http.txt |
| Parallel wallet funding, insufficient-balance purchases, duplicate references and offline edits | 4 | concurrency.txt |
| Offline encryption roundtrip, fresh IV/salt, no plaintext storage, wrong passphrase, tamper failure, queue coalescing and conflict retention | 14 | offline-js.txt |
| Actual frontend 4.9.0 → support → 5.0.0 install, explicit activation, all manager views, nested static deployment, independent plugin review, real Apache API header/scope, exact stable-index rollback, Family preservation and persisted-record reinstall | 47 | package-apache.txt |
| Apache homepage/rewrite/private storage/config/archives and authenticated Family routing | 9 | apache-routing.txt |
| ZIP manifest/source/digest/dependency/privacy/mode checks, immutable historical archives and deterministic rebuild | 21 | release-integrity.txt |
| Learning domain / HTTP / concurrency regression | 131 / 55 / 4 | regression/learning-*.txt |
| HR/Transport/Boarding domain / HTTP / concurrency regression | 128 / 90 / 6 | regression/operations-*.txt |
| Family domain regression | 61 | regression/family-domain.txt |
| Updater failure injection, parsing/dependency/hash/path/symlink/permission guards, interrupted recovery, rollback and approved static subdirectory | 27 | regression/updater.txt |
| Library/Inventory/Engagement/CMS domain / HTTP / concurrency regression | 150 / 108 / 8 | services-regression/*.txt |
| Second-version MariaDB Intelligence domain / concurrency | 115 / 4 | maria10-intelligence*.txt |
| PHP parse checks, application/test/tool sources | 43 files | syntax.txt |

Primary suites total **1,056 assertions**. MariaDB 10.11 adds **119 assertions**, separately counted. PHP syntax and JavaScript parsing are additional checks. All listed checks ran. Reset logs may be empty because successful database creation commands produce no output; seed logs confirm the databases and versions used.

## Defects found and corrected during validation

The updater initially rejected a previously absent offline directory. It now permits only the explicit `public/offline` destination, creates it after payload validation, and still rejects unsafe ancestors/symlinks. Frontend package installation and rollback exercised the correction.

MariaDB 10.11 concurrency exposed missing-event gap locks in offline synchronization. Synchronization now serializes each teacher's event processing with an account row lock, avoids the missing-key gap lock, and retains record-version conflict detection. Both database versions pass the concurrent-edit test.

A new WhatsApp campaign must keep the original authorized communications creator, rather than its approval-only reviewer; signed callback tests exercise this ownership. Exact integer-kobo journal tests distinguish prepaid liability release from an external cash receipt. Package tests exercise a cPanel-compatible explicit secret header for FastCGI installations that strip Authorization.

## Reproduction and limits

Use a fresh disposable `_test` database. Run `tests/seed.php`, `learning_seed.php`, `operations_seed.php`, `services_seed.php`, then `intelligence.php`, using `SCHOOLOS_ALLOW_TEST_FIXTURES=1`, `SCHOOLOS_TEST_DSN`, user and password as described in `tests/README.md`. Run concurrency afterward on that same fixture. These seeds intentionally reject populated/inappropriate databases. For compatibility change only the DSN socket to the independent MariaDB 10.11 instance and reseed a new disposable database. HTTP suites need a matching synthetic runtime clone and logged-in fixture users; package tests need an isolated Apache root populated with the historical 4.9.0 payload and a fresh fixture database.

Mocks validate exact provider payload/response handling and quota/privacy rules; they do not prove a real account, Meta approval, Paystack settlement, WhatsApp delivery or model availability. Browser crypto was executed using Node WebCrypto; actual Android PWA installation, IndexedDB/service-worker behavior, offline reconnection and visual/accessibility acceptance remain device/staging checks. Timetable tests cover bounded feasibility, approval, changed-input rejection and once-only application, not global optimization or a large school's performance benchmark.

Rollback restores files and preserves additive records; it does not reverse post-install business events. Tests cannot establish whether a hosting cron, antivirus, backup tool or file-manager user will later delete an entry point. Production server logs remain necessary to investigate that independently. NDPA alignment controls and financial-provider workflows are not legal/regulatory certification.
