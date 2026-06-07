"""
graph_schema.py

Defines all node and edge types for the drug repurposing knowledge graph. All other modules import from here. Eliminates the need to hardcode node or edge structure anywhere else in the codebase.
"""

from dataclasses import dataclass, field

@dataclass
class BaseNode:
    id: str
    name: str
    description: str
    source: str

@dataclass
class DrugNode(BaseNode):
    drug_type: str = ""
    synonyms: list = field(default_factory=list)

@dataclass
class DiseaseNode(BaseNode):
    mesh_id: str = ""
    efo_id: str = ""
    synonyms: list = field(default_factory=list)
    
@dataclass
class GeneNode(BaseNode):
    species: str = "Homo Sapiens"
    synonyms: list = field(default_factory=list)

@dataclass
class PathwayNode(BaseNode):
    pass

@dataclass
class MechanismNode(BaseNode):
    pass

@dataclass
class PaperNode(BaseNode):
    journal: str = ""
    year: int = 0
    abstract: str = ""
    authors: list = field(default_factory=list)

@dataclass
class ClinicalTrialNode(BaseNode):
    status: str = ""
    phase: str = ""
    drug: str = ""
    condition: str = ""

@dataclass
class BaseEdge:
    source_id: str
    target_id: str
    source: str
    date_collected: str
    confidence: float = 0.0
    
@dataclass
class TreatsEdge(BaseEdge):
    paper_id: str | None = None
    evidence_text: str | None = None

@dataclass
class TargetsEdge(BaseEdge):
    paper_id: str | None = None
    evidence_text: str | None = None

@dataclass
class AssociatedWithEdge(BaseEdge):
    paper_id: str | None = None
    association_score: float = 0.0

@dataclass
class CoOccursWithEdge(BaseEdge):
    paper_id: str | None = None
    evidence_text: str | None = None

@dataclass
class MentionedInEdge(BaseEdge):
    pass
    
@dataclass
class RegulatesEdge(BaseEdge):
    paper_id: str | None = None
    evidence_text: str | None = None

@dataclass
class PartOfEdge(BaseEdge):
    pass
    
@dataclass
class ImplicatedInEdge(BaseEdge):
    paper_id: str | None = None
    evidence_text: str | None = None

@dataclass
class HasTrialEdge(BaseEdge):
    trial_phase: str | None = None
    trial_status: str | None = None


NODE_TYPES = {
    "Drug": DrugNode,
    "Disease": DiseaseNode,
    "Gene": GeneNode,
    "Pathway": PathwayNode,
    "Mechanism": MechanismNode,
    "Paper": PaperNode,
    "ClinicalTrial": ClinicalTrialNode,
}

EDGE_TYPES = {
    "Treats": TreatsEdge,
    "Targets": TargetsEdge,
    "AssociatedWith": AssociatedWithEdge,
    "CoOccursWith": CoOccursWithEdge,
    "MentionedIn": MentionedInEdge,
    "Regulates": RegulatesEdge,
    "PartOf": PartOfEdge,
    "ImplicatedIn": ImplicatedInEdge,
    "HasTrial": HasTrialEdge,
}