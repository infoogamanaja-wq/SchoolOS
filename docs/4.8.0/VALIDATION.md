# Validation — School Operations 4.8.0

Validated 2026-10-22 using PHP **8.4.24**, MariaDB **11.8.6** and **10.11.18**, and local Apache **2.4.68** with PHP FastCGI. All fixtures are synthetic, on private local sockets with MariaDB TCP disabled. The user's production installation, database, cPanel configuration and external providers were not accessed.

## Executed checks

| Suite | Passed | Evidence |
|---|---:|---|
| HR/Transport/Boarding domain and scoped rendering | 128 | test-output/operations.txt |
| HTTP roles, all screens, actual PDF upload, private downloads, old routes and integrations | 90 | test-output/http.txt |
| Concurrent payroll posting, last seat/bed, fee retry and supplies | 6 | test-output/concurrency.txt |
| Actual two-stage frontend ZIP install, activation, all manager views, rollback and reinstall on Apache | 50 | test-output/package-apache.txt |
| Apache DirectoryIndex/rewrite/private paths/authenticated Family routing | 9 | test-output/apache-routing.txt |
| Existing Teacher/Student domain regression | 131 | test-output/regression/learning.txt |
| Existing Teacher/Student HTTP regression | 55 | test-output/regression/http.txt |
| Existing learning concurrency regression | 4 | test-output/regression/concurrency.txt |
| Existing 4.7.0 package upgrade/rollback regression | 44 | test-output/regression/package-apache.txt |
| Existing updater adversarial/recovery regression | 24 | test-output/regression/updater.txt |
| Existing Family Portal regression on a separate fresh database | 61 | test-output/regression/parent-regression.txt |
| **Primary automated assertions** | **602** | Logs above |
| MariaDB 10.11 domain/concurrency compatibility | **134** | test-output/maria10-operations.php.txt, maria10-operations_concurrency.php.txt |
| PHP syntax | **25 files** | test-output/syntax.txt |

Package member sets, all payload SHA-256 values, exclusions of configuration/install/schema/.htaccess files, and deployed source equality were also verified. Earlier four published ZIPs are unchanged. The builder freezes historical ZIPs rather than generating old versions from new source.

## What the evidence establishes

- A synthetic working 4.7.0 installation accepts the 4.7.1 whitelist update without changing its entry point, then installs the actual 4.8.0 package through the super administrator frontend. The new tables require explicit school-admin activation. All requested manager views render through PHP/Apache.
- Rollback restores the exact prior `index.php` hash and leaves Family, Learning and all new module files present. Reinstallation accepts existing additive tables. Existing configuration and Family/Learning/Finance module bytes are preserved by the new package.
- Payroll uses integer kobo. A known progressive-band vector checks pension, annual taxable pay, tax rounding and net salary. Different-user approval, approved-snapshot immutability, reserved advance recovery, once-only balanced journals and concurrency are tested. Invalid amounts/rates, negative-net configuration and replayed payment are rejected.
- Existing student records, password hashes and Finance invoices are compared before/after domain tests. Transport/boarding invoices and meal charges reach existing Finance. Parent homework, learning, Community Hub and Finance routes remain available. No existing parent, learning, finance, WhatsApp or authentication implementation was replaced.
- A private contract is uploaded using multipart HTTP, retrieved by the linked employee and denied to a peer, parent and other school. Payslips have the same scope and no-store response policy. Unpublished evaluations are filtered. Driver/warden/tenant/child boundaries and CSRF denial are exercised.
- Route/driver schedule overlap, manifest completion, current handover authorization and physical-check gate, bed/room capacity, check-in/out, permit lifecycle, visitor replay, roll-call updates, confidential Welfare integration, stock bounds, meal choice and once-only charging are exercised. Concurrent one-seat and one-bed requests cannot overallocate.

## Accounting and operational limits

Payroll journal account codes: `1000` cash/bank, `1300` staff advance receivable, `2200` PAYE payable, `2210` pension payable, `5100` salary cost, `5110` employer pension cost. Advance disbursement debits receivable/credits cash; net salary, employee deductions and recoveries balance gross salary cost; employer pension adds its own cost/liability. Payroll is visible in the existing journal/trial balance. The existing paid-expense cash/budget widgets use `fn_expenses` and therefore exclude payroll; do not duplicate the payment in that module. Invoice journal behavior uses the existing `1100` receivable / `4100` revenue convention.

No bank transfer, tax filing, pension remittance, automatic proration, YTD reconciliation, live WhatsApp/SMS delivery, live payment gateway transaction, continuous GPS tracking, geocoding or road-route optimization was tested or added. PAYE/pension rules require school review; no claim of automatic Nigerian statutory compliance is made. GPS tests validate application storage/permission boundaries, not physical location authenticity or device availability. Human staff must check collector identities, route safety, meal allergies and welfare follow-up.

No production host was accessed and no hosting-side deletion cause was inferred. These tests establish local code/update/rollback behavior, not a permanent resolution of any provider quarantine/deletion process. Production logs remain necessary for that conclusion.
