# SchoolOS 5.3.0 — portal update

This updates an existing **5.2.1** PHP 8.4/MariaDB installation. It is not a standalone installer. Upgrade older installations in sequence. Production has not been accessed or modified.

## Install and review on staging

1. Back up application files, database, uploads and private storage outside `public_html`. Include `config.php`, `storage/system/v23-key.php` and `storage/system/services-key.php`. Encryption keys must remain paired with their database ciphertext.
2. As Platform Super Admin, open **Updates & Plugins**. Install **SchoolOS-5.2.2-Portal-Updater.zip** first. It updates only the updater allowlist and preserves the exact existing `index.php`.
3. Install **SchoolOS-5.3.0-Role-Portals-LMS.zip**. Its 23 files are hash-verified; new helper modules precede the updated Experience loader, and the updater replaces `index.php` last. Normal file modes are 0644. The package contains no credentials, private keys, database dumps or upload contents.
4. Open **Setup & Accounts / Start Here** and activate the installed workspaces. Activation creates eight additive `px_*` tables. Repeating activation preserves records. Existing finance, wallet, affiliate and operational tables remain in place.
5. Complete school branding: school name/logo/motto, address, telephone, email and website. Receipt downloads use these fields automatically. Missing details cannot be invented; an absent logo receives a school monogram. Print or save the receipt to PDF from its print button.
6. Check parent/child links and current teacher allocations. They control conversation contacts, parent messaging and live lesson access. Review specialist Operations, Services and Intelligence grants; ordinary teachers no longer receive unrelated generic desks. Teachers linked to an employee record retain their own employment workspace.
7. In Family engagement, publish calendar items with start/end time, audience and venue. Publish a meal menu with options and a dated range. Parents then choose separately for each available day; old responses are retained. Approve pickup requests before issuing short-lived pickup tokens. Collector phone numbers supplement existing physical identity checks.
8. Review the connected demo and live staging roles using the acceptance list below. Only promote the tested files through the Update Manager after these checks pass.

## Connected public demo

If already configured, the marked, separate `_demo` database upgrades on its next connection. The update validates its existing table fingerprint, acquires the demo maintenance lock, creates the additive tables and inserts fictional examples transactionally. Existing visitor bookings survive this migration. Unexpected tables cause refusal rather than deletion.

If the demo has **never been configured**, create an empty dedicated cPanel database ending `_demo` and a dedicated database user. Open **Platform Super Admin → Setup & Accounts → Isolated connected demo** to validate/provision it. The update cannot create a cPanel database or infer hosting credentials. Login role buttons work after this setup. No live-school data is copied into the demo.

Optional refresh: `php /absolute/path/public_html/experience_demo_refresh.php --confirm-isolated-demo`. Refresh intentionally replaces shared fictional visitor changes; run during a quiet period. Only explicitly configured sandbox classroom relay settings are preserved. Protect the private services encryption key. Never enter live-school relay secrets in the public demo.

## Virtual classroom setup

Teachers can create a meeting in their own Zoom or Google Meet account and paste the HTTPS invitation into an allocated live lesson. No API credentials are needed for invitation links. SchoolOS does not create provider accounts or schedule meetings through provider APIs.

The built-in classroom is a **small-group teacher broadcast, eight participants including the host**. Learners receive video/audio without camera or microphone prompts. Teachers can share their screen. Leaving stops local capture; there is no recording. School chat provides questions/replies. Larger classes should use the configured invitation provider.

Use HTTPS and a WebRTC-capable browser. Reliable connections between different networks require a contracted or school-controlled **TURN relay**, using expiring HMAC-SHA1 credentials. A normal PHP/cPanel account does not supply this media service automatically. In the school's Teaching studio → Live classroom, configure the TURN URL and shared authentication secret as school administrator. The URL may use `turns:relay.example.ng:5349`; the shared secret must match the provider's expiring-credential convention and have at least 20 characters. Both values are stored encrypted; browsers receive only temporary credentials. Review provider quotas, region, retention and contracts before real child participation.

The platform administrator can configure a **separate demo relay** in Setup & Accounts. Live-school secrets are never imported into the demo. Local validation used a loopback-only coturn test fixture; it does not provision a hosted production relay or prove connectivity on the user's real networks.

## Staging acceptance

- Parent: switch children; see published CA/exam/total; download branded confirmed receipt; message administrator and assigned teacher together; expand dated event; save individual meal days; book an appointment; submit absence and pickup with phone; see focused success/error feedback and overview transport update.
- Teacher: only relevant role navigation; course map, resources, assignments and assessment tools; family appointments; private parent messaging; create an invitation and host a built-in lesson.
- Learner: learner course journey, assignments/resources, own grades, verified family chat, live lesson reception, own school-day transport/boarding and enabled own wallet.
- Specialist accounts: relevant library reservations, finance, HR, driver and warden workflows; active feature highlighting; no unrelated management desks without grants.
- Light/dark and mobile: visible text, form options, feedback, keyboard focus, no page overflow, optional update sound and pause/reduced-motion behavior.
- Chat: a verified guardian and learner exchange messages without reloading; unrelated users and foreign-school accounts cannot fetch the conversation.

## Rollback

Use the Update Manager's backup for the **5.3.0 main package**. Its pre-update baseline includes the support updater. Rollback restores the prior files, keeps private configuration and does not drop additive tables or delete new records. Reinstalling can reuse those tables. Restore a database backup only as a separately planned recovery operation; file rollback does not reverse business activity.

The real frontend install/rollback/reinstall test preserved the stable baseline homepage, Finance view, affiliate module, wallet and private configuration, and retained a pre-upgrade demo booking. No claim is made that hosting-side deletion is permanently resolved: cPanel/antivirus/filesystem access logs are still required to attribute a future hosting deletion.
