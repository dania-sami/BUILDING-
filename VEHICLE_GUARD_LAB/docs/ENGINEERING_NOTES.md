# Engineering notes and five-minute walkthrough

## Architecture

Browser UI → Python standard-library local HTTP API → SQLite cases + append-only-style evidence events → SHA-256 chain verification → downloadable briefing.

## Demonstration for a PSIRT manager

1. **Prioritize:** Explain why raw CVSS is only one input; vehicle exposure, safety context and confidence also matter. The composite is illustrative, not an official standard.
2. **Investigate:** Select the telematics case, read synthetic signals, and check the investigation steps.
3. **Coordinate:** Record a `Handoff` event to vehicle engineering, stating what evidence is needed and who owns the next decision.
4. **Decide:** Record a `Decision` with assumptions, owner and next review time. Change the case status to `Investigating`.
5. **Prove accountability:** Open the evidence chain and show the SHA-256 links. Export a concise case brief.

## Threat model and boundaries

This is a **local teaching demo**, not production incident-response infrastructure. It provides no identity verification, RBAC, secure timestamps, digital signatures, trusted storage, tamper-proof logs, incident containment controls, or integrations with real CVE feeds. The event chain detects accidental/manual modification of stored records only under the assumption that the attacker cannot rewrite the whole chain. Never import confidential vehicle data into the demo.

## Standards literacy

- ISO/SAE 21434: automotive cybersecurity engineering across lifecycle activities. This tool illustrates workflow discipline but does not establish compliance.
- UNECE R155: cybersecurity and cybersecurity management systems for vehicles. This tool is not a CSMS.
- CVSS: an established vulnerability severity scoring system. The project displays supplied synthetic CVSS numbers; its own priority metric is not CVSS.
- Coordinated vulnerability disclosure: document affected components, supplier handoffs, remediation plans and communication approvals.

## What to build next

Validated CycloneDX SBOM import, offline vulnerability correlation using published CPE applicability data, authenticated role-specific workflows, signed event exports, incident tabletop simulation scoring, and a documented test harness.
