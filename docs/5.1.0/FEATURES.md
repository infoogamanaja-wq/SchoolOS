# Platform Experience 5.1.0

## A clearer, interactive interface

- Responsive split-screen login and school registration with local glass surfaces, gradients, an animated connection illustration, qualitative “Did you know?” school insights, previous/next/pause controls and reduced-motion support. No invented statistics or dependency on a remote UI CDN.
- Password visibility control, keyboard-accessible forms, visible validation messages, retained nonsensitive form values after errors, clear join/create/sign-in choices and server-side CSRF checks.
- Configured plan/cycle selection with a live price/trial summary, unavailable-cycle feedback and no automatic renewal debit.
- Role-specific **My overview** for school owners, platform administrators, teachers, families, learners, operational staff, admissions and partners. Real school branding/logo is used when configured; light/dark preference persists in the browser.
- Current date/time formatted for **Africa/Lagos / WAT**, task-specific quick actions, smaller grouped owner navigation, useful empty states and a replayable walkthrough.
- Recorded-attendance donut with an explicit denominator, invoice-position infographic, current-session teacher workload bars and actual record-based KPI cards. Confirmed allocations/credits are not labelled bank cash. Empty data are not fabricated.
- Consistent modern shell for existing module screens; existing role and tenant guards remain in place. Module workflows retain their real business fields and approval rules.

## Guided school and user onboarding

**School owners** see an eight-check launch journey: identity/branding, classes/session/subjects, student records, teacher allocations, family/student links, Finance configuration, workspace activation and school privacy review. Checks derive from real configuration. Priority alerts identify unplaced learners, unlinked accounts, unassigned teachers and approaching self-service subscription expiry. Readiness checks are prompts, not a certification that every record is correct.

**New school registration** is a transaction that creates tenant, owner and configured subscription together. Active plans and configured trials are used, as requested. Trials, no-trial paid access, explicit free plans, expiry, renewal and independent administrative suspension have working server-side paths. Exact NGN/reference/amount verification is idempotent under concurrency. The existing platform verifier/webhook path delegates these payments to the same once-only logic.

**School members** can be administrator-created or request a role and wait for school approval, as requested. Public school listing is opt-in; private invitation codes are supported. New requests stay inactive and never infer child records or staff duties. Verified approval/recovery issues a temporary 72-hour credential, replaces an unverified request password and requires a personal password change at first sign-in. School owner recovery requires platform verification.

**Walkthroughs** explain what each part does and why setup matters. Native modal controls support next/back/close, focus handling and keyboard dismissal. Completion is saved per account after activation; it can be replayed from the header. A helpful overview does not unlock protected records for an unlinked account.

## Connected demonstration accounts

The login page supplies fourteen autofill choices:

| Choice | Demonstration |
|---|---|
| School owner | School overview, setup, accounts, Finance, approvals and workspaces |
| Teacher | Current class/subjects, attendance, homework, draft scores, timetable and review |
| Parent / guardian | Two linked learners, published results, attendance, fees, family requests and posts |
| Student | Same linked learner, homework, practice CBT, grades, attendance and library |
| Driver | Assigned Sunrise route and current-date passenger manifest |
| Warden | Harmony hostel, allocated beds and linked boarders |
| HR & payroll | Connected active employees and salaries; existing approval workflow |
| Librarian | Catalogue and a learner's pending request |
| School store | Stock, store products and procurement workflows |
| Communications | Shared Community Hub posts and website content authoring |
| Admissions | Fictional applicant and guardian records |
| Partner | Fictional school referral |
| Platform overview | Read-only sandbox platform views |
| School reviewer | Separate fictional school administrator for independent reviews |

Data contain 24 fictional learners across nursery, primary and junior secondary classes; linked siblings; 14 days of attendance; published approved assessment results; editable later assessment components; homework/lessons and CBT; balanced invoices/receipts; library, stock, HR, transport and boarding records; family calendar/consent/survey/meal posts; a teacher booking slot and reviewed sample school news. Dates are generated at provisioning/refresh, not copied from a production school.

A separate database, marker, encrypted connection configuration, private session storage and distinct cookies isolate demo work. Known fictional passwords do not authenticate into live accounts. Live provider I/O, uploads, native mail, host controls and role changes are disabled in shared demos. The platform demo is read-only. Optional guarded refresh restores the dataset without copying/clearing live school records.

## Operational scope

This release uses the existing PHP 8.4/MariaDB script and frontend Update Manager. It preserves Finance, Family, Learning, Operations, Services and Intelligence integrations. Explicit additive activation and workspace health checks replace dead ends caused by missing tables.

Real gateway credentials/settlement, messaging accounts/consent/templates/credits, scheduled workers, DNS/TLS, privacy decisions and licensed integrations remain actual configuration requirements. Optional innovations stay subject to their existing enablement/review rules. This is not a promise that an unconfigured provider, future roadmap item or every legacy catalogue control has become a live automatic integration. See the audit and deployment boundaries before rollout.
