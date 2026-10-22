# Validation — School Services 4.9.0

Validated on 2026-10-22 using **PHP 8.4.24**, **MariaDB 11.8.6 and 10.11.18**, and local **Apache 2.4.68 / FastCGI**. Databases contain synthetic fixtures only and use private local sockets. No production cPanel server, private production credential, live message recipient or real payment was used.

## Executed checks

| Suite | Passed | Evidence under test-output/ |
|---|---:|---|
| New domain workflows, permissions, accounting, provider/DNS simulations and rendering | 150 | services.txt |
| HTTP role screens, real media upload/download, public forms, private preview, encrypted settings, CLI and old routes | 108 | http.txt |
| Concurrent licence, stock, receipt, depreciation, delivery, tour and payment operations | 8 | concurrency.txt |
| QR matrix comparison with independent encoder plus ZXing decoding | 3 | qr.txt |
| Actual frontend two-stage install, activation, all manager views, independent CMS publication, exact rollback and reinstall | 55 | package-apache.txt |
| Apache homepage/rewrite/private storage/config/archives and authenticated Family routing | 9 | apache-routing.txt |
| Teacher/Student domain regression | 131 | regression/learning-domain.txt |
| Teacher/Student HTTP regression | 55 | regression/learning-http.txt |
| Learning concurrency regression | 4 | regression/learning-concurrency.txt |
| HR/Transport/Boarding domain regression | 128 | regression/operations-domain.txt |
| HR/Transport/Boarding HTTP regression | 90 | regression/operations-http.txt |
| Operations concurrency regression | 6 | regression/operations-concurrency.txt |
| Existing Family domain regression | 61 | regression/family-domain.txt |
| Existing updater adversarial/recovery regression | 24 | regression/updater.txt |
| **Primary assertions** | **832** | Logs above |
| **MariaDB 10.11 compatibility: new domain + concurrency** | **158** | maria10-services.txt, maria10-services_concurrency.txt |
| **PHP syntax** | **34 source files** | syntax.txt |

New ZIP member sets, payload SHA-256 values, current-source/deployed equality and exclusion of private configuration, storage, install/schema and `.htaccess` files were checked (manifests.txt). The six earlier published ZIPs remain immutable. `git diff --check` passes. Python QR/image test dependencies are not PHP runtime dependencies and are not shipped in an update payload.

## Findings and fixes established by these checks

- Existing `books` and `lp_library_loans` remain the canonical physical lending records. First-reservation priority is enforced in both new librarian issuance and the old Learning Portal issue handler. Replay guards, negative-stock/copy rejection, loss/recovery, frozen fines, licence periods and concurrent final-seat claims are tested.
- Entered ISBN10/13 values pass checksum validation. The locally generated QR matches an independent byte-mode version-2-L encoder and decodes to the exact catalogue key; no external QR generation service receives school data.
- Approved purchase lines freeze quantity/unit cost. Different-person approvals, partial/duplicate/over receipts, once-only supplier journals, paid store handover, audit variance and nonnegative stock are exercised. Two independent workers cannot issue the final unit or receive more than an approved order. Same-reference issuance retries succeed without decrementing twice.
- Straight-line depreciation is checked against a known monthly amount. Concurrent duplicate period posting produces one record/journal, and residual/future/earlier-period guards remain enforced.
- Message audience resolution is distinct from Community Hub's administrator read privilege: an administrator's ability to moderate posts does not implicitly add them as an external recipient. Assigned-class boundaries, recipient consent, current guardian links, revoked consent after queuing, future scheduling, newsletter marketing purpose, contact verification and secret non-disclosure are exercised.
- External outcomes are distinguished: API acceptance, definite rejection/refund, uncertain transport with no replay, in-app storage, and signed correct-school WhatsApp delivery transitions. Concurrent school workers produce one simulated provider call and one credit reservation. Existing SMTP is an explicit adapter; its simulated acceptance is not labelled delivery. Existing Community email enters the same queue/guards after activation.
- Frontend provider settings are encrypted with AES-256-GCM, scoped by school, and never redisplayed. Tests compare saved ciphertext against the test secret, verify other-school isolation and private server override precedence, reject control characters, and remove/restore a synthetic key temporarily to prove that missing-key access fails closed without silently generating a replacement over encrypted records.
- PHP and the MariaDB connection now use Lagos time consistently. This fixes immediate/scheduled campaign and hold comparisons when the MariaDB server's own timezone differs. It sets the SQL session timezone, not database rows.
- CMS revisions remain private until independently approved. Replacements publish atomically; approved images/PDFs have guarded MIME/header behavior, unpublished/cross-school files/previews are denied, disguised executables are rejected and public text is escaped. Public enquiries enter the existing CRM once; form replay is rejected.
- Domain tests check ownership TXT/CNAME proof and exact allowlisting using a resolver simulation. Tour tests cover holds, capacity under concurrent booking, exact payment verification, one journal under parallel verification, and a late paid booking flagged for review when capacity has been taken.
- The actual 4.8.1 support ZIP leaves the known working 4.8.0 index unchanged. The 4.9.0 frontend installation matches its manifest. Rollback restores the exact previous index **and Learning Portal** while retaining all new module/worker dependencies. Reinstallation recovers the approved public website/content record. Family, Finance, Operations and private configuration bytes remain unchanged by the main ZIP.
- Synthetic existing student records, password hashes, unrelated-school books and historical Finance invoices are compared before/after. Existing portal regressions run on separate fresh fixtures and pass.

## Accounting and external-service limits

Library fines/losses and store orders create existing Finance invoices and receivable/revenue journals (`1100` / `4100`). Existing Finance handles collection and receipts. Procurement receipt debits inventory `1200`, credits supplier payable `2000`; confirmed external supplier payment debits `2000`, credits cash/bank `1000`. Depreciation debits `5200`, credits accumulated depreciation `1590`. Verified tour payment debits `1000`, credits tour advance liability `2110` once. Tests verify balanced posting and replay protection.

These journal integrations do not automatically create `fn_expenses` rows. Existing expense-only cash/budget widgets therefore exclude these postings. Opening stock/asset balances, stock issue/adjustment valuation, store cost-of-goods expense, tax treatment, earned-tour revenue recognition, payable reversals, refunds and legacy balance migration require reviewed Finance/accounting handling; the update does not claim a complete inventory cost-accounting or statutory reporting system. Do not duplicate an already posted supplier/tour transaction through another payment path.

External provider tests use injected simulated responses; no Meta approval, Termii/Resend account funding, live SMTP acceptance, real OneSignal subscription, physical-device notification or real Paystack transaction is claimed. WhatsApp callbacks are locally HMAC tested. Email/SMS/push accepted status is not confirmed delivery. Missing credentials, insufficient internal units, opt-out, provider uncertainty and physical device/browser restrictions affect actual sending. No worker starts automatically during installation.

DNS tests do not provision a live domain, cPanel alias or certificate. Ebook seat controls do not establish publisher permission or implement DRM. Overdue reminders and inventory alerts are in-app/staff-triggered workspaces, not an unconfigured external notification daemon. Fines freeze at assessment; physical books remain title-level copy counts. These limits are described in the deployment guide.

Rollback preserves business tables, messages, invoices, stock, credentials and payment history; it is not a transactional undo of business activity. No production host was accessed and no hosting-related deletion cause was inferred. Local update/rollback evidence does not establish a permanent resolution of provider quarantine or deletion behavior without production logs.
