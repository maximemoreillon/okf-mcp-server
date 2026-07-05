---
type: language
title: TypeScript
tags: [language, javascript-family, static-typing]
---
TypeScript adds static types on top of JavaScript. Used by
[React](../frontend/react.md), [Vue](../frontend/vue.md), and
[Express](../backend/express.md). Its main advantage in a full-stack
JS setup is sharing type definitions between frontend and backend
without a separate schema language.

Tradeoff: types are erased at compile time (no runtime validation),
so request/response validation still needs a separate library (zod,
io-ts) if you want runtime guarantees.
