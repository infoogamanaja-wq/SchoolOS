# SchoolOS Nigeria — audited Family Portal update

This repository contains the repaired application source, automated tests, audit findings, and two staged Update Manager ZIPs. It was reconstructed from the supplied `public_html.zip`; production configuration, database contents, uploaded files, and historical backups are excluded.

Read [the audit](docs/AUDIT.md), [deployment instructions](docs/DEPLOYMENT.md), and [test evidence](docs/VALIDATION.md) before deployment.

1. Test `dist/SchoolOS-4.6.4-Updater-Repair.zip` on a staging clone first. It changes only `system_manager.php`, leaving the existing entry point untouched.
2. Test `dist/SchoolOS-4.6.5-Family-Portal.zip` on staging. This changes the entry point and includes all required new code.
3. Activate Family Space as a school administrator, after a database backup. Existing ecosystem account links supply parent access. No parent is linked merely by matching an email or name.

Build reproducible packages with `python3 tools/build_release.py`. PHP 8.4, MariaDB, and the extensions listed in the deployment guide are required for runtime tests. See `tests/README.md` for isolated test setup.

The complete product blueprint is product context. This change implements the requested Parent & Guardian Portal, not every future feature in that blueprint. Live hosting deletion and live Paystack behavior have not been established by local tests.
