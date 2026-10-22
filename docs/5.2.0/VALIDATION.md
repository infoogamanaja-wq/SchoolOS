# SchoolOS 5.2.0 — validation evidence

Local PHP **8.4.24**, MariaDB **11.8.6** and **10.11.18**, Apache **2.4.68**/FastCGI and real headless Chromium. Disposable fixtures only; no production records or provider transactions.

Evidence is under [test-output](test-output/). Primary checks cover domain logic, HTTP role/access control, concurrent money operations, actual browser interactions, distribution manifests and actual frontend package upload/install/rollback/reinstall. Separate MariaDB 10.11 runs verify compatibility. PHP files are syntax checked independently.

| Suite | Assertions |
|---|---:|
| Experience domain / HTTP / concurrency / browser | 57 / 103 / 4 / 17 |
| Affiliate domain / concurrency / HTTP | 70 / 4 / 9 |
| Public website real browser, online guides and PDFs | 74 |
| Frontend two-stage package install / rollback / reinstall | 50 |
| Archive hashes, privacy, immutable history, modes, determinism | 25 |
| Learning domain / HTTP / concurrency | 131 / 55 / 4 |
| Operations domain / HTTP / concurrency | 128 / 90 / 6 |
| Parent/guardian domain | 61 |
| Update Manager atomicity and rollback | 27 |
| Services domain / HTTP / concurrency | 150 / 108 / 8 |
| Intelligence domain / HTTP / concurrency / offline JS | 115 / 78 / 7 / 14 |

Primary total: **1,395 assertions**. MariaDB 10.11 compatibility: **257 assertions** (Experience 57+4, affiliate 70+4, Intelligence 115+7). **56 PHP files** parse under PHP 8.4.24. These totals refer to local checks, not live hosting certification.

The package test starts from the immutable 5.1.0 artifacts, uploads the support ZIP and main ZIP through the real Super Admin UI, compares every deployed byte to its manifest, exercises public routes, module activation, configurable affiliate terms, dedicated partner signup, approval, referral attribution and school creation. It then restores the exact stable entry point/libraries, checks isolated demo sessions cannot authenticate into the restored application and reinstalls while preserving the new school/subscription.

The affiliate suite covers exact-payment evidence, payment replay, original-rate preservation, disabled/suspended states, unverified bank rejection, minimum and insufficient funds, recipient verification, payout permission, concurrent reservations/submission, timeout preservation, exact transfer evidence, failure release, duplicate/partial/full refunds, post-payout debt, both checkout paths, cross-affiliate privacy, expired/self-referrals, CSRF and test/live separation.

Browser checks exercise every public page and all 18 web/PDF guides, invalid document paths, snapshot selection, fact controls, quiz feedback, mobile menu/Escape, reduced motion, no horizontal overflow and no JS errors. Desktop and mobile screenshots are included. Existing role walkthrough, clock, themes, connected demo identities and school registration remain checked.
