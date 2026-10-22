# SchoolOS Nigeria — School Intelligence 5.0.0

The final feature release adds Reporting & Analytics, permission-aware Copilot, reviewed WhatsApp workflows, encrypted selective teacher offline capture, smart pickup, student success alerts, configurable Nigerian report cards/curricula/state calendars, forecasting, timetable proposals, prepaid school credits, alumni/scholarships, accreditation, school-group headquarters and approved read-only integrations.

Read the [deployment guide](docs/5.0.0/DEPLOYMENT.md), [feature map and boundaries](docs/5.0.0/FEATURES.md), and [validation evidence](docs/5.0.0/VALIDATION.md).

On a backed-up staging clone of **4.9.0**, use **Platform Super Admin → Updates & Plugins**, in order:

1. `dist/SchoolOS-4.9.1-Intelligence-Updater.zip` — updater support; leaves the working index untouched.
2. `dist/SchoolOS-5.0.0-Intelligence-Innovations.zip` — main release.
3. As school administrator, open **School Intelligence → Activate School Intelligence**, then assign capabilities and review optional settings.

**1,056 primary assertions**, **119 MariaDB 10.11 compatibility assertions**, and **43 PHP syntax checks** passed locally, including actual frontend package installation, exact entry-point/module rollback and preserved-record reinstall. Existing Finance, Family, Learning, HR, Transport, Boarding, Library, Inventory, Engagement and CMS records are retained.

AI/offline/prepaid/mandatory pickup tokens are disabled until school review. AI/provider summaries, payment verification, WhatsApp delivery, financial arrangements and NDPA controls have documented operational limits. Live providers, production cPanel and actual Android devices were not exercised. The app supports these workflows; it does not certify legal compliance, global timetable optimality or guaranteed financial forecasts.

The [4.9.0 School Services guide](docs/4.9.0/DEPLOYMENT.md) remains available for the previous release. Earlier versions must be upgraded in sequence. Checksums are in `dist/SHA256SUMS`. These ZIPs update an existing installation; they are not standalone installers.

Prior [4.8.0 Operations](docs/4.8.0/DEPLOYMENT.md) and [4.7.0 Learning](docs/4.7.0/DEPLOYMENT.md) guides remain available.

AI is optional and disabled by default. Existing Teacher/Student AI uses the school's private `providers.ai_api_key`; Intelligence Copilot uses its separately encrypted school credential. Both require outbound HTTPS and explicit school enablement. Automated AI tests use simulated provider responses; no live model/account availability is claimed.

`python3 tools/build_release.py` builds the latest packages and checksum list. Historical 4.6.4–4.9.0 ZIPs remain immutable. See [tests/README.md](tests/README.md) for isolated test commands. This is the PHP 8.4/MariaDB/cPanel script application requested by the user; production credentials, database contents, uploaded files and historical live backups are excluded from Git and release payloads.

Earlier Family Portal findings and deployment evidence remain in [docs/AUDIT.md](docs/AUDIT.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) and [docs/VALIDATION.md](docs/VALIDATION.md). The product blueprint remains product context, not executable deployment instructions. No production server was accessed by this work.
