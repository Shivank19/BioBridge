# Research Log

A running diary of findings, surprises, and dead ends. Not formal. Updated throughout the project.

---

## 2025-06-02 : Project Start

### What I already know about celiac disease biology

Celiac disease is an autoimmune condition triggered by gluten ingestion in genetically predisposed individuals. The genetic risk is primarily driven by HLA-DQ2 and HLA-DQ8 haplotypes. When gluten is ingested, gliadin peptides cross the intestinal epithelium and trigger an immune response. Tissue transglutaminase (tTG) deamidates gliadin peptides, making them more immunogenic. This leads to T-cell activation, villous atrophy, and malabsorption.

Key molecular players:

- IL-15: central cytokine in the celiac immune response, drives intraepithelial lymphocyte expansion
- JAK-STAT pathway: downstream of IL-15 signaling
- HLA-DQ2/DQ8: MHC class II molecules presenting gliadin peptides to CD4+ T cells
- tTG (TGM2): enzyme that deamidates gliadin, creates neo-epitopes
- Zonulin: regulates intestinal tight junction permeability

The only current treatment is a strict lifelong gluten-free diet. There is no approved pharmacological treatment.

### Why I chose this project

Celiac disease has a well-understood mechanism, a small number of known drug candidates in trials, and active research into immunological treatments. This makes it a good case study because I have ground truth to validate against. The system should be able to recover larazotide, AMG 714, and tofacitinib through graph paths and if it cannot, I know something is wrong.

### What I expect to be hardest

Entity normalization : mapping drug and gene synonyms across different databases to the same canonical identifier is going to be messy. The same drug appears under a brand name, a generic name, a CHEMBL ID, and a ChEBI ID depending on the source. Getting these to resolve to the same node in the graph is the part I expect to produce the most bugs.

---
