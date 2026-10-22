# Reproduce validation in isolation

Never run fixtures or installation tests against production. Use PHP 8.4 with the required extensions, MariaDB, and an empty database named `schoolos_test`. The seed command refuses a nonempty database and requires an explicit fixture flag. These tests use synthetic identities and the documented test-only password `Local-test-password-2026!`.

Set `SCHOOLOS_TEST_DSN`, `SCHOOLOS_TEST_USER`, and `SCHOOLOS_TEST_PASSWORD` securely in your local test environment if defaults are unsuitable; do not commit real credentials. The default DSN is `mysql:host=localhost;dbname=schoolos_test;charset=utf8mb4` and the default local-only account is root with no password. For this audit MariaDB used only a private Unix socket, with TCP networking disabled.

```
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/seed.php
php tests/updater.php
php tests/portal.php
php tests/concurrency.php
```

The portal suite mutates its synthetic data. For a fresh repeat, recreate **only the disposable test database**, then seed it again. The updater suite creates independent temporary application roots. The concurrency test uses two independent PHP worker processes/database connections.

HTTP suites require local-only document roots prepared as follows:

- `/app`: copy `app/`, supply a local config pointing to the seeded `schoolos_test` database.
- `/installer`: copy `app/` without config or installation lock; create a separate empty `schoolos_installer` database for the installer form.
- `/upgrade`: copy the **original uploaded application** with its original updater and stable root index, configure only the synthetic test database, and initialize `storage/system/version.json` to the uploaded 4.6.3 state. Keep production config/uploads/backups out of all three roots.

Serve their parent with `php -S 127.0.0.1:8090 -t /path/to/runtime` and run:

```
python3 tests/http_smoke.py http://127.0.0.1:8090
python3 tests/package_http.py http://127.0.0.1:8090 /upgrade/
```

`package_http.py` additionally accepts `SCHOOLOS_UPGRADE_ROOT` for its disposable filesystem checks (default `/workspace/schoolos-audit/runtime/upgrade`). Do not point it at any real installation. It uploads the actual built ZIPs, verifies files/version/config, rolls back, checks the homepage, and reinstalls. Recreate `/installer` and its empty database before repeating fresh-install tests; recreate `/upgrade` from the original before repeating the full package sequence.

For Apache validation, point a local Apache 2.4 virtual host at `/upgrade`, enable mod_dir/mod_rewrite/mod_proxy_fcgi/authz_core and `.htaccess`, and connect it to PHP 8.4 CGI/FPM. Use `ProxyFCGIBackendType GENERIC` for a standalone `php-cgi -b` backend (not for PHP-FPM). Then run:

```
python3 tests/apache_routing.py http://127.0.0.1:8092
```

Apache tests verify DirectoryIndex, fallback rewrite, storage/config/database/dot-path denials, direct-module redirection and an authenticated portal route. This is local Apache/FastCGI evidence, not a test of the user's actual cPanel configuration.

Use `python3 tools/build_release.py` to reproduce ZIPs and hashes. Lint all PHP files and verify built archive contents and manifest hashes before distributing. Live Paystack test transactions and cPanel quarantine/deletion observations require the user's actual staging services and logs.

The read-only monitor can be tested independently with `SCHOOLOS_PHP_COMMAND=/path/to/php84 python3 tests/integrity_monitor.py`. To repeat MariaDB compatibility checks on a second server, set a socket-specific `SCHOOLOS_TEST_DSN`, create its empty `schoolos_test` database, and run the seed, portal, and concurrency suites there.
