# SchoolOS 5.3.0 — validation evidence

Validation used PHP **8.4.24**, MariaDB **11.8.6** and **10.11.18**, local Apache/PHP-CGI and real Chromium. All databases and accounts were disposable, fictional fixtures. Nothing here was run against the user's production cPanel account.

| Suite | Passed checks | Evidence |
|---|---:|---|
| Portal workflows, permissions, results and receipts | 58 | `test-output/portal-domain.txt` |
| Concurrent chat retries, guardian meal choices and classroom capacity | 5 | `test-output/portal-concurrency.txt` |
| HTTP conversation isolation, CSRF, role routing and PDF downloads | 21 | `test-output/portal-http.txt` |
| Real-browser portal interactions, WebRTC reception, dark mode and mobile | 33 | `test-output/portal-browser.txt` |
| Actual two-stage frontend installation, demo migration, rollback and reinstall | 41 | `test-output/package-http.txt` |
| Artifact hashes, previous archives, permissions, dependencies and deterministic rebuild | 53 | `test-output/release.txt` |
| Existing Experience activation, registration, accounts and demo isolation | 57 | `test-output/experience.txt` |
| Existing Experience HTTP routes and demo restrictions | 105 | `test-output/experience-http.txt` |
| Affiliate domain / concurrency | 70 / 4 | `test-output/affiliate-domain.txt`, `affiliate-concurrency.txt` |
| Learning domain / HTTP / concurrency | 131 / 55 / 4 | `test-output/regression/learning-*.txt` |
| HR, transport and boarding domain / HTTP / concurrency | 128 / 90 / 6 | `test-output/regression/operations-*.txt` |
| Family domain / updater safety | 61 / 27 | `test-output/regression/family-domain.txt`, `updater.txt` |
| Library, inventory, engagement and CMS domain / HTTP / concurrency | 150 / 108 / 8 | `test-output/services-regression`, `services-http.txt` |
| Intelligence domain / HTTP / concurrency / offline JavaScript | 115 / 81 / 7 / 14 | `test-output/intelligence-regression` |
| MariaDB 10.11 Experience / concurrent registration / portal / concurrent portal | 57 / 4 / 58 / 5 | `test-output/maria10-*.txt` |

The PHP syntax sweep parsed **61** application/test/tool PHP files, excluding private configuration and storage; new JavaScript files also passed `node --check`. See `test-output/php-syntax.txt`. No new PHP extension dependency was added beyond the existing application requirements.

## Specific evidence and fixes

- Package testing begins with actual historical 5.2.1 source overlaid into a disposable Apache root. It provisions the old isolated demo and books an appointment before uploading either ZIP. Installation verifies all 23 main-file hashes. The next demo connection adds CA/exam results, daily meals, connected chat and receipt branding while retaining that booking.
- Rollback restores exact prior files, preserves private configuration, Finance view, wallet and affiliate source, and serves the stable homepage. Reinstallation retains migrated data. Historical ZIP checksums are pinned to commit `7f71fef`; all 15 previous archives remain unchanged.
- Concurrency tests caught and fixed a rate-bucket shared-lock deadlock and a message retry snapshot conflict. The final rate insertion obtains an exclusive row lock; message insertion and retry verification serialize on the conversation. Distinct messages remain distinct; one retry key returns one message ID. Concurrent guardian choices retain one row per child/day, and concurrent final-seat joins retain the eight-person cap.
- Browser tests exchange actual parent/learner messages without reload, test escaped markup, save bookings/absence/pickup/meal choices with success feedback, select administrator and teacher together, expand event details, verify Reservations highlighting and receive actual teacher video frames at the learner. Teacher broadcast controls are hidden for learners.
- Media testing used a **loopback-only coturn fixture** with synthetic authentication. Chromium's managed network policy required a relay even locally. The receiving browser reported a real video track and nonzero video width; this is stronger than testing signaling alone. Production TURN, TLS, real-provider credentials, bandwidth and cross-network acceptance still require deployment-specific validation. Zoom/Meet checks validate invitation handling; no provider API account was available or provisioned.
- `contrast.json` records zero failures across 16 tested dark routes. The automated calculation covers visible text with resolvable solid backgrounds; it excludes ambiguous gradient/translucent surfaces. Screenshots provide additional visual evidence. This is not a full WCAG certification or proof for every custom theme.

## Preserved behavior and limits

Existing finance records, confirmed-payment access controls, invoices/journals, Community Hub, WhatsApp integration code, authentication, affiliate ledger, smart pickup and wallet remain. Automated provider tests use simulated responses; no real payment, WhatsApp send, affiliate transfer or production notification was performed.

An existing demo must already be configured as a verified separate database for automatic migration. Unknown sandbox tables fail closed. Explicit demo refresh replaces fictional visitor changes by design; live school records are never seeded or cleared. Live workspace activation is additive and file rollback does not drop its tables.

Chat uses visible-page polling, not a deployed WebSocket service. Built-in lessons are eight-person teacher broadcasts, not unlimited multi-party conferencing or a fully provisioned video platform. The existing CBT, assignments, resources, grading and offline teacher system remain the LMS foundation; this release organizes them and adds live delivery.

No hosting-side file deletion is attributed or declared permanently resolved without server evidence. The installed updater's path allowlist, syntax/dependency checks, verified staging, entry-point-last replacement and exact rollback remain tested safeguards. Review real cPanel/access/antivirus logs if a disappearance recurs.
