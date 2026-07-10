# VEIP SDK

MIT Reference Implementation of the Veraxis Execution Integrity Protocol (VEIP)

---

## Executive Summary

The VEIP SDK is a minimal, production-structured reference implementation of the **Veraxis Execution Integrity Protocol (VEIP)**.

It demonstrates how an AI-enabled system can:

- Enforce authorization *before execution*
- Perform deterministic state-transition classification
- Emit structured, schema-valid Evidence Packs
- Support replay validation of execution decisions
- Bind implementation behavior to a specific VEIP specification version

This repository is intentionally compact and readable.  
It is designed for interoperability, sandbox experimentation, and integration scaffolding.

It is **not** a certification engine.

---

## Deterministic Design Principles

This SDK enforces three core invariants:

1. **Authorization Precedes Execution**  
   No action may be executed without explicit classification.

2. **State Transitions Are Deterministic**  
   Given identical authority and proposal inputs, classification must be reproducible.

3. **Evidence Emission Is Mandatory**  
   Every classified action produces a structured Evidence Pack aligned to the VEIP schema.

These properties are test-verified through the included CI and replay validator.

---

## Relationship to the VEIP Specification

This SDK implements:

**VEIP Specification v0.1.0**

The canonical specification is defined in the `veip-spec` repository and includes:

- Formal state-transition model
- Authority envelope semantics
- Evidence Pack JSON Schema (Draft 2020-12)
- Conformance Test Suite (CTS) structure
- Supervisory Verification Interface (SVI)

The specification defines the normative rules.  
This repository provides executable implementation examples.

The SDK enforces:

- Specification version binding
- Schema hash pinning
- Schema validation at emission time

This prevents silent drift between implementation and specification.

---

## What This Repository Is

The VEIP SDK is:

- A minimal execution authorization gate
- A deterministic state-machine scaffold
- A schema-valid Evidence Pack emitter
- A replay validation demonstrator
- A developer-facing integration reference

It is suitable for:

- Regulatory sandbox experimentation
- Academic research
- AI control-plane prototyping
- Internal enterprise architecture evaluation

---

## What This Repository Is Not

The VEIP SDK is not:

- The official VEIP conformance validator
- The Verifier Core
- The registry or certification authority
- A regulatory endorsement mechanism
- A cryptographically sealed audit infrastructure

Certification and authoritative validation are governed separately through the VEIP Verifier Core and Registry layers.

---

## Architecture Model

The SDK illustrates the VEIP execution control-plane:

AI System  
→ Action Proposal  
→ VEIP Authorization Gate  
→ Deterministic Classification  
→ Execution (if permitted)  
→ Evidence Pack Emission  
→ Replay Validation (optional)

Each action:

1. Is scoped under an authority envelope
2. Is deterministically classified (ALLOW / DENY / ESCALATE / SUPERVISORY)
3. Produces a schema-valid Evidence Pack
4. Can be replay-validated against its inputs

---

## Repository Structure

```

veip-sdk/
├── README.md
├── LICENSE
├── pyproject.toml
├── Makefile
├── .github/workflows/ci.yml
├── veip_sdk/
│   ├── **init**.py
│   ├── authorize.py
│   ├── evidence.py
│   ├── replay.py
│   ├── schema.py
│   ├── state_machine.py
│   ├── veip_types.py
│   └── schemas/
│       └── veip-evidence-pack.schema.json
└── examples/
└── minimal_demo.py

````

---

## Installation

Python 3.10+

```bash
pip install -e ".[dev]"
````

---

## Local CI Verification

Run:

```bash
make ci
```

Expected output:

```
OK: Python syntax checks passed
..... [100%]
```

This confirms:

* Schema binding integrity
* Replay validator correctness
* Deterministic classification
* Evidence Pack schema compliance

---

## Minimal End-to-End Example

Run:

```bash
python examples/minimal_demo.py
```

Expected output:

```
Decision: ALLOW
Replay: True OK
Evidence Pack keys: ['schema_version', 'evidence_id', 'created_at', 'authority', 'policy', 'action', 'decision', 'execution', 'provenance']
Evidence ID: <uuid>
```

This demonstrates:

* Proposal submission
* Authorization classification
* Evidence Pack emission
* Schema validation
* Replay validation

---

## Specification Binding Safeguards

The SDK enforces two integrity controls:

1. Schema SHA-256 pinning
2. VEIP specification version matching

If the canonical schema changes without updating the SDK, execution fails explicitly.

This protects against silent compatibility drift.

---

## Early Production-Grade Posture

This SDK supports integration into regulated architectures with:

* Deterministic execution semantics
* Explicit authority scoping
* Structured Evidence emission
* Replay-verifiable decision paths
* Version binding safeguards

However, production environments require additional controls:

* Cryptographic sealing (hash chaining / Merkle anchoring)
* Secure time sources
* Tamper-evident storage
* Operational resilience hardening
* Independent security review
* Separation of duties enforcement

These layers are intentionally out of scope for this repository.

---

## Versioning

SDK Version: 0.1.0
Aligned Specification Version: 0.1.0

Breaking changes follow semantic versioning.

---

## Licensing

This repository is licensed under the MIT License.

You may:

* Use
* Modify
* Integrate
* Commercialize

Subject to MIT terms.

Use of “VEIP Certified” or “VEIP Compliant” is governed by trademark and registry policy.

---

## Contribution Policy

Contributions must preserve the following invariants:

1. Authorization precedes execution.
2. State transitions remain explicit and deterministic.
3. Evidence emission remains mandatory.
4. Schema alignment must remain enforced.

Pull requests may require alignment with the VEIP specification.

---

## Disclaimer

This SDK is provided “as is,” without warranty of any kind.

It is a reference implementation of an open protocol and does not constitute regulatory approval or certification.

```
```
