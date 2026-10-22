# 4.8.0 feature map

Access starts at **School Operations**. Staff self-service requires one explicit employee/account link. Capabilities are school-scoped and checked from the current database. Managers see their own school, drivers their assigned routes/trips, wardens their assigned hostels, and families only explicitly linked children. All writes require CSRF protection.

## Human Resources & Payroll — 17 areas

| Requested area | Implemented workflow |
|---|---|
| Staff records | Reuse legacy staff; explicit HR/account linkage, status and joining date |
| Recruitment | Private applicants, shortlist, offer, hire or reject; hire creates onboarding record |
| Onboarding | Private checklist, reviewed completion, salary and readiness gates |
| Contracts | Dated contract records, signed/ended status, private PDF storage/download |
| Departments | Create departments and change explicit employee department links |
| Attendance | Own clock-in/out with replay guards; existing Welfare staff register |
| Leave | Own date-range request and independent HR review in existing leave register |
| Duty schedules | Dated duties with per-employee overlap rejection and completion/cancellation |
| Salaries | Future monthly basic changes; immutable per-month payroll snapshots |
| Allowances | Exact kobo amounts, taxable/pensionable flags and prospective stop |
| PAYE / pension configuration | School-reviewed progressive annual band widths, relief, pension rates and tax deduction flag |
| Payslips | Independent run approval, own private printable payslip, manual-payment confirmation |
| Advances | Request, independent approval, manual disbursement, reserved recovery and balance tracking |
| Evaluations | Private reviews; only published evaluations visible to employee |
| Professional development | Evidence items with review; existing Teacher Portal PD records shown by linked account |
| Grievances | Private own submissions and HR reviewing/resolved status |
| Exit clearance | HR/Finance/Library/Transport/Boarding checklist, open-payroll/advance gates, explicit linked-account disable |

PAYE configuration is a calculation engine, not statutory filing or advice. Full-month snapshots do not prorate or reconcile YTD tax. A void period stays in the audit history and cannot be regenerated under the same month. Historical calculation snapshots remain unchanged when policy, salary or allowance settings change.

## Transport Management — 14 areas

| Requested area | Implemented workflow |
|---|---|
| Vehicles | Register capacity and plate, active/maintenance/inactive controls |
| Drivers | Explicit employee account, licence and expiry, renewal/contact/status updates |
| Routes | Daily vehicle/driver time conflict checks, active and future-fee settings |
| Stops | Named ordered stops with optional coordinates |
| Student assignments | One active route per student, matching route/stop and seat-capacity guards |
| Fees | Idempotent per-student/period Finance invoices |
| Manifests | Fixed passenger/stop snapshot at trip start; completion requires passenger outcomes |
| Pickup/drop-off notifications | Recorded passenger transitions produce private in-app Family updates |
| Driver interface | Assigned trips/routes, passenger forms, collector details and event reports |
| Optional GPS | Explicit route enablement, manual device read, latest point, bounds/accuracy/rate checks and disable/erase |
| Maintenance | Vehicle maintenance events and reviewed closure; vehicle maintenance state blocks trips |
| Incident logs | Scoped trip/vehicle events and manager closure |
| Route suggestions | Three nearby coordinate-bearing stops with spare capacity; staff-reviewed distance heuristic |
| Authorized handovers | Current approved Family pickup authorization, physical identity confirmation, once-only consumption |

## Hostel & Boarding — 14 areas

| Requested area | Implemented workflow |
|---|---|
| Hostels and rooms | Reuse/configure hostels, assigned wardens, room capacities and registered beds |
| Bed allocation | One active bed per child and one occupant per bed; history retained |
| Fees | Per-student/period Finance invoice with replay protection |
| Check-in/out | Presence state, movement history, approved current permit and physical collector verification |
| Leave permits | Linked family/student or warden request, independent approval, out/returned tracking |
| Visitors | Verified sign-in, student/hostel scope and once-only sign-out |
| Roll calls | Morning/evening marks, authorized-leave validation, absence follow-up notices |
| Warden dashboard | Assigned hostel occupancy, residents/presence and overdue returns |
| Incidents | Private hostel events linked to confidential existing Welfare cases |
| Maintenance | Assigned-hostel maintenance records and closure |
| Welfare | Private resident welfare records and confidential Welfare integration |
| Supplies | Opening/received/issued stock, reorder levels, signed adjustment trail and nonnegative quantity |
| Occupancy | Allocated beds, registered physical beds and room capacity reported separately |
| Meal integration | Menus published to resident families, existing choices, justified staff overrides, once-only serving/fee |

Existing Finance payments/receipts, Family Portal, Teacher/Student portals, Community Hub, WhatsApp handoff, authentication and historical records remain in place. Legacy HR/vehicle/hostel navigation opens the new workspace. Modules directly requested by URL redirect through authenticated `index.php`.
