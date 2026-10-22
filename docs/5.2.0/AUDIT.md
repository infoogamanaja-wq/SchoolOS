# SchoolOS 5.2.0 — audit and boundaries

The frontend is locally hosted: no advertising trackers, external font requests, remote screenshot dependencies or browser-exposed provider secrets. Academic facts are bounded mathematical/scientific statements, not fabricated school-outcome claims. Preview images contain only the existing fictional demo. Operator identity/contact are owner-supplied.

Affiliate financial helpers refresh account permissions and reject shared-demo mutations. Applications require CSRF/terms; signup is rate limited. School creation and attribution share a transaction. Commission credit creation shares the verified payment transaction, using a unique source transaction and payment identity. Money is integer kobo in the affiliate ledger. Both the current Experience and older SaaS verification paths call the same commission logic. A verified provider environment is required; test credits cannot fund live withdrawals.

Withdrawal creation locks the affiliate row before checking the available balance. It snapshots amount, environment and verified recipient, reserves immediately, and cannot overspend through parallel requests. Transfer authorization locks the withdrawal, refreshes affiliate status/balance, changes state to `sending` before calling the provider and refuses a second submission. Ambiguous responses remain reserved until reconciliation. Exact server-side verification is required to mark paid; a successful transfer cannot be downgraded by a pending/stale result. Reversals remain possible with verified evidence. Settings save atomically; attribution terms are not retroactively changed.

Processed refunds are fetched from Paystack rather than accepted from a browser claim, deduplicated by provider event identity, accumulated in gross kobo, and prorated against the original commission. Full cumulative refunds reverse the full commission without rounding residue. Earlier payouts remain recorded, producing debt instead of deleting history. Transfer state evidence is retained in affiliate event records. Private financial views are scoped to the current affiliate; referred school names, contacts and school records are not disclosed.

The Paystack callback now executes before the anonymous homepage response. The prior location after the homepage exit made anonymous callback delivery unreachable. Invalid signatures return 401. Callback event bodies alone never mark a payment/transfer paid. Unknown provider evidence returns a retryable failure and preserves funds.

## Explicit limits

- No production cPanel access, real payout, actual bank transfer, DNS change or real message was performed. Provider flows use injected synthetic responses in tests. Live provider transfer entitlement, OTP policy, balance and network access require deployment acceptance.
- Human Super Admin approval is deliberately required before submitting a withdrawal. Automation handles crediting, reservations and verification, not unreviewed movement of money.
- Self-referral checks cover the recorded owner ID/email; hidden common ownership or coordinated fraud requires review. A newly registered dedicated affiliate email has not been independently email-verified; platform approval must verify identity and ownership of the payout account. Bank resolution proves the provider's account name, not the affiliate's legal entitlement to that account.
- Disputes/chargebacks require investigation and payout suspension until resolved. The processed-refund workflow is not a general legal dispute adjudicator. Retention, tax, privacy compliance, operator contracts and commission tax treatment remain the operator's responsibility.
- The current shared school demo does not allow affiliate banking or payouts. Those workflows are tested against disposable fixtures and provider doubles.
- On/off does not erase earned obligations. A rollback does not cancel submitted transfers or remove database history.
- Hosting deletion cannot be declared permanently resolved without server logs. The working entry point is replaced only by the tested main update after its support package, and the production server was untouched during this work.
