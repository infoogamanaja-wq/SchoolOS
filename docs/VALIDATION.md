# Validation evidence — 22 October 2026

All tests ran on isolated application copies and synthetic databases. No production server/database was accessed or changed. All 80 files extracted from the uploaded archive remain byte-for-byte identical to the upload (see INPUT_EVIDENCE.json).

Runtime: **PHP 8.4.24**, **MariaDB 11.8.6**, **Apache 2.4.68 with PHP 8.4 FastCGI**. The database-backed portal and parallel booking suites also passed on a separately initialized **MariaDB 10.11.18** instance. Both databases used private Unix sockets with TCP networking disabled. Dependencies were obtained through signed Debian repositories with package checksum/TLS verification retained; no verification was disabled.

| Check | Outcome |
|---|---|
| PHP syntax, application/helpers/PHP tests | 14 files passed |
| Update engine | 24 assertions passed |
| Portal, database schema and integrations, MariaDB 11.8 | 61 assertions passed |
| Two simultaneous booking workers, separate connections | 1 assertion passed; one reservation, one rejection |
| HTTP fresh installation, authentication, routes, all portal views and access restrictions | 49 assertions passed |
| Actual ZIP uploads through original updater → repaired updater → portal; manual rollback and reinstall, under Apache/FastCGI | 13 assertions passed |
| Apache DirectoryIndex, rewrite, protected paths, direct module and authenticated parent route | 9 assertions passed |
| Additional full-source .htaccess ZIP denial | 1 assertion passed; HTTP 403 |
| Read-only integrity monitor | 4 assertions passed, including missing index and changed portal detection |
| MariaDB 10.11 portal/integration suite | 61 assertions passed |
| MariaDB 10.11 parallel booking workers | 1 assertion passed |
| Final ZIP contents, SHA-256 manifests, private-file exclusions | Passed for both packages |
| Full release integrity monitor against installed files | Passed |

There were **162 passing automated assertions on the primary runtime**, plus PHP lint and archive checks. The MariaDB 10.11 runs repeat 62 database/concurrency assertions on that second server version. No suite was skipped or treated as passing with zero tests. Raw per-suite output is in `docs/test-output/`.

Updater checks cover invalid PHP, required module absence, traversal, symlinks, payload tampering, forbidden config changes, undeclared payload, injected activation failure, verified rollback, entry preservation, safe modes, downgrade/same-version rejection, a held deployment lock, manual rollback, simulated interrupted transaction recovery, private storage protection, and corrupt-backup rejection. The injected failure simulates the failure path; it does not emulate every possible disk/quota/process failure on shared hosting.

Portal checks exercise multiple children, unrelated/foreign child denial, idempotent activation, CSRF, every view, draft-result exclusion, academic homework, absence review without attendance rewriting, dated pickup review/revocation, teacher replies, Support Desk integration, child-specific responses, survey deadlines, meal options, slot overlap/conflicts, class Community Hub audience, private posts, invoice scoping, confirmed receipt access, server-verification amount mismatch, successful/idempotent payment posting through existing Finance functions, disabled accounts, and preservation of synthetic legacy student/authentication/invoice rows.

The package test uploads the two exact generated ZIPs through multipart forms as Platform Super Admin. It verifies first-stage index equality, all second-stage manifest hashes, unchanged configuration, integrated homework, current-release rollback to the exact previous entry point, continued homepage operation, retained parent module, and successful reinstallation. New source and a fresh installer were also exercised separately.

## Limits of this validation

- **Exact 4.5.0 and failed 4.6.x release comparison remains incomplete:** those labelled complete packages were not supplied. Comparison used the uploaded root application and its embedded backups, with this limit stated in AUDIT.md.
- **Production/cPanel-host-specific behavior was not tested:** no host access/logs were provided. A real restored staging database, actual ownership/quotas, host PHP limits, caching, cron and antivirus/quarantine behavior still need observation.
- **Delayed external deletion is not proven fixed or attributed.** No server file-operation or quarantine logs were available. Local tests show repaired code paths and preserved files, not permanent hosting behavior.
- **Paystack HTTP traffic was simulated at the provider boundary.** The suite rejects mismatched provider data and exercises real database payment/ledger posting, including repeat verification. A live provider test transaction using the school's own staging key and network remains required. No real funds were moved.
- Local schema compatibility was tested on MariaDB 10.11 and 11.8; older versions, existing custom schema variations, production-sized datasets and browser visual/accessibility acceptance were not exhaustively tested.
- No automatic WhatsApp, email or SMS delivery, GPS tracking, automatic meal billing, or physical pickup identity verification is claimed.

The two update packages are locally validated, installable **staging candidates**. Complete the staging/observation steps in DEPLOYMENT.md before replacing the stable production entry point.
