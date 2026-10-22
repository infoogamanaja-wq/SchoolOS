# Validation — Platform Experience 5.1.0

Executed locally on **22 October 2026**, using **PHP 8.4.24**, **MariaDB 11.8.6 and 10.11.18**, **Apache 2.4.68/FastCGI**, Node WebCrypto and headless Chromium/Playwright. Fixtures are fictional. No production school, live payment, real message recipient or actual hosting logs were accessed.

| Executed suite | Passed assertions | Evidence under test-output/ |
|---|---:|---|
| New Experience domain: repeated additive activation, school creation, configured prices/trials, no-orphan/replay checks, payment verification/expiry/free renewal, approval/recovery/temporary credentials, role and school boundaries, demo provisioning/refresh/isolation and missing-key protection | 57 | experience.txt |
| HTTP: public pages, login, role overviews, all simplified owner navigation, setup, CSRF, initial password change, fourteen demo roles, connected attendance, existing demo workspaces, external/host/permission guards and source protection | 103 | http.txt |
| Actual Chromium interactions: insights/pause, demo autofill, password visibility, native walkthrough/replay/progress, live WAT clock, theme, mobile overflow and configured plan summary/unavailable cycle | 17 | browser.txt |
| Concurrent subscription verification and member approval | 4 | concurrency.txt |
| Actual frontend two-stage install on 5.0.0, exact deployed hashes, activation, configured plan/signup, isolated demo provisioning/login, exact file rollback, demo session-ID replay protection and persisted-school reinstall | 35 | package-apache.txt |
| Apache homepage/rewrite/private paths and authenticated Family routing | 9 | apache-routing.txt |
| ZIP source/hash/dependency/privacy/mode checks, historical immutability and deterministic rebuild | 23 | release-integrity.txt |
| Learning domain / HTTP / concurrency regressions | 131 / 55 / 4 | regression/learning-*.txt |
| HR/Transport/Boarding domain / HTTP / concurrency regressions | 128 / 90 / 6 | regression/operations-*.txt |
| Family domain regression | 61 | regression/family-domain.txt |
| Update Manager path/hash/parsing/dependency/failure recovery/rollback tests | 27 | regression/updater.txt |
| Library/Inventory/Engagement/CMS domain / HTTP / concurrency regressions | 150 / 108 / 8 | services-regression/*.txt |
| Intelligence domain / HTTP / concurrency / offline WebCrypto regressions | 115 / 78 / 7 / 14 | intelligence-regression/*.txt |
| MariaDB 10.11 Experience domain / concurrency | 57 / 4 | maria10-experience*.txt |
| MariaDB 10.11 Intelligence domain / repeated wallet/offline concurrency | 115 / 7 | intelligence-regression/maria10-*.txt |
| PHP syntax | 50 source files | syntax.txt |

**1,230 primary assertions** and **183 separately counted MariaDB 10.11 assertions** passed. PHP and JavaScript parsing are additional checks. The actual demo-maintenance CLI also completed successfully (`demo-refresh-cli.txt`). All listed checks ran; empty reset logs represent successful commands with no output, and seed logs identify the engines used.

## Browser review artifacts

- [Login, desktop](test-output/login-desktop.png)
- [School-owner overview, desktop](test-output/school-owner-desktop.png)
- [Guided onboarding, desktop](test-output/onboarding-desktop.png)
- [School-owner overview, dark](test-output/school-owner-dark.png)
- [School-owner overview, mobile width](test-output/school-owner-mobile.png)
- [Parent overview, mobile width](test-output/parent-mobile.png)
- [Registration, mobile width](test-output/registration-mobile.png)

Screenshots contain fictional accounts only. Browser tests assert no page JavaScript errors and no horizontal overflow at a 390-pixel viewport. They exercise real controls rather than only checking static HTML. They are not physical-device, exhaustive accessibility or large-school performance certification.

## Reproduction

Use the existing cloud checkout and private toolchain; never run fixture scripts against a live database. The new domain fixture requires a fresh disposable main database ending `_test` and its separately created empty `schoolos_experience_test_demo` sandbox. Run `seed.php`, `learning_seed.php`, `operations_seed.php`, `services_seed.php`, then `experience.php`, followed by `experience_concurrency.php`. Set `SCHOOLOS_ALLOW_TEST_FIXTURES=1`, `SCHOOLOS_TEST_DSN`, username and password explicitly. The fixture refuses inappropriate/populated main databases; demo provisioning refuses a populated sandbox.

For the second MariaDB instance, use its own DSN **and PHP default PDO MySQL socket**, including child processes, so demo provisioning also reaches that instance. HTTP/browser tests require a matching local runtime clone and a copy of the synthetic private credential key. The browser suite is `tests/experience_browser.py`; local Chromium/Playwright are test-only dependencies. The package suite requires a fresh isolated Apache document root with the historical 5.0.0 source and separate fixture database. Its demo provisioning database is also synthetic and empty before the test.

See `tests/README.md` for commands. Historical suites run against separate freshly seeded fixture databases. Source extraction in the PHP test harness now resolves `__DIR__` to the actual application directory, matching runtime storage behavior rather than accidentally placing keys below the test folder.

## Findings and limits

A duplicate-row lock-upgrade issue surfaced in existing prepaid concurrency tests and was fixed with an account write-lock upsert; repeated retries pass on both database versions. The legacy Community Hub regression remains intact. New demo sessions use separate server storage as well as cookies; the actual old index was tested against a replayed demo session ID after rollback and did not authenticate it.

An unlinked learner now signs into a helpful overview; its protected Learning route still returns 403. That deliberate UX change updates the login expectation in the retained Learning HTTP test while preserving its authorization assertion.

Provider tests use injected responses; no live Paystack charge, settlement, mail, WhatsApp, push, AI or real DNS ownership was verified. Signup/approval does not certify school ownership or child relationships; administrators must perform the stated verification. Temporary credentials are distributed through the school's secure process, not fictitious email automation. Demo resets replace shared fictional changes and may briefly interrupt demos; unexpected tables stop a reset before deletion. Rollback restores files and retains records, not business events.

Production cPanel PHP configuration, real mobile devices, accessibility needs, provider accounts, actual subscription contracts, capacity policy and operational/legal/privacy review still need staging acceptance. No evidence establishes that a hosting process can never remove an entry point.
