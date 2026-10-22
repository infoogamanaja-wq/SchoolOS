# Install Platform Experience 5.1.0 on working 5.0.0

This is an update for the existing PHP 8.4/MariaDB/cPanel application. It is not a standalone installer. Existing school records, Finance journals, account links, files and private provider configuration are retained. No production server was accessed during development.

## Install through the existing frontend

1. Back up the complete application, database and protected storage, especially `storage/system/v23-key.php` and the existing Services encryption key. Test on a backed-up staging clone using the production PHP/cPanel configuration first.
2. As **Platform Super Admin → Updates & Plugins**, install `SchoolOS-5.0.1-Experience-Updater.zip`. This only extends the updater's approved file list; the working entry point remains untouched.
3. Install `SchoolOS-5.1.0-Platform-Experience.zip` through the same screen. It validates manifest hashes, PHP syntax and dependencies before activation, and installs the entry point last. Never manually delete or overwrite the stable production index before validation.
4. Open **Setup & account → Activate Experience & installed workspaces**. Platform or school administrators can prepare the additive Experience and installed workspace tables. This does not enable live AI, configure providers, send messages, charge subscriptions or change existing school records.
5. Review **My overview** and replay **Take a walkthrough**. School administrators get a detailed setup journey, readiness checks, priority alerts and workspace health screen.

Verify both ZIPs against `dist/SHA256SUMS`. Ordinary PHP/static files remain 0644; no world-write permission is needed. Existing Apache protection for storage, configuration and archives remains required. PHP extensions remain PDO MySQL, mbstring, fileinfo, JSON, tokenizer, ZipArchive, cURL and OpenSSL. New UI assets are local; no additional application package manager or external font/CDN is required.

## Enable new-school registration and subscriptions

As platform administrator:

1. Configure active plans, each offered billing cycle's price and trial days in **SaaS Control Centre**. A termly cycle is four months; annual is twelve. Trials follow configured plans, capped at 90 days. An entirely zero-price plan is free. A zero-price cycle on an otherwise paid plan is unavailable, preventing accidental free access through an unset price.
2. In **Setup & account**, enter the canonical **HTTPS installation URL**, including any installation subdirectory. Choose **Use configured plan trial days**, then enable school registration and school-approved member registration. Public registration starts disabled until reviewed. The user's selected plan/cycle determines the server-side price snapshot; browser-supplied amounts never control the charge.
3. Configure and test the platform Paystack gateway in **Integrations**. This is the platform subscription gateway, distinct from each school's fee-payment credentials. Configure the existing signed provider callback using the installation's documented webhook route. Gateway availability and actual settlement require live-account verification outside these local tests.
4. Visit `index.php?register=1`. Registration creates the school, owner, subscription and enrolment together. Allowed trials enter guided setup immediately. Plans without trials wait at a billing screen until exact NGN amount, currency and reference are verified by the server. A browser callback alone never activates access. Failed checkout leaves a pending reference for reconciliation rather than claiming payment.

Self-service schools are gated when their subscription expires. Their aggregate API also checks subscription access. Administrative suspension cannot be lifted by paying. Existing direct-provisioned schools retain their current platform billing arrangement; this release does not silently migrate their contracts, expire old subscriptions, or change their prices. Existing background-worker policies are not a newly introduced universal subscription-metering engine.

Free plans have an explicit renewal action after expiry; repeated renewal cannot accumulate future periods. Paid checkouts use the captured enrolment terms, and concurrent verification extends the period only once per transaction. No automatic renewal debit, recurring provider mandate, coupon application or automatic contract-price migration is introduced. Plan changes, discounts and legacy contracts need platform review. Existing catalogue/limit/feature configuration is not represented as a new automatic usage-billing system.

## How schools create users

Both administrator invitations and approved self-registration are supported, as requested.

- **Direct creation:** school administrators continue using **Portal Accounts**, then **Account Links**, teacher allocations and assigned operational duties. Existing accounts are retained.
- **Self-registration:** in **Setup & account → People & access**, the school chooses whether to accept requests and whether to list its name/state publicly. A private school can share its invitation code. No school directory is published without opt-in.
- **Verification:** the applicant uses `index.php?join=1`, selects a listed school or supplies its code, and requests a role. The account stays inactive. The administrator verifies identity, control of the email address, school relationship and appropriate role. Self-registration never grants school/platform administrator status.
- **Activation:** approval replaces the password submitted on the pending request with a random temporary credential shown once to the administrator. Share it only with the verified person through a secure school process. It expires after 72 hours and must be replaced with a personal 12–72 character password before any school records open. This prevents an unverified pending password from becoming an approved person's credential.
- **Record access:** approval does not guess child links, teacher allocations, driver routes or warden duties. Assign these explicitly. Unlinked members see a helpful overview, while protected learning/child routes remain denied.
- **Recovery:** **People & access → Help someone sign in** issues a new temporary credential for an active member in that school after verification. A school owner needs platform-team recovery from the platform Experience page. Platform administrator recovery remains an operator-controlled procedure. This release does not pretend to send a reset email without a configured, verified recovery process.

Rejected or incorrectly submitted requests need school/platform review; they do not silently move an existing globally unique email account between schools. No child/employee record is inferred from a matching name. Approval, recovery and access changes are audited without logging passwords.

## Provision the connected demo safely

The login page includes role buttons that fill fictional credentials and select the demo sandbox. The demo needs **its own database**; buttons cannot authenticate against the live school database.

1. In cPanel, create an **empty dedicated MariaDB database whose name ends `_demo`** and assign dedicated credentials. It must differ from the application database. Do not use a populated school database or import real records into it.
2. As platform administrator, open **Setup & account → Isolated connected demo**, enter the dedicated connection details and confirm the empty sandbox. The application refuses populated databases, builds its own schema and seeds fictional records. Credentials are encrypted in protected platform storage; they are never embedded in the ZIP, browser assets or screenshots.
3. Return to the login page. Select School owner, Teacher, Parent, Student, Driver, Warden, HR, Librarian, Store, Communications, Admissions, Partner, Platform overview or School reviewer. The button fills the form; the visitor presses Sign in. The reviewer is a second fictional school administrator for independent approval workflows.
4. Try the connected journeys: teacher attendance → parent view; learner homework/CBT → teacher review; driver manifest → family transport; library request → lending history; communications CMS draft → independent reviewer publication. The demo contains 24 learners, multiple classes, linked siblings, approved results, homework, balanced fee records, staff records, transport/boarding assignments, family posts and approved sample news.

Shared demo changes can be replaced. Never enter real personal or payment details. The platform demo is read-only; permissions on seeded roles are fixed. Uploads, native mail dispatch, SMTP, live payment/AI/message transports, private provider configuration and host-management endpoints are blocked. Some real integrations are intentionally unavailable in the demo; the screens explain their prerequisites rather than fabricating successful sends or charges.

Demo cookies and server-side session files are separated from real sessions. Storage is private under `storage/system/demo-sessions`. A demo session ID cannot be replayed into the stable application after rollback. Signing into the demo ends the current normal browser session; signing out exits the sandbox. Keep storage protections and filesystem permissions intact.

### Refresh date-sensitive sample data

Use the platform's confirmed **Keep the demo fresh** action, or configure an optional cPanel cron using the correct PHP 8.4 binary:

```sh
/path/to/php /home/ACCOUNT/public_html/experience_demo_refresh.php --confirm-isolated-demo
```

Choose a quiet daily time in **Africa/Lagos**, for example **02:30 WAT** if the cPanel cron timezone is configured accordingly. This replaces **all shared fictional visitor changes**, refreshes dates/manifests and restores demo accounts. It checks the separate database marker and the exact provisioned table list; unknown additional tables cause a refusal before deletion. A concurrent reset is refused. A maintenance flag prevents new demo sessions during rebuilding. Live schools and their private credentials are not copied or cleared.

If rebuilding fails, the demo may remain unavailable until its dedicated database is reviewed/reprovisioned. Do not attempt to fix that by deleting live tables or encryption keys. Maintain separate backups and schedule resets away from demonstrations. Existing demo session files follow PHP session garbage collection and may also be cleaned by the host's normal private-session maintenance.

## Review and rollback

Check the [audit](AUDIT.md), [feature map](FEATURES.md), [validation](VALIDATION.md) and screenshots before production installation. Test actual mobile/assistive-technology usage, gateway settlement and provider configuration in staging.

Frontend rollback restores the exact 5.0.0 entry point, modified libraries and former static templates, retaining new dependency files and additive database records. Reinstalling returns saved schools/subscriptions. Rollback does not reverse payments or other business events; pause new registrations and reconcile business changes if rolling back. Version 5.0.0 does not supply the new self-service onboarding/expiry screens. Demo session isolation remains safe even when the old index runs.

No production server logs were accessed. Local installation/rollback tests cannot prove that hosting cron jobs, antivirus, backup tools or file-manager users will never delete files. Preserve logs and timestamps if the earlier hosting issue recurs.
