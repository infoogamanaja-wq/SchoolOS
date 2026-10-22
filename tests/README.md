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

## Teacher / Student 4.7.0 suites

Use a new **empty, disposable** `schoolos_learning_test` database and a socket-specific `SCHOOLOS_TEST_DSN` when necessary. Run the base seed, then the learning seed, then domain tests:

```
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/seed.php
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/learning_seed.php
php tests/learning.php
```

The seed refuses existing portal fixtures; do not run against production. The domain suite mutates synthetic data. `tests/learning_concurrency.php` uses independent PHP processes to test CBT starts, last-copy library issue, club capacity and AI quota reservation. Run it **after** HTTP tests because it deliberately starts an active exam.

Prepare a local `/learning` root from app/ pointing only at schoolos_learning_test, then run `python3 tests/learning_http.py http://127.0.0.1:8090`. This exercises all views, cross-account denial, old-form guards, actual multipart CSV preview/commit, and homework attachment download restrictions.

For packaged-upgrade tests, prepare a separate empty `schoolos_upgrade_test`, run only the base seed against it, and point the local Apache document root at a disposable `/runtime/upgrade` copy of the working **4.6.5** application, with its 4.6.5 version metadata. Copy the exact old app files from the immutable 4.6.5 ZIP; retain required existing dependencies from app/. Do not include learning_portal.php initially. Supply only the isolated database config. Run `python3 tests/learning_package_http.py http://127.0.0.1:8092`. It uploads both new packages through the frontend, explicitly activates schemas, checks all views, performs rollback and verifies/reinstalls the package. It refuses a nonlocal URL and checks that its filesystem target is a disposable runtime/upgrade root. Override its root with `SCHOOLOS_UPGRADE_ROOT` if needed.

The existing Family Space regression suite must run on a **different**, freshly base-seeded disposable database (`php tests/portal.php`), because it has its own expected synthetic state. Second-version MariaDB compatibility uses the same seeds/domain/concurrency suites and an independent socket/server, not the live school database. AI tests supply mock transports and a fake test key; no provider network traffic or real student data is involved.

## HR / Transport / Boarding 4.8.0 suites

Create an empty disposable database ending in `_test`, set `SCHOOLOS_TEST_DSN` to it, and run in this order with PHP 8.4:

```
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/seed.php
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/learning_seed.php
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/operations_seed.php
php tests/operations.php
```

Copy current `app/` to a local-only document root `/operations` and supply a synthetic config pointing to this same database. Serve the parent directory on port 8090, then run:

```
python3 tests/operations_http.py http://127.0.0.1:8090/operations
php tests/operations_concurrency.php
```

The HTTP suite uploads a real synthetic private PDF; use the domain fixture before HTTP, and run concurrency last. Recreate and reseed the disposable database before repeating. For second-version compatibility, use a separate MariaDB socket/empty database and run the three seeds, operations domain and concurrency suites again.

For the actual package suite, prepare another **empty** `schoolos_upgrade_test` database and run `seed.php` then `learning_seed.php` against it (not operations_seed/domain). Copy current app dependencies to a disposable `/runtime/upgrade` directory, overwrite all payload files with exact bytes from immutable `SchoolOS-4.7.0-Teacher-Student-Portals.zip`, remove the four new operations PHP modules, provide a test-only config, and set `storage/system/version.json` to `{"version":"4.7.0"}`. Point the local Apache/FastCGI root there, then run `python3 tests/operations_package_http.py http://127.0.0.1:8092`; override `SCHOOLOS_UPGRADE_ROOT` for your disposable runtime/upgrade path. The suite requires a local hostname and a runtime/upgrade filesystem target. It installs 4.7.1 and 4.8.0 ZIPs through the frontend, activates schemas, exercises views, restores the exact old index, verifies retained dependencies and reinstalls. Run `tests/apache_routing.py` against the same Apache host afterwards.

Run existing `updater.php` and fresh separately seeded Family/Learning regressions as described above. Lint all PHP sources, run `python3 tools/build_release.py`, and verify each ZIP member against its release.json SHA-256. No production data or real provider calls are needed. See `docs/4.8.0/VALIDATION.md` for results and limits.

## School Services 4.9.0 suites

Use an **empty disposable** MariaDB database ending in `_test`. Set the test DSN/user/password as above, then run:

```
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/seed.php
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/learning_seed.php
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/operations_seed.php
SCHOOLOS_ALLOW_TEST_FIXTURES=1 php tests/services_seed.php
php tests/services.php
```

Create a local-only `/runtime/services` copy of current app/. Give it a synthetic config pointing to that database, with `app.cms_origin = https://schoolos.test`. The domain suite creates synthetic encrypted provider settings, so copy its **test-only** `app/storage/system/services-key.php` into the runtime's protected storage to retain the matching key. Do not copy any production key/config/database. Serve runtime locally, then run:

```
SCHOOLOS_PHP_COMMAND=/path/to/php84 python3 tests/services_http.py http://127.0.0.1:8090/services
php tests/services_concurrency.php
```

HTTP tests require test-only Pillow for a real gallery image upload. The HTTP suite covers all role screens, actual image/PDF uploads and guarded publication/download, public enquiry and replay, private previews, encrypted provider settings, Community email guards, legacy routes and a real CLI worker bootstrap. It does not call live providers. The worker fixture has no due external deliveries when that CLI bootstrap runs; provider calls elsewhere use injected transports.

Concurrency runs **after** HTTP and uses independent PHP processes/connections for licensed seats, stock/receipt bounds, idempotent issue, depreciation, delivery claiming, tour capacity and payment posting. Recreate/reseed the disposable database before repeating. Repeat the seed/domain/concurrency sequence against a separate MariaDB version/socket for compatibility.

For independently checked QR output, install `qrcode`, `Pillow`, `zxing-cpp` in a disposable test environment (not in the PHP app), then run:

```
SCHOOLOS_PHP_COMMAND=/path/to/php84 python3 tests/services_qr.py
```

This compares the PHP-generated module matrix with an independent QR encoder and decodes it using ZXing. The installed PHP release has no Python or external QR service dependency.

For actual packaged installation/rollback, prepare a separate empty `schoolos_upgrade_test` database, run `seed.php`, `learning_seed.php`, `operations_seed.php`, then `op_install()` through bootstrap. Prepare a disposable `/runtime/upgrade` copy of app/ **excluding storage/config/install locks**, restore the exact 4.8.0 payload from the immutable ZIP, and restore the exact Learning Portal from the immutable 4.7.0 ZIP. Remove all seven new service module/worker files initially. Supply only the synthetic config (`app.cms_origin` as above) and `storage/system/version.json` containing `{"version":"4.8.0"}`. Point local Apache/FastCGI there and run:

```
python3 tests/services_package_http.py http://127.0.0.1:8092
python3 tests/apache_routing.py http://127.0.0.1:8092
```

Override `SCHOOLOS_UPGRADE_ROOT` if needed; the suite requires a local host and a disposable runtime/upgrade root. It installs both ZIPs through the actual frontend, activates tables, checks every manager view, grants scoped access, publishes a website through independent approval, restores the exact prior index/Learning Portal on rollback, verifies retained dependencies and checks preserved content after reinstall. Use a supervised FastCGI process (or `PHP_FCGI_MAX_REQUESTS=0` for this isolated test fixture) so the standalone test backend does not exit mid-suite after its default request limit.

Run Family, Learning, Operations and updater regressions on their **own fresh fixtures** as documented above. Keep old release ZIPs immutable. Lint tracked PHP source files (exclude private generated storage), verify the new ZIP manifests/source equality and private-file exclusions, and run `git diff --check`. See `docs/4.9.0/VALIDATION.md` for exact results and the limits of simulated DNS/provider evidence.

## School Intelligence 5.0.0

Use a **fresh disposable database ending `_test`**. Set `SCHOOLOS_TEST_DSN`, `SCHOOLOS_TEST_USER`, `SCHOOLOS_TEST_PASSWORD` and `SCHOOLOS_ALLOW_TEST_FIXTURES=1`; never point fixtures at production. Run these sequentially with PHP 8.4 plus PDO MySQL/mbstring/fileinfo/zip/cURL/OpenSSL:

```sh
php tests/seed.php
php tests/learning_seed.php
php tests/operations_seed.php
php tests/services_seed.php
php tests/intelligence.php
php tests/intelligence_concurrency.php
node tests/offline_teacher.mjs
php tests/updater.php
python3 tests/intelligence_release.py
```

The domain fixture includes synthetic independent reviewers, cashier, parent, teacher and cross-school accounts. Provider responses are injected mocks; no real external send/payment is needed. MariaDB compatibility tests use a separately seeded instance/socket. `intelligence_http.py` targets a matching local runtime clone (default loopback port 8090 `/intelligence`); `intelligence_package_http.py` targets a disposable local Apache root with baseline 4.9.0 and fresh pre-Intelligence fixtures. Package tests replace files and perform frontend rollback: **never run them against a live installation**. Python HTTP suites that invoke PHP accept `SCHOOLOS_PHP_COMMAND`. Existing Family/Learning/Operations/Services regressions each need their own freshly seeded fixture database.

Release evidence and limitations are in `docs/5.0.0/VALIDATION.md`. The offline JS suite executes WebCrypto and queue logic; it does not substitute for Android/IndexedDB/service-worker acceptance testing.
