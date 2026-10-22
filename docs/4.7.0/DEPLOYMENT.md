# Teacher & Student Portals — 4.7.0

This update extends the working 4.6.5 Family Portal release. It does not replace Finance, Family Space, Community Hub, WhatsApp handoff, existing authentication, or the database. Production was not accessed or modified during development.

## Install through the frontend in this order

1. Back up the working document root and database using cPanel. Preserve a separately verified copy of your working `index.php`, `config.php`, uploads, storage and `.htaccess` outside public_html. Restore the backup to a separate staging root/database first. Select PHP 8.4 and keep the same extensions used by the working release: PDO MySQL, ZIP, mbstring, cURL, OpenSSL, fileinfo and tokenizer.
2. Sign in as **Platform Super Admin → Updates & Plugins**. Upload **`SchoolOS-4.6.6-Learning-Updater.zip`**, check the trusted-source confirmation and install. It updates only `system_manager.php` to permit the new `learning_portal.php` module. It **does not change index.php**. Refresh the page after success.
3. Upload **`SchoolOS-4.7.0-Teacher-Student-Portals.zip`** in the same Update Manager. This installs exactly `index.php`, `learning_portal.php`, `system_manager.php` and `VERSION.txt`. Do not extract only index.php. Do not upload the source archive as an update. Compare archive hashes with `dist/SHA256SUMS`.
4. Sign in as a **school administrator → Learning Portals**, then click **Activate Learning Portals**. Activation adds eight `lp_*` tables and prepares any missing Academics, LMS, CBT, Welfare and Family schemas through their existing idempotent installers. It does not delete/relink existing records. This explicit action needs CREATE privileges; ordinary portal use requires normal CRUD permissions. Back up the database before activation.
5. Configure teacher allocations and student links as described below. Test with two teachers, two students, an unrelated class, and a parent. Verify existing Family Space, Finance, Community Hub, WhatsApp handoff, logins and receipts. Test the complete update and rollback on staging before using the same ZIPs on production in a short maintenance window.

The version sequence is **4.6.5 → updater support 4.6.6 → portals 4.7.0**. Do not edit version metadata or force a downgrade to bypass validation. Once 4.7.0 is installed, the support ZIP should not be uploaded again. Historical 4.6.4 and 4.6.5 ZIPs remain unchanged in dist/ for recovery/reference.

## Set up accounts and permissions

- Create users with the existing **Portal Accounts** workflow. A student must have exactly one distinct **Student → student record** link under **Account Links**. A parent link does not grant student access. Duplicate links to the same student are tolerated; links to multiple distinct students must be corrected by the school. No identity is inferred from names/emails.
- In **Academics → Teacher allocation**, allocate the teacher's **portal user ID** to a class, subject and academic session. Academic allocations use `users.id`, not the separate SIS `teachers.id`. The class's `session_name` must match the allocation. Teachers see only current allocated classes/subjects; no school-wide teacher access is granted by role alone.
- Configure curriculum topics, assessments and timetable in the existing Academics workspace. Teachers record lesson plans, coverage, attendance, draft scores and corrections through their portal. School administrators retain score moderation and result publication. Submitted/approved scores cannot be overwritten by teachers; published results remain locked.
- Teacher-created courses are drafts until published by the owning teacher. Activities are visible to students only in published courses for their class, after the opening time. Homework submissions respect deadlines and graded-work locks. Attachments are validated PDF/images/plain text up to 2 MB, stored in the database and downloaded through access-controlled endpoints.
- Teacher-created question banks/exams are drafts. School administrators review/publish them and complete manual CBT marking using the existing CBT workspace. Published banks and banks with attempts cannot be changed through the teacher portal. Student CBT supports explicit Save, resume, timed expiry and school-controlled result publication. **Save regularly:** expiry submits previously saved work; unsaved late answers are rejected.
- Library loans require administrator issue/return; requests alone do not decrement copies. Clubs require school approval and respect capacity. Teacher leave, development records and score corrections are reviewed under **Learning Portals → School approvals**. Confidential incidents appear in the existing Welfare workspace.

## Score CSV upload

Under **Teacher Portal → Bulk uploads**, select an allocated assessment and upload a UTF-8 CSV under 256 KB, with 1–500 rows and exactly this header:

```csv
student_no,score
YOUR-ADMISSION-NUMBER-1,22
YOUR-ADMISSION-NUMBER-2,24
```

Use actual admission numbers and marks within that assessment's maximum. The full file is validated before preview. Confirm the preview within ten minutes to import all rows atomically. Invalid/duplicate/unrelated students reject the file. Import rechecks permissions, student class, assessment publication and score state at confirmation. No partial import occurs. Bulk uploads in this release cover **assessment scores**; question-bank authoring is through the teacher form.

## Enable real AI assistance separately

AI is **off by default**. All non-AI workflows work without a provider key. The implemented adapter uses OpenAI (`gpt-4.1-mini`, with `omni-moderation-latest` for input/output moderation), over verified HTTPS to `api.openai.com`.

1. Through your private cPanel configuration workflow, set the existing **`providers.ai_api_key`** entry in the site's `config.php` to the school's provider key. Keep config.php private/readable only by the owning PHP account. Do not put a key in chat, a public form, an update ZIP or Git. Existing configuration is never overwritten by these updates.
2. Confirm the host permits outbound HTTPS to `api.openai.com`. No AI provider traffic was made during automated tests; those tests used a simulated transport. Provider billing and account availability remain your school's responsibility.
3. Under **Learning Portals → School approvals**, enable teacher assistance and/or student assistance explicitly and choose a per-account daily limit (1–20, default 5). Confirm the school's policy for student access before enabling it. Existing enabled settings are displayed and preserved by the form.
4. Test an age-appropriate lesson request as a teacher and a practice/explanation request as a student. Confirm a missing/invalid key or provider/network failure produces a helpful error. Verify assistance is blocked during active student CBT.

Safeguards include teacher/student role checks, current student identity, school-controlled enablement, quota reservation with account locks, bounded prompts/output, common identifier redaction, educational system instructions, risk/cheating keyword refusal, input/output moderation, and exam checks before/after external calls. Moderation errors fail closed. No school records, grades, documents or answer banks are attached to model requests. Users must still avoid entering personal details; filtering is not a guarantee that arbitrary sensitive text will be identified. Responses are escaped text, not executable HTML. Teacher lesson output is a draft for human review; AI never writes grades or approves work. Failed provider requests consume quota to prevent unlimited retries. Raw prompts/responses are not stored in database logs; a response is held temporarily in the user's session for display. Audit records contain a redacted-prompt hash and the user ID.

## Rollback

Use **Updates & Plugins → Restore previous release** for the current 4.7.0 deployment. It restores verified previous code and version metadata while retaining new dependencies and every database record. It returns the application index to the working 4.6.5 code with the 4.6.6 updater support still installed. The added tables and legitimate submissions/requests remain in the database and must not be dropped as a rollback step. Reinstall 4.7.0 directly when ready.

The rollback/install/reinstall sequence was tested through the real multipart frontend under Apache/FastCGI. If the dashboard cannot run, restore the verified working files through cPanel using the private backup. Preserve updater transaction journals for investigation. The earlier atomic update and no-deletion protections remain in place. Local tests do not guarantee against a future hosting quarantine or external deletion; continue the existing file/log monitoring.

The updated read-only `tools/integrity_check.php` can be kept outside public_html with the new 4.7.0 `release.json`. It verifies the declared entry point, Learning module, updater and version hashes, reports a missing file, and never rewrites it. It also supports the earlier full Family release manifest. Use the manifest matching the installed release, not an old index hash. Modules intentionally unchanged and absent from a release manifest need a separate trusted baseline if you want their hashes monitored as well.
