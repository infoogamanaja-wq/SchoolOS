# School Services 4.9.0 feature map

School Services uses current active accounts, school-scoped capabilities, explicit parent/student links and CSRF-protected writes. Business history stays in existing records where those records already exist. The new navigation supplements the existing portals and Community Hub.

## Library Management

| Requested area | Implemented workflow |
|---|---|
| Book catalogue | Existing books, title/author/shelf edits and audited copy adjustments |
| ISBN | ISBN10/ISBN13 normalization and checksum validation on entered catalogue values |
| Digital resources | School-account access through a guarded HTTPS resource endpoint and active licence dates |
| Lending and returns | Shared Student Portal loan register, librarian issue/return/reject and replay guards |
| Barcode/QR | Locally generated printable QR keys, ISBN/typed/USB-scanner search, supported-browser camera scanning |
| Reservations | First-come waiting queue, explicit cancellation and priority enforced in both new and legacy issuing |
| Overdue alerts | Staff-triggered daily in-app reminders, once per overdue loan/day, via existing Community Hub |
| Fines | Explicit daily-rate assessment frozen once per loan; existing Finance invoice/payment/receipt workflow |
| Losses | Once-only physical copy removal and replacement invoice; recovery restores a copy with Finance refund review kept separate |
| Licensed ebooks | School licence dates, seat limits, up-to-seven-day checkout/return and immediate access disable |
| Reading history | Own/linked-child physical loan history and ebook seat history; librarian school-wide view |
| Inventory reports | Titles, physical copies, available/issued counts and loan-status totals |

The existing register counts copies per title; labels are catalogue identifiers, not individually serialized copy or borrowing credentials. Digital access controls are not publisher DRM. Browser/device permissions and publisher rights remain external requirements.

## Inventory, Procurement & Assets

| Requested area | Implemented workflow |
|---|---|
| Asset register | Reuse existing assets; unique tags, acquisition cost/date, residual value, life and book value |
| Stock levels | Reuse existing inventory quantity, carrying cost metadata and audited signed movements |
| School store | Linked-child order request, approval/reservation, Finance invoice and paid handover |
| Uniforms and books | Separate typed stock items; category/size/edition labels and store pricing |
| Purchase requests and orders | Employee requests, multi-request supplier orders, frozen submission, partial receipts and payment confirmation |
| Approvals | Different-person request/order review, requester/creator exclusion and immutable approved lines |
| Suppliers | School-scoped supplier contact and address register linked to orders |
| Stock issuance | Recipient, purpose and unique reference; atomic stock decrement and duplicate-reference guards |
| Low-stock alerts | Current quantities at/below reorder thresholds in the alerts workspace |
| Depreciation | Cumulative monthly straight-line posting, nonfuture/duplicate guards and protected residual value |
| Maintenance | Private asset maintenance records with follow-up closure |
| Audits | Locked expected/observed stock counts, recorded variance, physical asset-audit records and audit trails |

Stock audits do not silently correct counts. Store stock is reserved at invoice approval and handed over only after confirmed payment. Procurement and depreciation post to the existing Finance ledger; bank transfers/refunds and opening-balance migration remain reviewed external/Finance operations.

## Communications & Engagement

| Requested area | Implemented workflow |
|---|---|
| Announcements | Scoped campaigns, Community Hub inbox posts and current-recipient access |
| Class broadcasts | Explicit class audiences; teachers limited to current assigned classes and in-app sends |
| WhatsApp Business integration | Meta Cloud API approved-template adapter, normalized phone, signed phone-scoped status callback |
| SMS | Termii adapter using verified contact and channel/purpose consent |
| Email | Resend adapter or explicit reuse of existing platform SMTP; old Community email joins consented queue after activation |
| Push notifications | OneSignal adapter and opt-in browser setup/worker; generic sign-in-only payload |
| Templates | Saved subject/body with name/school placeholders, approved provider template/language references |
| Scheduled broadcasts | Draft → scheduled → queue → delivery log; Lagos time, school-serialized cPanel CLI worker and explicit small-batch frontend run |
| Parent–teacher messages | Existing Family and Teacher Portal thread creation, recipient/child checks and existing replies |
| Emergency notices | Pinned in-app notices and opted-in external channels with truthful status tracking |
| Newsletters | Reusable plain-text campaign/template workflow with separate marketing consent |
| Events | Scoped event starts/ends and scheduled notices |
| Polls | Listed choices, eligibility, closing time, once-per-account vote and manager totals |
| Delivery logs | Queued/suppressed/sending/unknown/failed/accepted states and verified WhatsApp sent/delivered/read transitions |
| Credits | Internal unit allowances, unique top-ups, atomic reservation, definite rejection refunds and no uncertain automatic replay |
| Consent management | Per-channel/per-purpose recipient choice, active linked-parent control for student accounts and pre-send recheck |

Provider settings can be saved by the school administrator in encrypted per-school storage. The matching protected encryption key must be backed up. Private server settings may override frontend configuration. Tests simulate provider responses, including timeout/rejection and signed callbacks; no real delivery/provider approval is claimed. Internal budget units do not represent provider tariffs or funded accounts.

## School Website & CMS

| Requested area | Implemented workflow |
|---|---|
| Website themes | Three responsive school themes, school-specific public link and platform homepage preservation |
| Custom domain | Exact-host request, TXT ownership + canonical CNAME verification, server allowlist, explicit cPanel/HTTPS readiness and activation |
| News | Approved plain-text news revisions, escaped rendering and published-history retention |
| Galleries | Reviewed JPEG/PNG/WebP media, consent reference, safe headers and unpublished-media denial |
| Admissions landing pages | Approved landing content, same-school existing open application link and Family payments link |
| Events | Approved dated public event content |
| Staff profiles | Explicit approved public profile content linked to legacy staff; private HR data never auto-published |
| Enquiry forms | CSRF/nonce/honeypot/rate/processing-consent guards and existing Admissions CRM insertion |
| School tours | Capacity-checked dated tours, one place per visitor booking, expiring paid holds and private booking records |
| SEO | Page title, description, sharing metadata and configured canonical URLs independent of untrusted Host headers |
| Testimonials | Consent-referenced editor content and different-person publication |
| Prospectus | Reviewed PDF upload and safe public attachment download |
| Content approval | Draft/submission/different-person publication or rejection; atomic replacement; history and guarded preview |
| Integrated payments | Existing school Paystack configuration, server-side exact verification, printable private tour payment record and Finance advance journal; existing student payment workflow preserved |

No arbitrary HTML or script editor is exposed. Live DNS, cPanel aliasing/TLS, provider accounts, domain ownership, publication rights and real payment/refund reconciliation require operator setup. A late verified payment without tour capacity becomes `paid_review` rather than overbooking. Code rollback retains business records rather than reversing them.
