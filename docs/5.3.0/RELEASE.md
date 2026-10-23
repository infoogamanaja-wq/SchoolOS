# SchoolOS 5.3.0 — role portals, family care and live learning

This release reorganizes Family Space, Teaching studio and the learner journey while retaining the existing features. Grouped feature navigation and course cards replace an undifferentiated menu. Library reservations and other module tabs mark the active view. Specialist workspaces require corresponding grants; own employment, wallet, transport and boarding remain available through role-specific routes.

## Family workflows

Published results display weighted CA, exam and total values separately. Total-only historical results remain identified rather than receiving fabricated component marks. Confirmed receipts carry the school's branding, contact details, invoice/payment references, learner/admission, amount in words and current invoice balance.

Parents can send a message to several permitted school adults as private individual copies. Teachers can do the same for linked guardians. Calendar entries expand to show start/end time, audience and venue. Daily meal choices are unique per child/menu/date. Pickup requests require a collector phone; existing approval, short-lived token and verified handover tools remain.

Bookings, absence and related module actions show focused success/error banners. Important transport, appointment, review, emergency and unread conversation updates appear prominently. Rotating updates can be paused; sound is opt-in. Dark-theme overrides cover the tested dashboard modules and form surfaces.

## Conversations and classroom

In-app conversations refresh every three seconds while visible; important-update checks run every fifteen seconds. This is authenticated polling, not a deployed WebSocket service. Contacts follow verified school and family relationships; group membership must respect all members' relationships. Browser output treats message bodies as text. Retries are idempotent and concurrent sends serialize safely.

Teachers can attach existing Zoom/Meet invitation links or host an eight-person built-in teacher broadcast. Learners do not publish their camera/microphone. Built-in media uses WebRTC with addressed, scoped signaling, time windows and participant limits. It supports teacher screen sharing, temporary relay credentials and local capture cleanup. **A separately configured TURN service is needed for reliable remote connectivity.** This release is not a full multi-party conferencing service and does not provision Zoom/Meet accounts. Existing CBT, assignment, question-bank, grading, resource and offline-teacher capabilities remain.

## Demo and documentation

An existing verified isolated demo upgrades automatically with fictional CA marks, daily meals, dated events, connected chat and a scheduled lesson, retaining existing demo bookings. Fresh isolated-demo provisioning still requires an empty dedicated database. Optional sandbox relay settings remain separate from real schools. The 18 downloadable role guides remain available; the owner, parent, teacher, learner and platform guides now cover this release.

Install the support ZIP followed by the main ZIP. See [deployment](DEPLOYMENT.md), [validation](VALIDATION.md) and the [parent night preview](test-output/parent-night.png). Local testing is not a live cPanel deployment or a blanket guarantee that every future configuration/provider is compatible.
