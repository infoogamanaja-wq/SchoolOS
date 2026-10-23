# SchoolOS Nigeria — Role Portals & Live Learning 5.3.0

Family, teacher and learner workspaces now have focused navigation, verified in-app conversations, daily meal choices, CA/exam results, branded receipts, prominent updates and improved dark mode. Live lessons support existing Zoom/Meet invitations and a small-group in-app teacher broadcast; reliable remote video requires a separately configured TURN relay.

On a backed-up **5.2.1 staging installation**, install `dist/SchoolOS-5.2.2-Portal-Updater.zip`, then `dist/SchoolOS-5.3.0-Role-Portals-LMS.zip` through **Updates & Plugins**. Activate installed workspaces in **Setup & Accounts**. Existing configured demos migrate on their next connection; an unconfigured demo still needs its own empty cPanel database. Production was not accessed.

Read [deployment and demo setup](docs/5.3.0/DEPLOYMENT.md), [release scope](docs/5.3.0/RELEASE.md) and [validation evidence](docs/5.3.0/VALIDATION.md). Preview the [parent night portal](docs/5.3.0/test-output/parent-night.png), [teacher studio](docs/5.3.0/test-output/teacher-night.png) and [branded receipt](docs/5.3.0/test-output/branded-receipt.png).

## Earlier releases

A six-file frontend patch adds visible academic doodle movement, animated headline text, scroll reveals, hover spotlights, a persistent light/night switch and **36 challenges across six topics**. Public pages, login and dashboards now share the same SchoolOS mark. School-specific uploaded logos remain separate.

On an existing **5.2.0** installation, test on staging and install `dist/SchoolOS-5.2.1-Interactive-Website.zip` through Super Admin → Updates & Plugins. No new updater support package or database migration is needed. Read the [release and validation notes](docs/5.2.1/RELEASE.md) and preview the [night website](docs/5.2.1/test-output/website-night-desktop.png).

## Website & Affiliates 5.2.0

A redesigned public website with responsive mobile layouts, working dashboard snapshots, academic facts, an interactive quiz, clear school onboarding paths and complete public information pages. Eighteen role guides are available as accessible pages and downloadable server-generated PDFs.

The built-in affiliate module is configurable and disabled until the platform operator installs/enables it. Approved partners receive personal referral links and a dedicated commission/payout workspace. Verified subscription payments create credits; withdrawals reserve funds and require Super Admin approval before provider submission. Test and live funds are separated.

Read [deployment](docs/5.2.0/DEPLOYMENT.md), [features](docs/5.2.0/FEATURES.md), [audit and limits](docs/5.2.0/AUDIT.md) and [validation](docs/5.2.0/VALIDATION.md). Preview the [desktop website](docs/5.2.0/test-output/website-desktop.png) and [mobile website](docs/5.2.0/test-output/website-mobile.png).

On a backed-up staging copy of **5.1.0**, install through **Platform Super Admin → Updates & Plugins**, in order:

1. `dist/SchoolOS-5.1.1-Website-Affiliate-Updater.zip` — updater support; preserves the stable entry point.
2. `dist/SchoolOS-5.2.0-Website-Affiliates.zip` — main update.
3. Open **Website & Affiliates**, install its additive tables, choose commission/hold/minimum terms and test provider callbacks, bank setup and payouts before enabling live participation. Operator details default to Vendorhub Global Concept / admin@getschoolos.com.ng.

**1,395 primary assertions**, **257 MariaDB compatibility assertions** and **56 PHP syntax checks** passed locally. Real browser and frontend installation/rollback evidence is included. No production deployment or live provider transfer was performed. See the deployment guide for required provider/cron configuration.

The previous [5.1.0 Experience guide](docs/5.1.0/DEPLOYMENT.md) documents registration, approved member access, guided school setup and isolated connected demo accounts. Existing school modules and records are retained. These packages update an existing application and are not standalone installers. Historical published ZIPs remain immutable; checksums are in `dist/SHA256SUMS`.

The previous [5.0.0 Intelligence guide](docs/5.0.0/DEPLOYMENT.md) and its [feature boundaries](docs/5.0.0/FEATURES.md) remain available. Upgrade earlier installations in sequence. The ZIPs update an existing application and are not standalone installers. Check `dist/SHA256SUMS`.

The [4.9.0 School Services guide](docs/4.9.0/DEPLOYMENT.md) remains available for the previous release. Earlier versions must be upgraded in sequence. Checksums are in `dist/SHA256SUMS`. These ZIPs update an existing installation; they are not standalone installers.

Prior [4.8.0 Operations](docs/4.8.0/DEPLOYMENT.md) and [4.7.0 Learning](docs/4.7.0/DEPLOYMENT.md) guides remain available.

AI is optional and disabled by default. Existing Teacher/Student AI uses the school's private `providers.ai_api_key`; Intelligence Copilot uses its separately encrypted school credential. Both require outbound HTTPS and explicit school enablement. Automated AI tests use simulated provider responses; no live model/account availability is claimed.

`python3 tools/build_release.py` builds the latest packages and checksum list. Historical 4.6.4–5.1.0 ZIPs remain immutable. See [tests/README.md](tests/README.md) for isolated test commands. This is the PHP 8.4/MariaDB/cPanel script application requested by the user; production credentials, database contents, uploaded files and historical live backups are excluded from Git and release payloads.

Earlier Family Portal findings and deployment evidence remain in [docs/AUDIT.md](docs/AUDIT.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) and [docs/VALIDATION.md](docs/VALIDATION.md). The product blueprint remains product context, not executable deployment instructions. No production server was accessed by this work.
