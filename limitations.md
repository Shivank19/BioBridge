# Known Limitations

A living document updated throughout the project as new
limitations are discovered.

---

## V1 Limitations

### Data coverage

- **Abstracts only.** V1 uses PubMed abstracts, not full text.
  Claims buried in results sections, figure captions, or
  supplementary material will be missed. This likely
  underrepresents mechanistic detail.

- **English language only.** PubMed queries return English
  abstracts by default. Non-English literature is not covered.

- **Source coverage.** V1 uses PubMed, PubTator, Open Targets,
  and ClinicalTrials.gov. Relevant information in STRING,
  DrugBank, UniProt, Reactome, or OMIM is not included until
  later versions.

- **Open access bias.** Full text will only be added from
  PubMed Central open access papers. Paywalled literature
  is excluded for ethical and legal reasons.

### NLP and entity extraction

- **Co-occurrence is not causation.** A drug and a gene
  appearing in the same abstract does not mean the drug
  targets that gene. Co-occurrence edges in the graph carry
  low confidence scores but are still a source of noise.

- **PubTator errors.** Pre-trained NER models make mistakes.
  Entity boundaries may be wrong, entities may be missed,
  and normalization to canonical IDs will have errors
  especially for drug synonyms and gene aliases.

- **Negation is not handled in v1.** A sentence saying "Drug X
  does NOT inhibit Gene Y" may still produce a co-occurrence
  edge. This is a known source of false positives.

### Graph and ranking

- **The graph is only as good as its sources.** If a
  biological relationship is not documented in the literature
  or databases we use, it will not appear in the graph.

- **Ranking is not clinical validation.** A high-ranked drug
  candidate has strong graph connectivity to the disease. It
  does not have proven clinical efficacy.

- **Bias toward well-studied drugs.** Drugs with more
  published literature will score higher on evidence count
  and path metrics simply because more is written about them,
  not necessarily because they are more relevant.

### Scope

- **Celiac disease only in v1.** The system is not intended for other diseases in v1.

- **Hypothesis generation only.** This tool is for
  computational researchers exploring mechanistic hypotheses.
  It is not for clinical or patient-facing use under any
  circumstances.

---

## Planned improvements in later versions

- Full text ingestion via PMC OA API (v1.5)
- Negation detection in relation extraction (v1.5)
- STRING and DrugBank integration (v1.5)
- Graph attention network scoring with learned explanations (v2)
- Interactive graph visualization (v2)
- Multi-disease support (v2)

---
