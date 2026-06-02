# ADR 001: Use Gradio for V1 UI

## Date

2025-06-02

## Status

Accepted

## Decision

Use Gradio as the UI framework for the v1 prototype.

## Context

The v1 system needs a way to display ranked drug candidates, evidence paths and paper references to a researcher. The UI for v1 is a prototype and its job is to prove the system works, not to be a polished product.

## Alternatives Considered

- **Streamlit** — similar simplicity, more popular, but less flexible for custom component layouts.
- **React + Cytoscape.js** — the right long-term choice for graph visualization, but overkill for a prototype and requires
  frontend build tooling.
- **Jupyter notebook** — too informal, not shareable as a demo.

## Reason for Choice

Gradio is fast to build with, requires no frontend knowledge and supports multi-page layouts via gr.Blocks which maps cleanly onto our three pages: Disease Overview, Candidate Ranking, Evidence Inspector. It is explicitly a prototype choice. The API layer design means swapping Gradio for React later requires no changes to any layer below src/api/.

## Consequences

- V1 will not have interactive graph visualization. That moves to v2 with React + Cytoscape.js.
- Gradio's styling is limited. The UI will be functional, not polished.
- This is acceptable because v1's goal is validation, not presentation.
