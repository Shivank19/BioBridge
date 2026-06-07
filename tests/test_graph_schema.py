"""
test_graph_schema.py

Tests that the graph schema dataclasses are correctly defined, inherit properly, and that the NODE_TYPES and EDGE_TYPES registries are complete and point to the right classes.
"""

import pytest
from graph.graph_schema import (
    BaseNode, BaseEdge,
    DrugNode, DiseaseNode, GeneNode, PathwayNode,
    MechanismNode, PaperNode, ClinicalTrialNode,
    TreatsEdge, TargetsEdge, AssociatedWithEdge,
    CoOccursWithEdge, MentionedInEdge, RegulatesEdge,
    PartOfEdge, ImplicatedInEdge, HasTrialEdge,
    NODE_TYPES, EDGE_TYPES
)


# SECTION 1: Node instantiation
# These tests prove that each node class can be created without errors. If a dataclass has a field ordering problem or a wrong type, it will raise a TypeError here before any real data ever touches it.

def test_drug_node_instantiation():
    node = DrugNode(
        id="CHEMBL1234",
        name="Tofacitinib",
        description="JAK inhibitor",
        source="drugbank",
        drug_type="small molecule",
        synonyms=["Xeljanz"]
    )
    # assert checks the condition is True.
    # if False, pytest fails the test and shows the message after the comma.
    assert node.id == "CHEMBL1234", "DrugNode id was not set correctly"
    assert node.name == "Tofacitinib", "DrugNode name was not set correctly"
    assert node.synonyms == ["Xeljanz"], "DrugNode synonyms were not set correctly"


def test_disease_node_instantiation():
    node = DiseaseNode(
        id="MONDO:0005130",
        name="Celiac Disease",
        description="Autoimmune disease triggered by gluten",
        source="open_targets",
        mesh_id="D002446",
        efo_id="EFO_0001060",
        synonyms=["Coeliac Disease"]
    )
    assert node.id == "MONDO:0005130", "DiseaseNode id was not set correctly"
    assert node.mesh_id == "D002446", "DiseaseNode mesh_id was not set correctly"


def test_gene_node_instantiation():
    node = GeneNode(
        id="3600",
        name="IL15",
        description="Interleukin 15, involved in immune response",
        source="open_targets"
        # species is not passed — should default to "Homo sapiens"
    )
    assert node.species == "Homo Sapiens", "GeneNode species default was not set correctly"


def test_pathway_node_instantiation():
    # PathwayNode has no extra fields — only BaseNode fields
    node = PathwayNode(
        id="R-HSA-6785807",
        name="IL-15 signaling",
        description="Signaling pathway downstream of IL-15",
        source="reactome"
    )
    assert node.id == "R-HSA-6785807", "PathwayNode id was not set correctly"


def test_mechanism_node_instantiation():
    node = MechanismNode(
        id="intestinal-permeability",
        name="Intestinal Permeability",
        description="Dysfunction of tight junctions in the gut epithelium",
        source="literature"
    )
    assert node.name == "Intestinal Permeability", "MechanismNode name was not set correctly"


def test_paper_node_instantiation():
    node = PaperNode(
        id="12345678",
        name="Role of IL-15 in Celiac Disease",
        description="Study on IL-15 signaling in celiac patients",
        source="pubmed",
        journal="Gut",
        year=2021,
        abstract="This study investigates...",
        authors=["Smith J", "Jones A"]
    )
    assert node.id == "12345678", "PaperNode id (PMID) was not set correctly"
    assert node.year == 2021, "PaperNode year was not set correctly"
    assert len(node.authors) == 2, "PaperNode authors list length is wrong"


def test_clinical_trial_node_instantiation():
    node = ClinicalTrialNode(
        id="NCT01396213",
        name="Larazotide Phase 3 Trial",
        description="Phase 3 trial of larazotide for celiac disease",
        source="clinicaltrials.gov",
        status="Completed",
        phase="Phase 3",
        drug="Larazotide",
        condition="Celiac Disease"
    )
    assert node.phase == "Phase 3", "ClinicalTrialNode phase was not set correctly"
    assert node.status == "Completed", "ClinicalTrialNode status was not set correctly"


# SECTION 2: Default values work correctly
# These tests prove that fields with defaults do not require values to be passed in, and that the defaults are what we expect.

def test_drug_node_defaults():
    node = DrugNode(
        id="CHEMBL999",
        name="TestDrug",
        description="A test drug",
        source="test"
        # drug_type and synonyms are not passed — should use defaults
    )
    assert node.drug_type == "", "DrugNode drug_type default should be empty string"
    assert node.synonyms == [], "DrugNode synonyms default should be empty list"


def test_treats_edge_defaults():
    edge = TreatsEdge(
        source_id="CHEMBL1234",
        target_id="MONDO:0005130",
        source="open_targets",
        date_collected="2025-06-02"
        # paper_id and evidence_text not passed — should default to None
        # confidence not passed — should default to 0.0
    )
    assert edge.confidence == 0.0, "TreatsEdge confidence default should be 0.0"
    assert edge.paper_id is None, "TreatsEdge paper_id default should be None"
    assert edge.evidence_text is None, "TreatsEdge evidence_text default should be None"


# SECTION 3: Inheritance is correct 
# isinstance(obj, Class) checks if obj is an instance of Class or any subclass of Class. This proves the inheritance chain is intact. issubclass(Child, Parent) checks the class itself, not an instance.

def test_node_inheritance():
    node = DrugNode(
        id="CHEMBL1234",
        name="Tofacitinib",
        description="JAK inhibitor",
        source="drugbank"
    )
    # DrugNode should be a BaseNode because it inherits from it
    assert isinstance(node, BaseNode), "DrugNode should be an instance of BaseNode"
    # DrugNode should also be a DrugNode obviously
    assert isinstance(node, DrugNode), "DrugNode should be an instance of DrugNode"


def test_edge_inheritance():
    edge = TreatsEdge(
        source_id="CHEMBL1234",
        target_id="MONDO:0005130",
        source="open_targets",
        date_collected="2025-06-02"
    )
    assert isinstance(edge, BaseEdge), "TreatsEdge should be an instance of BaseEdge"
    assert isinstance(edge, TreatsEdge), "TreatsEdge should be an instance of TreatsEdge"


# SECTION 4: Registries are complete and correct
# These tests protect against accidentally adding a new node or edge type to the dataclasses but forgetting to add it to the registry dict. If you add a new node type later and forget the registry, this test fails and reminds you.

def test_node_types_registry_count():
    # we defined 7 node types: Disease, Drug, Gene, Pathway,
    # Mechanism, Paper, ClinicalTrial
    assert len(NODE_TYPES) == 7, (
        f"NODE_TYPES should have 7 entries but has {len(NODE_TYPES)}. "
        f"Did you add a new node type and forget to register it?"
    )


def test_edge_types_registry_count():
    # we defined 9 edge types
    assert len(EDGE_TYPES) == 9, (
        f"EDGE_TYPES should have 9 entries but has {len(EDGE_TYPES)}. "
        f"Did you add a new edge type and forget to register it?"
    )


def test_all_node_types_are_subclasses_of_base_node():
    # issubclass checks the class itself, not an instance of it
    # this loops through every value in the registry and checks
    # that it inherits from BaseNode
    for name, node_class in NODE_TYPES.items():
        assert issubclass(node_class, BaseNode), (
            f"NODE_TYPES['{name}'] = {node_class.__name__} does not "
            f"inherit from BaseNode"
        )


def test_all_edge_types_are_subclasses_of_base_edge():
    for name, edge_class in EDGE_TYPES.items():
        assert issubclass(edge_class, BaseEdge), (
            f"EDGE_TYPES['{name}'] = {edge_class.__name__} does not "
            f"inherit from BaseEdge"
        )


# SECTION 5: Registry keys match expected names
# These tests check that the string keys in the registries are exactly what we expect. If a key is misspelled, this catches it immediately rather than letting it cause a confusing KeyError later.

def test_node_registry_has_correct_keys():
    expected_keys = {
        "Drug", "Disease", "Gene", "Pathway",
        "Mechanism", "Paper", "ClinicalTrial"
    }
    actual_keys = set(NODE_TYPES.keys())
    assert actual_keys == expected_keys, (
        f"NODE_TYPES keys do not match expected. "
        f"Missing: {expected_keys - actual_keys}. "
        f"Extra: {actual_keys - expected_keys}."
    )


def test_edge_registry_has_correct_keys():
    expected_keys = {
        "Treats", "Targets", "AssociatedWith", "CoOccursWith",
        "MentionedIn", "Regulates", "PartOf", "ImplicatedIn", "HasTrial"
    }
    actual_keys = set(EDGE_TYPES.keys())
    assert actual_keys == expected_keys, (
        f"EDGE_TYPES keys do not match expected. "
        f"Missing: {expected_keys - actual_keys}. "
        f"Extra: {actual_keys - expected_keys}."
    )
