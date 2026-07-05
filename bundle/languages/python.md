---
type: language
title: Python
tags: [language, dynamic-typing, data-ecosystem]
---
Python is dynamically typed with optional type hints. Used by
[FastAPI](../backend/fastapi.md), which leans on those hints for
runtime request validation via Pydantic — one of the few cases where
Python type hints have real runtime effect, not just static checking.

Its main advantage over the JS/TS ecosystem is the data/ML tooling
(pandas, numpy, PyTorch), relevant if the backend needs to touch data
pipelines or models directly.
