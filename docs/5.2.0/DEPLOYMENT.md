# SchoolOS 5.2.0 — deployment

This is an update for an existing 5.1.0 PHP 8.4/MariaDB installation, not a standalone installer. Upgrade earlier versions in sequence. No production server was accessed during development.

## Install on a staging copy first

1. Back up the complete database, application files, `config.php`, uploads, private storage and both encryption keys (`storage/system/v23-key.php` and the school-provider services key). Keep backups outside the public document root.
2. Sign in as Platform Super Admin. In **Updates & Plugins**, install `SchoolOS-5.1.1-Website-Affiliate-Updater.zip`. This only expands the updater's exact destination allowlist; it leaves the stable `index.php` in place.
3. Install `SchoolOS-5.2.0-Website-Affiliates.zip`. The manifest covers all 15 payload files, including public documentation and fictional dashboard screenshots. The updater stages and verifies files before replacing the entry point last. Normal payload permissions are 0644.
4. Open the platform website and its **Platform**, **How it works**, **Guides**, **Partners**, **About**, **Contact**, **Privacy**, **Terms** and **Cookies** pages. Verify mobile navigation, dashboard previews, quiz/facts and all PDF downloads. Confirm school-domain CMS sites remain correctly routed.
5. Open **Website & Affiliates** from the dashboard header and choose **Install Website & Affiliates module**. This adds six InnoDB tables and defaults to disabled. Existing school tables and records are not rebuilt or deleted.
6. Operator defaults are **Vendorhub Global Concept** and **admin@getschoolos.com.ng**, supplied by the owner. Review their public display and the policies against the actual operating agreement.

## Configure the affiliate program

- Set a nonzero commission rate in **basis points** (1000 = 10%; supported maximum 5000 = 50%). Set the holding period in days (0–365) and minimum withdrawal in **kobo**, not Naira (500000 = ₦5,000). These are configuration choices, not promised rates.
- Confirm the canonical **HTTPS platform origin** in Setup & Accounts; referral links use that origin. Approve terms before enabling the program.
- Test provider integration using Paystack test mode. Test and live commission balances, payout recipients and withdrawals are separated. Reverify a payout bank account after changing environment. Test credits cannot fund live withdrawals.
- Test a new affiliate application, platform approval, referral link, new-school registration, exact verified subscription payment, one commission, holding period and withdrawal. Repeated callbacks must not create another credit.
- Configure Paystack's webhook to `https://YOUR-PLATFORM/index.php?v23_webhook=paystack`. Signatures are checked, then charge, transfer and processed-refund evidence is fetched from the provider. A browser return or unsigned payload is insufficient.
- Bank resolution and transfers require the appropriate provider permissions, an active NGN recipient and sufficient provider balance. Review a withdrawal before choosing **Approve & transfer**. A timeout stays reserved as `sending`; use **Verify provider status**. Never submit the same uncertain withdrawal again. Transfers requiring OTP must be authorized in the provider dashboard, then reconciled here.
- Add a cPanel cron every ten minutes, using the actual PHP 8.4 binary and absolute path:

  `php /absolute/path/public_html/affiliate_worker.php`

  The worker reconciles up to 100 transfers per run in the current provider environment. Submitted transfers take priority; successful transfers are checked for reversals for 30 days after creation. It never creates a new withdrawal or approves one. Nonzero exit status means configuration or reconciliation needs investigation. Protect cron logs from public access.
- Only enable live payouts after a controlled real provider transaction has been accepted, reconciled and checked by the operator. Local tests use simulated financial responses and do not prove that a live Paystack account permits transfers.

## Operational rules

First valid referral attribution wins for a new school registering within 30 days. The referral cookie contains a signed absolute expiry. Rates/holding periods are frozen at attribution; verified renewals for that referral also earn. Free plans, trials and unverified payments do not earn. Self-referrals matching the owner identity/email are excluded; investigate related-party abuse that software cannot infer from account identity alone.

Turning the program off stops new applications, referrals, bank changes and withdrawal requests. Existing balances stay visible, eligible already-attributed payments still accrue under their recorded terms, and existing transfers can still be reconciled. Suspension blocks new financial actions and payout authorization for that affiliate. Refunds reverse commission proportionately; refunds after payout leave visible debt that reduces future availability. Disputes/chargebacks require operator review and payout suspension until the source transaction is resolved; they are not silently treated as completed refunds.

## Rollback

Use Update Manager's recorded backup to roll back the main package. The exact prior entry point and changed libraries are restored. New dependency files and additive tables remain; registered schools, credits and withdrawal history are not deleted. Reinstalling the same release from the supported baseline preserves those records. Existing transfers must still be reconciled with the provider even if the public affiliate program is paused or the UI is rolled back.

The hosted documentation page is `index.php?page=documentation`; public account guides use an exact allowlisted role key and generate a PDF download on the server. No external PDF service or shell command is used. PDF generation supports hosts with mbstring but no iconv.
