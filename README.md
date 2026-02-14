
# VEIP SDK

MIT Reference Implementation of the Veraxis Execution Integrity Protocol

## Overview

The VEIP SDK provides a minimal, MIT-licensed reference implementation of the Veraxis Execution Integrity Protocol (VEIP).

This repository demonstrates how to implement:

* Deterministic state-transition handling
* Execution-time authorization gating
* Evidence Pack serialization aligned to the VEIP specification
* Supervisory classification semantics (ALLOW, DENY, ESCALATE, SUPERVISORY)

The SDK is designed to accelerate ecosystem adoption and interoperability. It is not a certification engine and does not confer official VEIP compliance status.

---

## Relationship to the VEIP Specification

This SDK implements **VEIP Specification v0.1.0** as defined in the `veip-spec` repository.

The specification defines:

* State-transition formalism
* Authority envelope semantics
* Evidence Pack schema
* Conformance Test Suite (CTS) definitions
* Supervisory Verification Interface (SVI)

The SDK demonstrates how these rules can be implemented in practice.

Normative rules are defined in the specification.
This repository contains executable examples.

---

## What This Repository Is

The VEIP SDK is:

* A developer integration scaffold
* A minimal execution authorization engine
* An Evidence Pack emitter aligned to the official schema
* A reference state-machine implementation
* A foundation for sandbox experimentation

The SDK is intentionally compact and readable.

---

## What This Repository Is Not

The VEIP SDK is not:

* The official VEIP conformance validator
* The deterministic replay verification engine
* The certification authority
* A registry implementation
* A regulatory endorsement mechanism

Official conformance validation and certification are governed separately through the VEIP Verifier Core and Registry infrastructure.

---

## Architecture Model

The SDK illustrates the VEIP execution control-plane:

AI System
→ Action Proposal
→ VEIP Authorization Gate
→ State Transition Evaluation
→ Execution (if permitted)
→ Evidence Pack Emission

Each proposed action:

1. Is classified under a defined authority envelope
2. Results in a deterministic decision
3. Produces a structured Evidence Pack

No action is executed without explicit classification.

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
│   ├── __init__.py
│   ├── types.py
│   ├── authorize.py
│   ├── evidence.py
│   └── state_machine.py
└── examples/
    └── minimal_demo.py
```

---

## Installation

Python 3.10+

```bash
pip install -e .
```

---

## Minimal Example

```bash
python examples/minimal_demo.py
```

The example:

* Proposes an action
* Evaluates authorization
* Performs state transition classification
* Emits a VEIP Evidence Pack (JSON)

The resulting artifact aligns with the schema defined in `veip-spec`.

---

## Early Production Grade Posture

This SDK is structured for integration into regulated environments with the following properties:

* Deterministic transition semantics
* Explicit authority scoping
* Versioned Evidence Pack schema alignment
* Clear separation between authorization and execution

However, production deployments require additional controls including:

* Cryptographic sealing
* Secure time sources
* Tamper-evident storage
* Operational resilience hardening
* Independent security review

This repository does not implement those infrastructure layers.

---

## Versioning

SDK Version: 0.1.0
Aligned Specification Version: 0.1.0

Breaking changes will follow semantic versioning.

---

## Licensing

This repository is licensed under the MIT License.

You are free to:

* Use
* Modify
* Integrate
* Commercialize

Subject to MIT license terms.

Use of the terms “VEIP Certified” or “VEIP Compliant” is governed by the VEIP trademark and registry policy.

---

## Contribution Policy

Contributions must preserve VEIP invariants:

1. Authorization precedes execution.
2. State transitions remain explicit and deterministic.
3. Evidence emission is mandatory for classified actions.

Pull requests may require alignment with the VEIP specification.

---

## Disclaimer

This SDK is provided “as is” without warranty of any kind.
It is a reference implementation of an open specification and does not constitute regulatory approval.

