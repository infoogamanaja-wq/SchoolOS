# SchoolOS Nigeria — School Operations 4.8.0

The latest release adds **17 HR & Payroll**, **14 Transport Management**, and **14 Hostel & Boarding** areas on top of the working 4.7.0 portals. Existing Finance, Family, Teacher/Student, Community Hub, WhatsApp handoff, authentication and records remain in place.

Read the [4.8.0 deployment guide](docs/4.8.0/DEPLOYMENT.md), [feature map](docs/4.8.0/FEATURES.md) and [validation evidence](docs/4.8.0/VALIDATION.md). Prior Teacher/Student documentation remains in [docs/4.7.0](docs/4.7.0/DEPLOYMENT.md).

On a backed-up staging clone of **4.7.0**, install through **Platform Super Admin → Updates & Plugins**, in order:

1. `dist/SchoolOS-4.7.1-Operations-Updater.zip` — permits the four new modules; leaves the working index unchanged.
2. `dist/SchoolOS-4.8.0-HR-Transport-Boarding.zip` — installs the validated update.
3. As a school administrator, open **School Operations → Activate School Operations**, then configure access, explicit employee links, reviewed payroll policy, routes and hostels.

Payroll records manual payments; it does not transfer funds. PAYE/pension rules require school review. Notifications are in-app; optional foreground GPS and route suggestions have the limits described in the deployment guide. **602 primary assertions**, **134 second-version compatibility assertions** and syntax checks of **25 PHP files** passed in isolation; see the evidence for scope.

AI is optional and disabled by default. Real provider use needs the school's private `providers.ai_api_key`, outbound HTTPS and school enablement. Automated AI tests use simulated provider responses; no live model/account availability is claimed.

`python3 tools/build_release.py` builds the latest packages and checksum list. Historical 4.6.4–4.7.0 ZIPs remain immutable. See [tests/README.md](tests/README.md) for isolated test commands. This is the PHP 8.4/MariaDB/cPanel script application requested by the user; production credentials, database contents, uploaded files and historical live backups are excluded from Git and release payloads.

Earlier Family Portal findings and deployment evidence remain in [docs/AUDIT.md](docs/AUDIT.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) and [docs/VALIDATION.md](docs/VALIDATION.md). The product blueprint remains product context, not executable deployment instructions. No production server was accessed by this work.
