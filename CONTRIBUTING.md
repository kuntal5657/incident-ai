# Contributing to Incident AI

Thank you for your interest in Incident AI.

This repository is primarily intended as a **reference architecture and learning resource**
for building production-grade GenAI systems.

Contributions are welcome, but they must respect the architectural principles
documented in this repository.

---

## Contribution Philosophy

Before contributing, please read:

- docs/MASTER_DOC.md
- docs/ARCHITECTURE.md
- docs/ANTI_PATTERNS.md

Changes that violate documented invariants will not be accepted.

---

## What Kinds of Contributions Are Welcome

✔ Documentation improvements  
✔ Clarifications and examples  
✔ Bug fixes that preserve architecture  
✔ Observability or safety enhancements  

---

## What Is Out of Scope

✖ Turning this into a SaaS product  
✖ Adding UI layers  
✖ Making LLM calls synchronous  
✖ Removing async boundaries  
✖ Treating fine-tuning as memory  

These are deliberate non-goals.

---

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make changes with clear reasoning
4. Update documentation if behavior changes
5. Open a pull request

---

## Coding Guidelines

- Prefer clarity over cleverness
- Explicit > implicit
- Architecture > model tweaks
- Safety > speed

---

## Documentation Rule

If your change affects:
- behavior
- architecture
- safety
- cost
- reliability

You **must** update the relevant documentation.

Documentation drift is treated as a bug.

---

## Final Note

Incident AI treats GenAI as:

> A powerful but untrusted dependency inside a carefully engineered system.

All contributions must preserve that assumption.

---

Thank you for contributing responsibly.
