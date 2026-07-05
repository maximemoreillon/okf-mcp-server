---
type: decision
title: Stack Pairing Guidance
tags: [decision, stack]
---
How to pair frontend, backend, and language choices for a new project.

**All-TypeScript stack**: [React](../frontend/react.md) or
[Vue](../frontend/vue.md) + [Express](../backend/express.md), both in
[TypeScript](../languages/typescript.md). Pick this when you want one
language across the stack and the team is JS/TS-native. You can share
types (e.g. API request/response shapes) between client and server
without duplicating schemas.

**Python backend, JS frontend**: [React](../frontend/react.md) or
[Vue](../frontend/vue.md) + [FastAPI](../backend/fastapi.md) in
[Python](../languages/python.md). Pick this when the backend needs
Python's data/ML ecosystem, or the team already has stronger Python
than JS backend skills. The frontend/backend language split is fine
since they communicate over HTTP/JSON regardless of language — you
lose type-sharing but gain FastAPI's automatic request validation and
OpenAPI docs, which partially substitutes for it.

**Choosing React vs Vue** is mostly independent of the backend
choice — it's driven by team familiarity, ecosystem needs (Next.js if
you need SSR), and hiring pool, not by which backend you pick.

**Rule of thumb**: optimize the frontend choice for team/ecosystem fit,
and the backend choice for what the backend actually needs to do
(heavy I/O and JS-native tooling → Express; data/ML work or fast
validated APIs → FastAPI).
