---
type: technology
title: Express
tags: [backend, nodejs, javascript]
resource: https://expressjs.com
---
Express is a minimal Node.js web framework. It's unopinionated —
routing, validation, ORM, and auth are all separate library choices
you assemble yourself (or via a wrapper like NestJS if you want more
structure out of the box).

Runs on Node, written in [TypeScript](../languages/typescript.md) or
plain JS.

Best fit when: the team wants one language (JS/TS) across the whole
stack, sharing types between frontend and backend, or the project is
I/O-bound (lots of concurrent requests, not CPU-heavy work).

See [Stack Pairing Guidance](../decisions/pairing.md).
