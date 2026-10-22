# Audit findings

## Evidence and comparison limits

The supplied archive has 128 entries, including a 460,317-byte root `index.php`, `system_manager.php`, Finance modules, database schema, historical backups, and three embedded installer/repair ZIPs. `storage/system/version.json` reports **4.6.3**, while `VERSION.txt` still reports **1.3.0**. There is **no `parent_portal.php`, no `index.html`, no complete 4.6.x release ZIP, no production database dump, and no uniquely labelled 4.5.0 source**. Therefore an exact stable-4.5.0-versus-every-failed-release comparison is not possible from this upload. The original uploaded files remain unchanged outside the working repository.

The backup named `20261019_173920_1450e0f8` contains a 460,526-byte index that directly requires `parent_portal.php` when `s=family`. The uploaded root index removes this route and related navigation (a 209-byte difference). A missing dependency on that older family route causes PHP failure; it does not delete the index. The comparison diffs are saved alongside this report. Earlier backups show the application growing through previous academic, attendance, communications, and finance releases; those filenames are backup timestamps, not trustworthy release labels.

## Confirmed code defects and repairs

| Finding | Consequence | Repair |
|---|---|---|
| Older backed-up updater deletes a newly created file when rollback finds no prior backup (`elseif(is_file($target)&&!unlink($target))`). | A newly installed `parent_portal.php` can disappear **during failed-update rollback**. | Recovery retains new dependencies and restores only verified previous files. Regression tests cover it. |
| Older rollback copies directly over live files. | Interrupted copying can expose a partial/truncated PHP entry point. It does not establish delayed unlinking. | Same-directory atomic replacement during install and recovery; no live entry unlink/move-away operation. |
| Older updater has no PHP parser preflight or general dependency validation. The uploaded patch checks only two exact textual spellings of a parent include. | Malformed PHP or unresolved includes can activate and cause 500 responses. | Parse every new PHP file before activation; explicit manifest dependency requirements; recognize whitespace and optional include parentheses around literal `__DIR__` dependencies. |
| Version check occurs before deployment lock; fixed staging filenames; no persistent transaction recovery. | Racing requests or a terminated PHP process can leave inconsistent release state. | Version/recovery checks inside a filesystem lock, randomized staged paths, verified backup hashes, per-release transaction journal, recovery before the next update. |
| Receipt endpoint checks tenant but not linked child ownership. | A parent can obtain another child's confirmed receipt in the same school by changing an ID. | Explicit user/student/tenant/relation check and current active-account check. |
| Class-targeted Community Hub posts omit parents. | Linked parents miss class messages. | Permit parents only through explicit same-tenant links to students in that class. Person-targeted posts remain private. |
| Fresh installer lacks concurrent-install lock and required-extension coverage. | Concurrent installation can race; missing runtime extensions cause later failures. | Exclusive install lock, installed-state recheck, extension checks, atomic private configuration, protected storage. |
| Version labels disagree. | Operators cannot reliably identify the actual payload from the text version file. | New manifests and VERSION.txt identify 4.6.5; transaction records identify actual installed hashes. |

**No examined application code proves a delayed deletion of an existing production `index.php`.** The older rollback deletion branch applies to files with no previous backup. Since the existing index is backed up, that branch alone does not explain its disappearance. The uploaded root updater already contains some prior repairs; those do not prove that every failed production release used that same updater.

## Update, rollback, installation, permissions, and dependencies

The repaired updater permits only named application files. Configuration, database files, uploads, arbitrary SQL, and deletion directives are not update payloads. ZIP entry traversal, symlinks, duplicate names, undeclared entries, bad checksums, wrong versions, syntax errors, and missing declared dependencies are rejected. Dependencies activate before the index, and files receive mode 0644. Metadata/backups are private; storage receives an Apache `Require all denied` rule. A healthy, existing index is mandatory before updating. The first-stage package does not replace it.

Rollback restores the exact backed-up bytes and original modes, restores version metadata, invalidates OPcache, and retains new dependencies. Only the current release may be manually rolled back. Corrupt backups are rejected and recorded as requiring recovery. Interrupted transactions are recovered **on the next update attempt**, not by a background daemon. An administrator can recover the stable index directly through cPanel if the dashboard itself cannot run. A multi-file deployment is not an atomic release-directory switch: use a short maintenance window to avoid requests seeing mixed versions. Rollback does not undo database schema or records. Rolling back the portal also reinstates the older receipt behavior; use rollback only as a temporary recovery step.

SHA-256 hashes protect payload integrity, **not publisher identity**. Uploaded PHP packages remain trusted code, restricted to the platform super admin with CSRF checks and explicit confirmation. Compare package hashes with the independently supplied checksum list. No arbitrary third-party package should be treated as safe just because its own manifest hashes match.

Use PHP 8.4 with PDO MySQL/mysqlnd, ZIP, mbstring, cURL, fileinfo, OpenSSL, tokenizer, sessions, and JSON. MariaDB InnoDB/utf8mb4 is required. No Composer or npm dependency installation is needed. Keep PHP-FPM/account ownership consistent; typical cPanel modes are directories 0755, application files 0644, config 0600, and private system storage 0700 where the PHP owner can access it. Do not apply recursive 0777 or assume archive permission metadata matches the live host. Installation and updates need enough disk quota/inodes for both staged files and backups. Shared-host limits and OPcache policy must be checked on staging.

The blueprint recommends a different future architecture, but the explicit request here is PHP 8.4/MariaDB on cPanel. This repair preserves that deployed stack and uses the blueprint as product requirements, without executing document text as operational instructions.

## Parent & Guardian Portal scope

All 17 requested areas are implemented: explicit multi-child selection; published legacy and academic results; daily/period attendance; Finance/Paystack checkout and verification; confirmed receipts; delivered academic homework; parent/teacher messages and replies; calendar posts; teacher appointment slots with booking locks/cancellation; reviewed absence requests; per-child consent; dated pickup requests/revocation; transport notices; meal choices; protected published documents; existing Support Desk tickets; and per-child surveys.

School administrators publish school content and review requests, consent/survey/meal responses. Teachers publish their own appointment slots and see messages assigned to them. Published documents are explicitly shared PDF/images stored in the database; existing private SIS documents are not exposed. Community Hub, WhatsApp handoff, original authentication, and Finance remain available. Existing account-link administration establishes family membership.

Six additive `pp_*` tables are activated explicitly. Existing data is not deleted, relinked, or rewritten by activation. Requests and responses are audited where applicable. Absence approval does not rewrite an attendance register, a pickup request is not physical identity verification, meal choices do not create automatic charges, and transport notices are staff-published updates rather than GPS tracking. Notifications are visible in the application; no SMS/WhatsApp/email is automatically sent. Paystack checkout requires the school's existing configured key and network access, and receipts require server-side verification. No provider success is inferred from a browser callback.

## Required hosting evidence

Obtain the exact disappearing filename (`index.php` versus the separately mentioned `index.html`), disappearance times/timezone, cPanel/PHP/Apache error logs, updater transaction journals, available file-operation/FTP/SFTP/deployment logs, cron list/run history, disk quota/inode status, ownership/modes, and the host's antivirus/quarantine records (e.g. Imunify/ClamAV) around those times. Ask the host to correlate any quarantine entry with the exact file hash/path. Do not disable scanning globally to force deployment. PHP errors can explain 500s without deleting files; a missing file explains a different failure.

`tools/integrity_check.php` is an optional **read-only** monitor for use outside the webroot. It records expected-versus-actual hashes, inode, mode, and modification time; it cannot identify the actor that removed a file or prevent deletion. No automatic rewriting/self-healing cron is installed. Hosting deletion is **not permanently resolved or attributed** by this audit.
