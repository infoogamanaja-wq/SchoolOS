# SchoolOS 5.2.1 — Interactive Website

The public website now has rotating headline text, scroll reveals, pointer-following card highlights, hover lifts, button shine and clearly drifting academic doodles. Floating panels and notes add movement without blocking content. Motion respects the operating system's reduced-motion preference, and a persistent pause/resume control is available on desktop and mobile.

A light/night switch appears on every public page. It follows the system preference until a visitor chooses a theme, then saves that choice using the existing `schoolos-theme` key shared with dashboards. Dark surfaces, forms, cards, quiz answers, navigation and footer are styled together. Theme preference is applied in the document head to reduce a bright flash on navigation.

The challenge collection contains **36 distinct questions across six topics**: Maths, Science, Logic, Words, Geography and Digital skills. Each topic has six questions, three answer choices and a reviewed explanation. Visitors can select a topic or explore the shuffled full collection. A question does not repeat until its current deck is exhausted, and solving a question twice does not inflate the score. Incorrect answers allow another attempt. The section offers a next-question button and keyboard-friendly controls, without imposing a countdown.

The same SchoolOS mark now appears on the public header/footer, authentication screens and dashboard sidebar. A school's uploaded logo and school identity remain independently configured.

## Install

Requires the existing **5.2.0** release. Back up and test on staging, then install **`dist/SchoolOS-5.2.1-Interactive-Website.zip`** through Super Admin → Updates & Plugins. This is one six-file patch; the 5.2.0 updater already permits every destination, so no new support ZIP is needed. Older versions must first follow the documented upgrade sequence.

The patch contains `index.php`, `experience_ui.php`, `public_site.php`, `public_site.css`, `public_site.js` and `VERSION.txt`. There are no database migrations, provider configuration changes or affiliate/Finance/Family module replacements. Asset cache versions are incremented. Update Manager rollback restores the exact prior six files; reinstallation is supported.

## Verification

- **148 real-browser assertions** cover time-varying doodles and headlines, pause persistence, shared dark theme, hover highlights, every question's correct feedback, repeat-free topic decks, unique scores, 360/390/768/1024px layouts, reduced motion, branding and dashboard theme continuity.
- **74 public website regression assertions** cover public pages, all 18 online/PDF guides, mobile menu, quiz/facts, snapshots, invalid routes and document path rejection.
- **17 real frontend package checks** cover installation on 5.2.0, all deployed hashes, existing affiliate data, exact rollback, protected libraries/config and reinstall.
- **26 archive checks** cover all fourteen immutable historical ZIPs, manifest/source equality, permissions, private-path exclusion and deterministic rebuilds.
- The three changed PHP files parse under PHP 8.4.24; JavaScript syntax checks pass. Browser checks report no JavaScript errors. Screenshots and logs are in `test-output`.

No production server was accessed or changed. Browser and installation checks ran against local disposable runtimes; the release ZIP is ready for staging acceptance.
