# cPanel deployment and recovery

These packages were validated locally; they have not been installed on your production account. The complete failed v4.6.x packages, exact v4.5.0 source, production logs, and a production-like database are still needed for the remaining comparison and hosting investigation. Do not test installation against the only production database.

## Prepare a staging clone

1. Use cPanel Backup/Backup Wizard or the host's supported backup tool to export the live database and archive the complete current webroot. Keep verified recoverable copies **outside public_html** and download a copy. Preserve `config.php`, any `.env`, uploads, storage, and account-specific `.htaccess` rules. Save the stable production `index.php` separately, with its SHA-256. Do not replace it yet.
2. Create a separate staging document root, database, and database user. Restore the application's real schema/data into this database using cPanel tools; retain the original charset/collation. Configure the staging copy's `config.php` to point only to that database. Protect staging from public access. Disable production cron jobs, outbound messaging, and live payment credentials in staging; use the provider's test mode.
3. Select PHP 8.4 for this staging domain in cPanel MultiPHP Manager/Select PHP Version. Enable the extensions listed in AUDIT.md. Confirm PHP runs as the owning account, storage is writable, and sufficient disk quota/inodes remain for backups. Never use 0777.
4. Confirm staging `/index.php`, `/index.php?login=1`, school admin Finance, and Community Hub work **before any update**. If the live/staging index is missing or depends on a missing parent module, restore the operator-verified stable index first through cPanel File Manager. Do not substitute one of the unlabelled backup indexes based only on its timestamp.
5. Compare the two ZIP hashes with `dist/SHA256SUMS`. The manifest must be at the ZIP root; do not repackage it inside a `public_html/` directory.

## Install in two stages through the frontend

1. Sign in to staging as **Platform Super Admin → Updates & Plugins**. Upload `SchoolOS-4.6.4-Updater-Repair.zip` and confirm its trusted source. This package contains only `system_manager.php` plus `release.json`. It is intended for the uploaded 4.6.3 state or an older version; do not edit version metadata to bypass a newer installed version. Refresh the page after success. Verify the installed version and check that the stable `index.php` hash has not changed.
2. Start a short maintenance window, then upload `SchoolOS-4.6.5-Family-Portal.zip`. It contains `index.php`, `parent_portal.php`, `system_manager.php`, `finance_engine.php`, and `VERSION.txt`. It deliberately contains **no config, SQL dump, uploads, user data, installer, deletion rules, or .htaccess replacement**. It checks for existing Finance view and logo handler dependencies. Do not manually extract only index.php.
3. Sign in as a **school administrator → Family Space**. If required, first have the Platform Super Admin activate the existing Ecosystem Hub tables. With a database backup available, click **Activate Family Space**. This explicitly creates six `pp_*` tables with `CREATE TABLE IF NOT EXISTS`. The updater itself does not run database migrations. Normal runtime can use CRUD privileges; activation needs CREATE privileges on that database.
4. Under **Portal Accounts / Account Links**, connect parent accounts to their children using the existing account-link workflow. Do not grant access based only on name/email matching. Publish appointment slots, dates, transport notices, consent forms, menus, documents, and surveys from Family Space. Teachers can publish their own slots and reply to assigned messages.
5. Test every portal area with at least two children and a second unrelated family. Verify the unrelated family cannot access the first family's results, invoices, receipts, documents, or child IDs. Verify existing Finance, Community Hub, WhatsApp handoff, school admin, teacher and platform logins.
6. Configure the school's **Paystack test** key using existing Finance settings. Confirm outbound TLS to `api.paystack.co` and the parent browser's access to `checkout.paystack.com`. Complete a real test transaction, return to Fees, and select **Verify payment**. Check that exactly one payment/ledger entry pair is posted and the correct confirmed receipt appears. Local automated tests used a simulated provider; they do not validate your provider account/network.
7. Review cPanel Errors, PHP logs, permissions, cron, malware quarantine, and file integrity over an observation period appropriate to the reported delay. Only after staging passes should you deploy the same packages to production in the same order, with a fresh backup and a maintenance window. The new production index has not been replaced by this work.

## Rollback and recovery

- The repaired **Updates & Plugins** page offers **Restore previous release** for the current committed update. It restores verified previous code and version metadata, retains newly added dependencies, and preserves all database records. Retained additive portal tables are harmless to the earlier application. Returning to the previous Finance file also returns its older receipt access behavior, so rollback is a temporary recovery step.
- If a request stops midway, the persistent transaction journal lets the next update attempt restore the previous files before installing. Failed backup checks stop the operation and require manual recovery. Do not delete backup journals to silence an error.
- If the dashboard cannot run or index.php is absent, use cPanel File Manager to restore the **verified stable index backup** and its required previous module versions from your independent backup. Restore with the correct account ownership and readable mode. Do not delete `parent_portal.php` as a cleanup measure; preserve it for investigation. Do not restore an entire database merely to undo this code-only update.
- Journals/backups are under `storage/system/backups/<id>/`, protected from HTTP by storage rules. They include prior hashes/modes, release hashes, state, and error details. Preserve them privately for diagnosis. Cross-file activation still has a brief mixed-version window; it is not a release-directory switch.

## cPanel hardening and evidence collection

Preserve your existing `.htaccess` customizations. The original rules already deny storage/config/database paths. The supplied full-source `.htaccess` adds `DirectoryIndex index.php` and denies `.zip`, `.tmp`, `.smnew`, and `.smrestore` artifacts. These additions are **not applied by the update ZIP**, because the updater deliberately excludes `.htaccess`. Review/merge these directives through cPanel after backing up the existing rules; confirm Apache supports them. An unexpected 500 after an .htaccess edit should be diagnosed from the Apache log and reverted immediately if necessary.

Move installer/repair ZIPs and exports out of the public document root after preserving private copies. Remove or disable the fresh installer after installation using your usual cPanel procedure. The update ZIP does not remove operator files. Do not change PHP upload/post limits globally; each update is small and must fit both PHP's configured upload/post limits and the manager's 12 MB upload cap. ZIP expansion is capped at 30 MB with an 8 MB per-file limit.

Optionally place `tools/integrity_check.php` and the **4.6.5 `release.json` extracted from the validated ZIP** in a private directory outside public_html. Use the owning account's PHP 8.4 CLI, for example:

```
/path/to/php84 /home/ACCOUNT/schoolos-private/integrity_check.php /home/ACCOUNT/public_html /home/ACCOUNT/schoolos-private/release.json >> /home/ACCOUNT/schoolos-private/integrity.log 2>&1
```

Replace paths with your cPanel account paths. Run once to establish a correct baseline before optionally scheduling it. This is read-only: exit 0 means expected hashes, exit 1 means a mismatch/missing file, exit 2 means bad arguments. Rotate/restrict the log and update the expected manifest after intentional releases. Preserve host quarantine/audit logs as well; a checksum mismatch alone cannot establish who removed a file.
