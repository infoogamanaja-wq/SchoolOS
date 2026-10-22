# SchoolOS Nigeria — Teacher & Student Portals 4.7.0

The latest release adds the requested **17 Teacher Portal** and **14 Student Portal** areas on top of the working Family Portal release. It preserves existing Finance, Family Space, Community Hub, WhatsApp handoff, authentication and records.

Read the [4.7.0 deployment guide](docs/4.7.0/DEPLOYMENT.md), [feature map](docs/4.7.0/FEATURES.md) and [validation evidence](docs/4.7.0/VALIDATION.md).

Install on a backed-up staging clone through **Platform Super Admin → Updates & Plugins**, in this order:

1. `dist/SchoolOS-4.6.6-Learning-Updater.zip` — permits the new module; leaves the working index unchanged.
2. `dist/SchoolOS-4.7.0-Teacher-Student-Portals.zip` — installs the tested portal/router update.
3. As a school administrator, open **Learning Portals → Activate Learning Portals**. Configure teacher class/subject/session allocations and explicit student account links using the existing school administration screens.

AI is optional and disabled by default. Real provider use needs the school's private `providers.ai_api_key`, outbound HTTPS and school enablement. Automated AI tests use simulated provider responses; no live model/account availability is claimed.

`python3 tools/build_release.py` builds the latest packages and checksum list. Historical 4.6.4/4.6.5 ZIPs remain immutable. See [tests/README.md](tests/README.md) for isolated test commands. This is the PHP 8.4/MariaDB/cPanel script application requested by the user; production credentials, database contents, uploaded files and historical live backups are excluded from Git and release payloads.

Earlier Family Portal findings and deployment evidence remain in [docs/AUDIT.md](docs/AUDIT.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) and [docs/VALIDATION.md](docs/VALIDATION.md). The product blueprint remains product context, not executable deployment instructions. No production server was accessed by this work.
