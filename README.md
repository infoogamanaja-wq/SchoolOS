# SchoolOS Nigeria — School Services 4.9.0

The latest release adds **Library Management**, **Inventory/Procurement/Assets**, **Communications/Engagement** and **School Website/CMS** on the working 4.8.0 application. Existing Family, Teacher/Student, HR, Transport, Boarding, Finance and Community Hub records remain in place.

Read the [4.9.0 deployment guide](docs/4.9.0/DEPLOYMENT.md), [feature map](docs/4.9.0/FEATURES.md) and [validation evidence](docs/4.9.0/VALIDATION.md).

On a backed-up staging clone of **4.8.0**, install through **Platform Super Admin → Updates & Plugins**, in order:

1. `dist/SchoolOS-4.8.1-Services-Updater.zip` — whitelist support; leaves the working index unchanged.
2. `dist/SchoolOS-4.9.0-Library-Inventory-Engagement-CMS.zip` — validated main update.
3. As school administrator, open **School Services → Activate School Services**, then assign capabilities and configure each module.

Provider settings can be saved in the school-admin frontend with encrypted storage. Consent, provider setup and a cPanel cron job are required for scheduled external messages; internal credits are budget units, not provider payments. CMS needs the canonical HTTPS installation address and explicit cPanel/DNS/TLS setup for custom aliases. Live providers/domains were not exercised.

**832 primary assertions**, **158 second-version MariaDB assertions**, and **34 PHP syntax checks** passed in isolation, including actual frontend ZIP installation, exact-index rollback and preserved-record reinstallation. See the evidence for scope and accounting/provider limits.

Prior [4.8.0 Operations](docs/4.8.0/DEPLOYMENT.md) and [4.7.0 Learning](docs/4.7.0/DEPLOYMENT.md) guides remain available.

AI is optional and disabled by default. Real provider use needs the school's private `providers.ai_api_key`, outbound HTTPS and school enablement. Automated AI tests use simulated provider responses; no live model/account availability is claimed.

`python3 tools/build_release.py` builds the latest packages and checksum list. Historical 4.6.4–4.8.0 ZIPs remain immutable. See [tests/README.md](tests/README.md) for isolated test commands. This is the PHP 8.4/MariaDB/cPanel script application requested by the user; production credentials, database contents, uploaded files and historical live backups are excluded from Git and release payloads.

Earlier Family Portal findings and deployment evidence remain in [docs/AUDIT.md](docs/AUDIT.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) and [docs/VALIDATION.md](docs/VALIDATION.md). The product blueprint remains product context, not executable deployment instructions. No production server was accessed by this work.
