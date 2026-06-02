# BioBridge: Connecting Biomedical Evidence for Drug Repurposing

BioBridge is a research tool that builds an evidence-backed knowledge graph to surface drug repurposing candidates for celiac disease, with mechanistic explanations grounded in biomedical literature and public databases.

## What this is

A hypothesis-generation tool for researchers. It connects drugs, genes, pathways and mechanisms to celiac disease by mining
PubMed abstracts and open biomedical databases, then ranks candidate drugs by the strength and diversity of their evidence paths through the graph.

## What this is NOT

This is not a clinical recommendation system. Nothing produced by this tool should be interpreted as medical advice or a validated treatment recommendation. All candidates surfaced are hypotheses for further investigation only.

## Who this is for

Computational biology researchers and bioinformaticians exploring mechanistic links between drugs and immune-mediated diseases. This tool is not intended for clinical or patient-facing use.

## Sanity check candidates

The system is validated throughout development against three known celiac disease candidates with well-understood mechanisms:

- **Larazotide**: in Phase 3 trials, targets intestinal
  permeability
- **AMG 714**: anti-IL-15 monoclonal antibody, targets the
  core celiac immune pathway
- **Tofacitinib**: JAK inhibitor with mechanistic support
  via JAK-STAT and IL-15 signaling

If these three do not appear in the top 20 ranked candidates, something is wrong with the pipeline.

## Version roadmap

**v1 (current):** NetworkX graph, PubMed abstracts, PubTator NER, three interpretable scorers (evidence count, path, PageRank), Gradio interface. Goal is a working, validated prototype.

**v1.5:** Migrate graph backend to Neo4j, add PubMedBERT relation extraction, add TransE embedding scorer via PyKEEN.

**v2:** Add Graph Attention Network scorer via PyTorch Geometric, attention-based explanations, React and Cytoscape.js frontend with interactive graph visualization.

## Running the project

```bash
python -m venv venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/01_collect_pubmed.py
python scripts/02_extract_entities.py
python scripts/03_build_graph.py
python scripts/04_rank_candidates.py
python scripts/05_generate_explanations.py
gradio app/gradio_app.py
```

## Limitations

See `limitations.md` for a full list of known limitations.

## License

For research use only.
