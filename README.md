# SchoolOS Nigeria — Platform Experience 5.1.0

A modern, interactive platform experience for school owners, teachers, families, learners and operational teams: clearer role dashboards, responsive glass surfaces, recorded-data infographics, WAT date/time, guided setup, walkthroughs and priority readiness alerts.

New schools can register using configured subscription plans/trials. School members can be administrator-created or request access for verified approval. Secure first-login/recovery workflows and fourteen connected demo choices are included. Demo activity uses a **separate database and private sessions**, with live providers disabled.

Read the [deployment guide](docs/5.1.0/DEPLOYMENT.md), [feature map](docs/5.1.0/FEATURES.md), [audit and boundaries](docs/5.1.0/AUDIT.md) and [validation](docs/5.1.0/VALIDATION.md). [Preview the school-owner overview](docs/5.1.0/test-output/school-owner-desktop.png).

On a backed-up staging clone of **5.0.0**, install through **Platform Super Admin → Updates & Plugins**, in order:

1. `dist/SchoolOS-5.0.1-Experience-Updater.zip` — updater support; preserves the working entry point.
2. `dist/SchoolOS-5.1.0-Platform-Experience.zip` — main update.
3. Open **Setup & account → Activate Experience & installed workspaces**. As platform administrator, configure plans/trial policy, the canonical HTTPS URL and gateway. Provision an empty dedicated `_demo` database in cPanel before enabling demo logins.

**1,230 primary assertions**, **183 MariaDB compatibility assertions**, **50 PHP syntax checks**, real browser interactions and actual frontend installation/rollback passed locally. Existing school records and the Finance, Family, Learning, Operations, Services and Intelligence workflows are retained. Provider/live-cPanel/physical-device acceptance remains a deployment check; legal compliance and every future roadmap integration are not certified by this update.

The previous [5.0.0 Intelligence guide](docs/5.0.0/DEPLOYMENT.md) and its [feature boundaries](docs/5.0.0/FEATURES.md) remain available. Upgrade earlier installations in sequence. The ZIPs update an existing application and are not standalone installers. Check `dist/SHA256SUMS`.

The [4.9.0 School Services guide](docs/4.9.0/DEPLOYMENT.md) remains available for the previous release. Earlier versions must be upgraded in sequence. Checksums are in `dist/SHA256SUMS`. These ZIPs update an existing installation; they are not standalone installers.

Prior [4.8.0 Operations](docs/4.8.0/DEPLOYMENT.md) and [4.7.0 Learning](docs/4.7.0/DEPLOYMENT.md) guides remain available.

AI is optional and disabled by default. Existing Teacher/Student AI uses the school's private `providers.ai_api_key`; Intelligence Copilot uses its separately encrypted school credential. Both require outbound HTTPS and explicit school enablement. Automated AI tests use simulated provider responses; no live model/account availability is claimed.

`python3 tools/build_release.py` builds the latest packages and checksum list. Historical 4.6.4–5.0.0 ZIPs remain immutable. See [tests/README.md](tests/README.md) for isolated test commands. This is the PHP 8.4/MariaDB/cPanel script application requested by the user; production credentials, database contents, uploaded files and historical live backups are excluded from Git and release payloads.

Earlier Family Portal findings and deployment evidence remain in [docs/AUDIT.md](docs/AUDIT.md), [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) and [docs/VALIDATION.md](docs/VALIDATION.md). The product blueprint remains product context, not executable deployment instructions. No production server was accessed by this work.
