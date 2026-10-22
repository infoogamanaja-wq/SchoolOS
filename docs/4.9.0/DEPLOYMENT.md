# School Services 4.9.0 — install on working 4.8.0

This update adds Library Management, Inventory/Procurement/Assets, Communications/Engagement and School Website/CMS. It preserves the existing Finance, Family, Learning, HR, Transport, Boarding and Community Hub records. It is an update for an installed 4.8.0 application, not a standalone initial installer.

## Frontend installation

1. Back up the application, private configuration, protected storage and complete MariaDB database. Use a backed-up staging clone with the same PHP/cPanel configuration first.
2. Through **Platform Super Admin → Updates & Plugins**, install **SchoolOS-4.8.1-Services-Updater.zip**. This changes only the updater whitelist and leaves the working entry point unchanged.
3. Install **SchoolOS-4.9.0-Library-Inventory-Engagement-CMS.zip** through the same screen. The manager checks manifest hashes, dependencies and PHP syntax before replacing files; it replaces `index.php` last. Do not remove or manually overwrite the stable production entry point before verification.
4. As a school administrator, open **School Services → Activate School Services**. This creates **33 additive tables** and prepares existing module dependencies without inferring account links or resetting records.
5. Under **School Services → Access controls**, grant existing active staff/teacher accounts the required capabilities: `librarian`, `stock_manager`, `procurement_approver`, `asset_manager`, `communications_manager`, `website_editor`, `website_approver`. School administrators have these manager permissions. Approval still requires a different person where specified.

Verify the ZIPs against `dist/SHA256SUMS`. Required PHP 8.4 extensions include PDO MySQL, mbstring, fileinfo, JSON, tokenizer, ZipArchive, cURL and OpenSSL. Keep normal PHP file permissions (typically 0644), protected storage, and existing `.htaccess` rules. No world-write permissions are required. Application database connections now explicitly use the same Lagos timezone (`+01:00`) as PHP, preventing scheduled sends and temporary holds from shifting with the database server timezone. This sets the connection's timezone; it does not rewrite historical rows.

## Configure and operate

### Library

Reuse the existing `books` catalogue and `lp_library_loans` records. Catalogue edits validate entered ISBN10/13 checksums and configure shelf, daily overdue fine and replacement cost. Add received/donated copies separately with a reason. Student Portal requests and librarian issues/returns use the same loan register. Waiting reservations have first-come priority; cancel a reservation explicitly when no longer needed.

Print local QR catalogue labels, or scan a printed ISBN using a USB barcode scanner. Supported browsers can scan QR/barcodes with a permitted HTTPS camera; typed search remains available. Labels identify a catalogue title and do not authorize a loan. Existing loans are title/copy-count based, not individually serialized physical copies.

Daily overdue reminders are posted in Community Hub once per loan/day when staff select the action. Assess configured fines explicitly, preferably at return for a final amount. The first assessment freezes that fine; the release does not silently accrue or compound charges. Loss creates one replacement charge; recovery restores the copy but does not silently refund a previously paid charge. Use existing Finance for payment, receipts and reviewed corrections/refunds.

Digital resources require an active school account and licence dates. Licensed ebooks additionally allocate a seat for at most seven days or the licence expiry, whichever comes first. This controls application access; publisher authentication, redistribution rights, offline access and DRM are not provided by the update.

### Inventory, school store and assets

Configure legacy inventory items with type, reorder level, opening carrying cost and optional store price. Uniform sizes/book editions can be separate stock items. Record opening stock and issues with unique references. Negative stock and duplicate reference conflicts are rejected. Physical audits capture expected/observed quantities; correcting a discrepancy requires a separately referenced adjustment.

Employees submit purchase requests. A different procurement approver reviews them. A stock manager combines approved requests into a draft supplier purchase order, submits it, and obtains independent approval. An order's creator or a requester whose line it contains cannot approve it. Partial receipts use unique supplier delivery references and cannot exceed ordered quantities. Receiving posts inventory/supplier-payable journal entries; only a school administrator can confirm an actual external supplier payment after complete receipt. Confirmation does not transfer money.

Families request store orders for linked children. Staff approval reserves stock and creates a Finance invoice; staff can hand over goods only after Finance confirms full payment. Only unapproved requests can be cancelled here. Invoiced cancellation, refund or stock-release corrections need Finance/staff reconciliation; there is no automatic timeout that could release goods after a payment.

Register asset tags, acquisition date/cost, residual value and useful life. The accounting setup is immutable and does not create an acquisition payment/opening balance. Straight-line depreciation includes the acquisition month, posts the cumulative amount through the selected nonfuture month and protects residual value. Maintenance and physical asset audits retain findings and follow-up history.

### Communications, consent and providers

**School administrator → School Services → Communications & Engagement → Provider setup** saves per-school settings. Blank fields retain existing values. Secrets are encrypted at rest using **`storage/system/services-key.php`** (0600); back up this key **with** the database. A different/missing key cannot decrypt saved credentials. Do not regenerate a replacement over existing encrypted credentials; restore the matching backup. Secrets are never redisplayed or written into delivery/audit logs.

Available settings:

| Service | Settings / external setup |
|---|---|
| Email via Resend | `email_transport=resend`, `resend_key`, `email_from`; verify sender/domain with Resend |
| Existing SchoolOS SMTP | `email_transport=legacy_smtp`; uses the existing platform SMTP configuration |
| SMS via Termii | `termii_key`, `sms_sender`; provider-approved sender and funded provider account |
| WhatsApp Business / Meta | `whatsapp_token`, `whatsapp_phone_id`; a Meta-approved named template with **one body text parameter**, matching language |
| Signed WhatsApp status callback | `whatsapp_app_secret`, `whatsapp_verify_token`; subscribe Meta's message status callbacks |
| Browser push via OneSignal | `onesignal_key`, `onesignal_app_id`; configure the installation's HTTPS origin in OneSignal |

Optional server-managed overrides may be supplied in private `config.php` as `school_services => [school ID => [setting => value]]`. They take precedence over frontend saved settings; removing a saved value does not remove a server override. The sample config contains no credentials.

Account holders submit email/phone addresses; staff record ownership-verification evidence before external sending. This is a documented staff verification, not an automatic OTP verification service. Each recipient explicitly grants or revokes consent separately for **operational** and **marketing** messages and for each external channel. A currently linked, active parent must manage a student's external consent; removing that relationship invalidates the grant. In-app school notices remain available without external-channel consent. Emergency notices respect these checks too; use the school's established emergency calling/escalation procedure when immediate confirmation is essential.

After activation, the old Community Hub **email** button queues through the same verified-contact, consent, credit and delivery controls. Its prior posts, read/comment/scanner behavior and SMTP history remain available. Select the existing SMTP transport when retaining that configured service. Manual WhatsApp handoff links remain handoffs, not automatic or confirmed delivery. Admissions CRM correspondence remains its existing workflow; new public enquiries explicitly consent to a response and are not subscribed to marketing.

Campaigns are reviewed drafts, then explicitly scheduled in Lagos time. Newsletter campaigns always use marketing consent, even if a different purpose was selected when composing. Teachers may schedule **in-app only**, assigned-class notices/events/polls; communications managers can compose wider/external campaigns. Recipients and permissions are checked again at queue/send time. A parent/teacher message uses the existing Family/Teacher Portal thread record. Polls allow one vote per eligible account before closing.

**Credits are internal budget units, not money or provider credit.** Per external attempt: email 1, SMS 2, WhatsApp 3, push 1; in-app 0. A school administrator allocates units with a unique approval reference. Insufficient credit leaves messages queued. Definitive API rejection refunds units; accepted or uncertain outcomes retain them pending reconciliation. SMS segments, provider tariffs and account funding remain provider concerns; these fixed units do not estimate actual billing.

Status meanings:

- `queued`: not sent; consent/contact/credits may still block sending.
- `delivered` for in-app: stored in Community Hub, not proof it was read.
- `accepted` externally: provider API/SMTP acceptance, **not delivery**.
- `sent`, `delivered`, `read` externally: verified WhatsApp callback transitions where available.
- `failed`/`suppressed`: definite rejection or application access/consent guard.
- `unknown`, or `sending` left after a worker interruption: reconcile against the provider before composing a replacement; these are never automatically retried. Cancelling a campaign cannot recall accepted messages.

Configure Meta's callback as `https://YOUR-INSTALLATION/index.php?eg_webhook=SCHOOL_ID`. Use the private verification token in Meta's challenge setup. POST events require the correct SHA-256 signature and school phone-number ID. Duplicate/out-of-order callbacks cannot downgrade a confirmed delivery. Email/SMS/push acceptance is not promoted to confirmed delivery without supporting evidence.

For push, recipients use **Consent → Enable browser push**, permit the OneSignal SDK/worker, save their browser subscription, then explicitly grant push consent. HTTPS, compatible browser permissions and OneSignal setup are required. The optional SDK/worker is fetched from OneSignal's CDN. Push payloads contain only a generic sign-in reminder, not student information or message contents. Removing the saved subscription stops application sends; users may also revoke the browser/provider permission.

### cPanel scheduled delivery

Add a cron job, using the hosting account's actual **PHP 8.4 CLI binary** and installation path, for each school that sends scheduled broadcasts:

```
* * * * * /path/to/php84 /home/ACCOUNT/public_html/services_worker.php --tenant=1 --limit=30
```

Use a private log destination if recording cron output. The worker is CLI-only over HTTP, limits each run, serializes school workers with a database lock, and claims each delivery once before network I/O. Adjust frequency/batch size to the provider and hosting limits. The frontend can also process up to 10 queued deliveries explicitly. No background process starts just by installing this release.

### Website, domains and payments

In private `config.php`, configure `app.cms_origin` as the actual canonical HTTPS installation address (include a subdirectory if needed), for example `https://getschoolos.com.ng`. Under **Website & CMS**, configure one of three themes, SEO title/description, and enable the school site. Each school has its own public token link; the platform homepage remains intact.

Editors submit draft news, pages, galleries, admissions landing content, events, public staff profiles, testimonials, prospectus PDFs and tours. **A different approver** publishes/rejects them. A replacement with the same type/slug leaves the current published revision live until approval. Public text is escaped; arbitrary HTML/scripts are not executed. Identifiable gallery/testimonial/staff content requires a publication-consent reference. Staff profiles never automatically expose private HR records. Media accepts checked JPEG/PNG/WebP or prospectus PDF up to 3 MB; draft/archived media are not public. Live booked tours cannot be silently replaced/withdrawn.

The admissions landing page links to the same school's existing open application form. Public enquiries are CSRF/nonce/honeypot/rate guarded and enter the existing Admissions CRM. Public processing consent is not external-channel marketing consent.

For a custom domain, request the exact hostname, publish the supplied `_schoolos-verify.HOST` TXT value and a CNAME to the canonical installation hostname, then select DNS verification. Configure the alias to the **same installation** in cPanel and provision a valid HTTPS certificate. Add the exact verified hostname to `app.cms_allowed_hosts` in the private server config before activating it in CMS. No arbitrary/wildcard Host routing is enabled. Automated tests use simulated DNS records; live DNS, cPanel mapping and certificate provisioning remain operator steps.

Tours support one place per booking and capacity-checked temporary holds (30 minutes for paid bookings). Free tours confirm immediately. Paid tours use the school's existing **Finance Paystack key** and exact server-side amount/reference/NGN verification; a checkout return or client claim never confirms payment. The private booking link provides payment/printable-record access. Late verified payments without remaining capacity become `paid_review`; contact the visitor and reconcile/refund with Paystack rather than overbooking. Tour payments post a cash/tour-advance journal and remain distinct from student fee invoices; existing Family Space continues to handle student fees, checkout and receipts. School Services does not automatically issue a bank refund or classify tour advances as earned income.

## Rollback and scope of evidence

Pause School Services cron during rollback. Rollback the **4.9.0 installation** through Update Manager. It restores the exact previous index and Learning Portal file, retains newly introduced modules/worker files, and leaves all additive tables, credentials and records intact. Reinstallation preserves those records; resume cron after reinstating the service routes. This is code rollback, not a reversal of business, stock, payments or messages; reconcile such records through reviewed workflows. Keep the support updater installed.

All testing used synthetic local data and simulated provider/DNS responses, with actual local HTTP/Apache uploads, installation, rollback and CLI execution. No production cPanel server, live gateway transaction, real message recipient, publisher account or custom domain was used. Existing file-installation safeguards are retained; no permanent hosting-side deletion claim is made without server logs.
