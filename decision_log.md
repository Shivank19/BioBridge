# Decision Log

A chronological index of every significant decision made in
this project, with a one-line reason and a pointer to the
relevant ADR where one exists.

---

| Date       | Decision                                  | Reason                                                                                                 | ADR     |
| ---------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------- |
| 2025-06-02 | Gradio for v1 UI                          | Fast to build, no frontend knowledge needed, explicitly a prototype choice                             | ADR 001 |
| 2025-06-02 | NetworkX before Neo4j                     | Schema needs to stabilize before committing to a database; NetworkX requires no server setup           | ADR 002 |
| 2025-06-02 | Abstracts only in v1, no full text        | PubMed API provides abstracts for all papers; full text coverage via PMC is patchy and adds noise      | ADR 003 |
| 2025-06-02 | PubTator for v1 NER                       | Pre-annotated on all of PubMed, no training required, official NCBI API                                | ADR 004 |
| 2025-06-02 | Delay GNN to v2                           | Graph needs to exist and be validated before training a model on it; interpretable baselines first     | ADR 005 |
| 2025-06-02 | Abstract Scorer interface from day one    | Ensures all scoring methods are swappable without changing any other layer                             | ADR 006 |
| 2025-06-02 | API layer as seam between pipeline and UI | Gradio app only talks to src/api/, making UI replaceable with React/Vue without touching pipeline code | ADR 007 |

---
