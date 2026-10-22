# School Intelligence 5.0.0 — feature map and operational limits

This release extends the installed 4.9.0 PHP/MariaDB application. It uses existing student/account links, academic allocations, Finance journals, Community Hub delivery queue, transport manifests and school permissions. Existing records are retained. Features below are implemented workflows with explicit boundaries, not claims of live provider or legal approval.

## Reporting & Analytics

| Requested area | Delivered behavior |
|---|---|
| Executive dashboards; enrolment | Current roster/active-profile/application/recorded-attendance KPIs; per-class totals and dated admissions. |
| Admission conversion | Application cohorts grouped by CRM stage; conversion counts linked enrolled students. |
| Academic trends | Published approved normalized assessment components grouped by subject, session and term. Component averages differ from weighted report-card totals. |
| Attendance | Recorded present/late/absent counts and percentages; missing days never assumed absent. Historical grouping uses current class. |
| Fee collections and debt | Confirmed external collections separated from internal credit/prepaid allocation. Net billing and current outstanding on invoices created in the selected period; not reconstructed historical closing debt. |
| Teacher workload | Current active allocations, periods and weekly minutes from existing timetable. |
| Comparisons; year-on-year | Selected and prior-year date windows; explicit immutable active-roster cohort snapshots. Current-state metrics remain labelled current. |
| Retention | Intersection of consecutive saved cohorts, preserving snapshot class labels. Missing historical cohorts are not invented; absence from a cohort is not automatically dropout. |
| HR; transport/hostel | Separate HR capability for aggregate employment/paid payroll; current transport/boarding counts and incident totals. No individual payroll/incident detail in report/API exports. |
| Custom report builder | Fixed datasets, allowlisted ordered columns, date/class filters. No arbitrary SQL. |
| Scheduled exports | School-scoped CLI cron, rolling windows, rechecked owner permissions, once-per-due-date private CSV records, 1–30 day retention and formula escaping. No automatic email attachments. |
| Early-warning indicators | Explainable attendance, approved performance and overdue homework indicators, evidence and human disposition. |

Reports are descriptive, not statistical causal claims. Executive/HR/Finance/operations/workload metrics do not apply every explorer class/date filter: labels identify the population and whether data are current. Reconcile Finance reports with the ledger: wallet funding/cafeteria sales and restricted fundraising receipts appear in their own ledgers/journals, not legacy tuition payment totals.

## Differentiating innovations

| Innovation | Implemented workflow and boundary |
|---|---|
| AI School Copilot | Permission-aware natural-language intent selects fixed query tools. Families see linked-child balances/attendance; teachers see assigned teaching; managers need dataset capabilities. Optional external AI receives numeric aggregates only, not names, child-level facts or raw questions. Five provider summaries/account/day. Immutable message/report drafts require a different reviewer, current access and explicit once-only execution. No generated SQL or autonomous money/grade actions. |
| WhatsApp-first | Existing HMAC-verified Meta callback accepts exact BALANCE, ATTENDANCE, PAYMENTS, HELP and STOP commands. Verified unique parent phone, active account/links, consent, approved school flow and Meta template required. Replies enter existing credited provider queue; payment portal links require login. Attendance replies use recorded statuses. Existing broadcasts provide scheduled attendance alerts. STOP revokes WhatsApp consent; messages never confirm payment. |
| Offline teacher workspace | Trusted-device opt-in, AES-GCM encrypted IndexedDB snapshot/queue with PBKDF2 passphrase; assigned class, selected recent attendance day and draft allocated assessments only. Snapshot unlock expires after seven days; server requires current login, scope, CSRF, date bounds and matching base versions. Replay-safe event IDs and conflicts retained for human review. Static shell has its own service-worker subdirectory, preserving push integration. No general offline login, Finance or school-wide database cache. |
| Smart pickup verification | Linked guardian issues/rotates 5–30 minute credential for today's approved pickup request. Only hashes stored; QR/text displayed once. Assigned staff/driver/warden and physical identity confirmation required. One-time consumption, expiry, revocation and transport handover integration. Ambiguous multiple live trips require manifest-specific handling. Boarding leave permits remain separate. |
| Student success alerts | Recent vs previous recorded attendance, latest four published approved components, and overdue homework completion. Transparent thresholds and evidence; human review/support note. No automated sanctions, diagnosis, promotion or external sending. |
| Visual report designer | Drag or move approved blocks; immutable nursery/primary/secondary designs, CA/exam weights, descending grade bands, promotion-review threshold. Separate approval. Nursery approved observations; primary/secondary complete published weighted results. Browser print/PDF, not a proprietary PDF engine. Attendance is all recorded days, clearly labelled; historical former-class reconstruction is not supplied. |
| Financial forecasting | Low/base/high scenarios from actual receivables, declared horizon, collection assumption ±15 percentage points, opening cash and outflows. Explicit shortfall estimate; no promise of collection or trained predictive model. |
| Smart timetable | Teacher/class/room conflicts, room capacity, approved allocation, permitted slots, teacher unavailability. Bounded heuristic/backtracking proposal (40 allocations, 60 added periods, 100 slots, 50 rooms, 20,000 search nodes); independent review, baseline-change detection, serialized explicit apply. Preserves existing periods; no claim of global optimum. |
| Digital school wallet | School-operated NGN prepaid liability ledger, disabled until review. Linked parent policy, daily limit, server-priced cafeteria items and school-store/meal invoice settlement; balance locks and idempotent references. Independently verified bank funding or exact Paystack NGN verification; balanced Finance journals. Cafeteria-only credit reversal by different administrator. No cash-out, P2P, third-party merchant network or automatic bank refunds. Provider contracts/regulatory assessment remain prerequisites where applicable. |
| Alumni and scholarships | Consented adult verified directory, family mentoring requests with employee supervisor, approved fundraising purposes and independently bank-verified restricted donations. Existing CMS payment workflow remains available for online gifts. Scholarship windows/criteria/budgets, family applications, independent award review and once-only school-admin fee waiver. No unsupervised adult-child messaging or automatic cash award. |
| Accreditation | Private PDF/image evidence up to 3 MB, authority/source/expiry, independent verification, assigned deadlines and evidence-backed completion. No automatic official accreditation certification. |
| School group headquarters | Explicit school invitations, each school's aggregate-sharing consent, dataset restrictions, analyst grants, revocation, consolidated approved aggregates, reviewed HQ policy and local adoption record. No cross-school individual records or automatic local policy overwrite. |
| Plugin ecosystem | School-approved declarative integration catalogue, semantic versions, read-only aggregate API v1, independent reviewer, hashed expiring/revocable tokens, current permission recheck and 60 requests/minute. No uploaded PHP, arbitrary SQL, remote code execution or unrestricted write APIs. |

## Nigeria-specific requirements

| Requirement | Behavior |
|---|---|
| NERDC versions / school subjects | Versioned NERDC or school references with explicit school subject IDs, independent approval and class policy binding. Official curriculum content is supplied/reviewed by the school, not inferred or bundled as authoritative. |
| CA/exam, promotion, report cards | Configurable weights that must match actual published subject assessments; level-specific formats and school grade bands. Promotion shown as human review, retaining existing approved promotion workflow. |
| Naira, bank transfer, Paystack, instalments | Integer-kobo Finance preserved; partial tuition payments/instalments and receipts unchanged. New prepaid and scholarship entries distinguish external cash, liabilities and fee waivers. No live payment used in validation. |
| Low-bandwidth Android/PWA | Existing responsive application retained; small selective offline shell with text controls and mobile move buttons. HTTPS required for service worker/crypto. Actual Android device, intermittent network and assistive-technology acceptance testing remain deployment checks. |
| NDPA 2023 / children | Scoped roles, private exports/evidence, encrypted device capture, consent/review controls, processing register with lawful basis, child-data flag, retention, processors/transfers and DPIA reference. Identity-checked access/correction/erasure/restriction request workflow. Bounded own-account/child access response; full subject-access response and record-specific erasure/correction require school privacy review. No automatic deletion of statutory/financial records; no legal certification. |
| State-specific configuration | All 36 states and FCT; explicitly entered dates/holidays, inspection notes and source reference; binds to class curriculum/report policy. No invented official dates or automatically downloaded state rules. |

## Privacy and operation

Disable AI/offline/prepaid/token enforcement until the school reviews the intended workflow. Minimize free text and uploaded evidence. Small aggregate cohorts can still identify people; keep aggregate APIs private and assess disclosure risk. Staff need training, backups, scoped account links and an incident procedure. Existing Finance PAYE/pension/provider rules are unchanged.

A school administrator's capability is broad within their school; platform administrator status does not itself grant school Intelligence access. Independent approval requires another account/person with the applicable capability. Schools should avoid shared accounts and record actual review evidence.

On cPanel/FastCGI configurations that strip the HTTP Authorization header, API v1 also accepts the same secret in `X-SchoolOS-Token: TOKEN`. Use HTTPS and never send either credential in a URL.
