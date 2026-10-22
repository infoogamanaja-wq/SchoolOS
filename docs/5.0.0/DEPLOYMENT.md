# Install School Intelligence 5.0.0 on working 4.9.0

This is an update for the existing PHP 8.4/MariaDB/cPanel script. Do not install as a standalone application or skip earlier schema/module releases.

1. Back up the complete database, application, private configuration and protected storage, including the existing encrypted provider key. Test on a backed-up staging clone with the production PHP/cPanel configuration first.
2. In **Platform Super Admin → Updates & Plugins**, install `SchoolOS-4.9.1-Intelligence-Updater.zip`. It changes only the Update Manager and leaves the working index untouched.
3. Through the same screen, install `SchoolOS-5.0.0-Intelligence-Innovations.zip`. The updater validates allowlisted paths, hashes, PHP syntax and dependencies before activating files, and writes `index.php` last. The only newly allowed directory is `public/offline`; parent symlinks remain rejected. Never manually remove the stable entry point.
4. As a school administrator, open **School Intelligence → Activate School Intelligence**. Activation creates additive tables and prepares existing dependencies without deleting records or changing account links.
5. Assign staff/teacher capabilities in **Access & settings**. Use separate author/reviewer accounts for approvals. Reports, Finance reports, HR reports, success review, pickup, flow approval, curriculum, timetable, prepaid cashier, alumni, accreditation, privacy, HQ and integrations have distinct capabilities.
6. Review school procedures and applicable provider/legal/privacy arrangements before enabling optional AI, offline capture, prepaid credits or mandatory transport pickup tokens. Record the review note. Saving settings does not itself send messages, spend credits or execute AI actions.

Check package SHA256 against `dist/SHA256SUMS`. Retain ordinary 0644 files and 0755 public directories; no world-write permissions are needed. Required extensions: PDO MySQL, mbstring, fileinfo, JSON, tokenizer, ZipArchive, cURL and OpenSSL. Browsers need HTTPS/WebCrypto/IndexedDB for offline use. Protect `storage`, configuration and database directories using the existing Apache rules. Local validation used PHP 8.4.24 and MariaDB 11.8/10.11, not your production server.

## Configuration and cron

Report schedules generate private CSV records rather than public files or emailed attachments. For each activated school, use its actual numeric tenant ID in a cPanel cron such as:

```sh
/path/to/php /home/ACCOUNT/public_html/intelligence_worker.php 123 20
```

Select the correct PHP 8.4 binary in cPanel. The worker is CLI-only, processes up to the supplied limit (maximum 100), rechecks current definition-owner permissions and removes only expired generated report exports. A failure disables the affected schedule with a review message; correct the owner/scope then create a reviewed replacement schedule. It does not automatically scan success alerts, send provider messages or run financial actions.

Existing external delivery cron (`services_worker.php --tenant=123 --limit=20`) remains separate. Configure the canonical HTTPS CMS origin, per-school verified contacts, explicit parent consent, Meta callback signature/phone ID and approved templates as documented in 4.9.0. Configure BALANCE/ATTENDANCE/PAYMENTS/HELP flows with a different reviewer. Outbound credit units are not provider funds. Incoming STOP revokes consent. Provider acceptance does not establish delivery.

Optional Intelligence AI uses its own encrypted school credential in Access & settings; existing teacher/student AI settings are preserved. Provider availability, contractual child-data safeguards and transfers need school review. No live AI, Paystack or WhatsApp account was exercised by automated tests.

## Offline operation

Teacher → School Intelligence → Curriculum, Reports & Timetable → Offline workspace opens `public/offline/offline_teacher.html`. Sign in first, enable school offline capture, choose assigned class/recent attendance date, confirm a trusted device and use a unique passphrase of at least 12 characters. Capture while connected, then unlock/use the encrypted workspace offline. Keep the passphrase securely; it cannot be recovered by the school.

Reconnect using the same school/teacher account and synchronize. Applied edits leave the queue; conflicts/denials remain for human review. Capture a fresh snapshot before editing records already synchronized. Capturing replaces the local snapshot/queue after a warning. Snapshots expire after seven days. Do not clear browser data with unsynced edits. On shared devices explicitly delete the local workspace after syncing; logout does not remotely erase a device's encrypted storage. Browser/OS compromise and weak/reused passphrases remain risks. The worker caches only this static shell, never authenticated application responses or data exports; its scope does not replace the existing root push worker.

## Accounting and governance

Prepaid credits are disabled initially. A parent sets eligible school purchase categories and a daily cap. Staff enter cafeteria menu prices; purchases take server prices/current eligible invoice balance, lock credits and post liability/revenue or liability/receivable entries. Bank declarations do not prove payment: another school administrator checks the real bank statement and unique reference. Paystack verification must match NGN amount and reference. Reconcile liability account `2120`, external funding and daily balances. Do not use this feature as an unreviewed general-purpose financial service. Cafeteria credit restoration is not an external bank refund; invoice corrections go through Finance review.

Scholarships are approved fee waivers, within round budgets and linked unpaid base fees. Fundraising bank declarations require independent verified receipts and post restricted receipts to `2130`; no payout is initiated. Configure/review account codes `2120`, `2130`, `4100` and `5400` with the school's accountant. Existing fee Finance cash summaries do not automatically include every new journal source.

Configure official curriculum/state rule references and review school calendars instead of treating sample dates as authoritative. Curriculum/report design, mentoring, evidence, plugin and HQ-policy review require different users. Each school consents to HQ datasets; revoke sharing to stop subsequent requests. API v1 is read-only: `GET index.php?ix_api=v1&dataset=attendance` with `Authorization: Bearer TOKEN`; never put tokens in query strings. Rotate/revoke tokens, limit scopes and treat all responses as private.

NDPA processing records and rights workflows support the school's privacy programme; they do not certify legal compliance or automatically erase retained records. Approved access downloads are bounded and may require a separate complete response by the school's privacy officer.

## Rollback and evidence

Use **Updates & Plugins → rollback** for the main release backup. Tested rollback restores the exact previous index and modified pre-existing modules, retains new dependency/static files, and keeps additive database records. Reinstalling 5.0.0 returns the new interfaces and saved records. File rollback does not reverse payments, awards or other business transactions performed after installation; reconcile those separately.

The original hosting deletion incident cannot be declared permanently resolved from these local tests. No production server logs were accessed. Review cPanel deployment/file-manager/backup/antivirus/cron/PHP logs if it recurs; preserve timestamps and hashes rather than deleting evidence. Keep the validated staging and production backups.

On cPanel/FastCGI configurations that strip the HTTP Authorization header, API v1 also accepts the same secret in `X-SchoolOS-Token: TOKEN`. Use HTTPS and never send either credential in a URL.
