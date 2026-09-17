# Track 3 preview: Preserve PPE decision evidence

## Outcome

Relate one Praxis request to a policy decision and a tamper-evident ledger
receipt using the exact same trace identifier. The learner explains what the
receipt proves—and what it does not prove—without placing evidence storage in
the authorization path.

This is a **contract-ready preview**, not a required lab exercise. A released,
pinned Praxis/PPE audit interface and an OpenShift conformance run are still
required before publication as a live integration.

## See

Start with one request whose `trace_id` is visible in the Praxis learning UI.
The intended evidence path is:

```text
polyglot client
    -> Praxis AI Gateway
        -> PPE allow / deny / transform
            -> configured backend
            -> OCSF audit adapter
                -> immutable ledger proof receipt
```

ContextForge can host CPEX and emit the corresponding `cpex.*` evidence path.
Praxis hosts PPE and emits `praxis.ppe.*`. The engines share ancestry but are
not stacked in a single request path.

## Learn

PPE remains responsible for authorization. The OCSF adapter translates the
completed decision into a portable audit event, and the ledger preserves those
opaque bytes in an independently verifiable hash chain. A valid receipt proves
that matching bytes remain in the ledger; it does not prove the policy was
correct, make the event true, or grant access.

The lab deliberately excludes prompts, completions, credentials, and raw
sensitive values from evidence. It records pseudonymous identity, policy and
resource identifiers, a machine-readable reason, hashes, and correlation
metadata.

The producer contract is maintained in
[`are-immutable-ledger/contracts/praxis-ppe-ocsf-ledger-contract.md`](https://github.com/jkershawrh/are-immutable-ledger/blob/main/contracts/praxis-ppe-ocsf-ledger-contract.md).

## Do: red phase

Given a versioned PPE fixture for a known Praxis request, first validate the
environment before installing an adapter. The result must be red when any of
these are absent:

- the PPE event uses `praxis.ppe.audit.v1`;
- its `trace_id` exactly matches the request trace;
- the OCSF event contains the required policy metadata and no content canary;
- the ledger accepts an idempotency key derived from the event ID; and
- the receipt can be verified with both its entry hash and entry type.

The red result is evidence that the integration has not yet been established,
not an instruction to bypass policy or weaken audit delivery.

## Do: green phase

After a pinned upstream audit interface is available:

1. Deploy the adapter as a separately identified OpenShift workload.
2. Configure its ledger credential through an OpenShift Secret.
3. Apply NetworkPolicy so only the adapter reaches the ledger endpoint.
4. Submit an allowed and a denied request through Praxis.
5. Query the ledger by each exact request trace ID.
6. Verify each receipt and its exact entry-type chain.
7. Repeat one event ID and prove the write is idempotent.
8. Interrupt the ledger and verify the declared fail-closed, buffered, or
   best-effort delivery behavior.

Green evidence must include sanitized request metadata, policy outcome, OCSF
mapping result, proof receipt, chain verification result, and delivery-mode
result. It must not include credentials or model content.

## Assess

The learner succeeds when they can:

- distinguish policy enforcement from evidence preservation;
- explain why CPEX and PPE are alternative enforcement engines in this design;
- correlate the UI, Praxis trace, PPE event, and ledger receipt without a
  "latest event" fallback;
- demonstrate that a receipt is evidence rather than authorization; and
- state why the module remains preview until upstream and OpenShift gates pass.

## Industry application

Banking, healthcare, government, manufacturing, and telecommunications teams
may choose different retention, delivery, identity, and redaction policies.
Those profiles change the controls and evidence requirements; they do not
turn this exercise into proof of regulatory compliance.

