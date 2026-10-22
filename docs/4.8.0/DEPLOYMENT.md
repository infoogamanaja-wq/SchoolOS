# School Operations 4.8.0 — cPanel deployment

For an existing working **4.7.0** PHP/MariaDB installation. This is an Update Manager release, not a fresh application installer. The existing Finance, Family and Learning modules are dependencies.

## Install

1. Back up the complete cPanel application directory and database. Test on a staging clone with the same PHP extensions and database version first.
2. In **Platform Super Admin → Updates & Plugins**, upload **SchoolOS-4.7.1-Operations-Updater.zip**. This updates only the manager whitelist; it leaves the working `index.php` unchanged.
3. Upload **SchoolOS-4.8.0-HR-Transport-Boarding.zip** through the same screen. The manager verifies the package, dependencies and PHP syntax, stages replacements and replaces the entry point last. Do not manually remove or replace the stable index before verification.
4. Sign in as a **school administrator**, open **School Operations**, and select **Activate School Operations**. Activation creates 36 additive tables and prepares the existing Family, Finance and Welfare dependencies. It does not automatically bind legacy staff records to accounts or change existing payroll values.
5. Under **Access controls**, grant the appropriate existing active staff/teacher accounts `hr_manager`, `transport_manager`, `boarding_manager`, `driver`, or `warden` access. School administrators have all manager permissions. Drivers and wardens still require explicit capability grants and driver/hostel assignments. A platform super administrator does not receive school payroll access through this module.

Verify downloaded ZIPs against `dist/SHA256SUMS`. PHP 8.4 needs PDO MySQL, mbstring, fileinfo, sessions, JSON, tokenizer and ZipArchive; the existing application's dependencies also remain required. Use normal PHP file permissions (typically 0644) and writable protected storage as described in the earlier deployment guides. Never grant world-write permission to PHP files.

## Configure each school

- **HR:** create departments; link existing staff records explicitly to employee accounts and departments; enter monthly basic salary; complete onboarding before activation. Recruitment hires create an unlinked onboarding profile; use **Staff records → Update account / department links**, then configure salary and onboarding. Contracts accept private PDF attachments up to 2 MB; they are stored in the database and served after authorization.
- **Payroll:** have the school's payroll adviser review the applicable annual tax band **widths**, fixed annual relief, taxable/pensionable allowances and pension percentages. No statutory defaults are supplied. Generate a draft for `YYYY-MM`; a **different HR manager or school administrator** must approve it. Only the school administrator confirms an actual external/manual payment reference. The application posts accounting records; it does **not** transfer funds. Full-month payroll only; joining/leaving proration, minimum-tax rules and year-to-date reconciliation must be resolved outside this release before approval where applicable.
- **Transport:** register vehicles and drivers, including licence expiry; create non-overlapping daily route schedules and stops; assign students within vehicle capacity. Start a pickup/drop-off trip to snapshot its manifest. A drop-off handover requires a current approved Family Space pickup authorization and a physical collector identity check. Renew licence/contact details in Drivers. Route settings control future fees, active status and optional GPS. Complete active trips before changing route, vehicle or driver status.
- **Boarding:** configure existing hostels or create new ones; assign explicitly authorized wardens; create rooms and physical beds; allocate students. Record arrival. Checkout needs an independently approved current leave permit and a physical collector identity check. Create visitor and roll-call records, private welfare cases, stock movements and meal menus. Publish menus to residents in Family Space; staff record the actual serving and any justified change from the family choice.

Use repeatable invoice period keys such as `2026-T1`. Transport/boarding invoices and configured meal-serving fees go into existing Finance; payment and receipts use its existing workflows. Do not issue the same charge again manually. Payroll posts to the general ledger, not `fn_expenses`; the existing expense-only cash/budget widgets do not include payroll. See VALIDATION.md for account codes and calculation limits.

## Rollback and retention

Use the Update Manager's **rollback for the 4.8.0 installation**. It restores the exact prior index and existing replaced files from verified backup bytes. Newly introduced modules are retained deliberately; rollback never deletes portal dependencies. The 36 tables and their records are retained too. Rollback is a code rollback, not a reversal of payroll, student movement, accounting or invoices. Correct business records through reviewed workflows; do not drop tables as a rollback step.

Leave the support updater installed; the known previous index remains compatible with it. Reinstalling the main ZIP after rollback preserves the additive tables. Keep backups, configuration, package archives and personnel documents inaccessible through public HTTP.

## Operational limits

Notifications are scoped **in-app** updates mirrored to Family Space. Existing WhatsApp/payment integrations are preserved; this release does not automatically send WhatsApp/SMS or initiate a bank payment. GPS is optional foreground, device-permission-based reporting over HTTPS, retaining only the latest point per trip. Disabling a route's GPS erases retained coordinates for that route. Families do not receive raw location coordinates. Route suggestions use straight-line proximity and spare capacity, requiring staff review of roads, travel time and safety. Physical identity checks are human checks; clicking the confirmation is not automated identity verification.

All evidence is from isolated synthetic databases and local PHP/Apache servers. No live cPanel server was accessed. This release retains the existing updater's entry-point safeguards; no claim is made that hosting-side deletion is permanently prevented without production logs.
