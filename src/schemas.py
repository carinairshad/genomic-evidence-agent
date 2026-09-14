from enum import Enum
from typing import List
from pydantic import BaseModel


class Status(str, Enum):
    EVIDENCE_PACKET_COMPLETE = "EVIDENCE_PACKET_COMPLETE"
    EVIDENCE_DOES_NOT_SUPPORT_SPECIFIED_CLAIM = (
        "EVIDENCE_DOES_NOT_SUPPORT_SPECIFIED_CLAIM"
    )
    CRITICAL_EVIDENCE_MISSING = "CRITICAL_EVIDENCE_MISSING"
    CONFLICT_REQUIRES_REVIEW = "CONFLICT_REQUIRES_REVIEW"
    PROVENANCE_FAILURE = "PROVENANCE_FAILURE"
    UNSUPPORTED_ASSERTION = "UNSUPPORTED_ASSERTION"
    VARIANT_IDENTITY_UNCERTAIN = "VARIANT_IDENTITY_UNCERTAIN"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNKNOWN = "UNKNOWN"


class NextAction(str, Enum):
    STOP_AND_REVIEW = "STOP_AND_REVIEW"
    CONTINUE_EVIDENCE_RETRIEVAL = "CONTINUE_EVIDENCE_RETRIEVAL"
    RESOLVE_VARIANT_IDENTITY = "RESOLVE_VARIANT_IDENTITY"
    VERIFY_PROVENANCE = "VERIFY_PROVENANCE"
    INVESTIGATE_CONFLICT = "INVESTIGATE_CONFLICT"
    REQUEST_MISSING_EVIDENCE = "REQUEST_MISSING_EVIDENCE"


class EvidenceItem(BaseModel):
    claim: str
    evidence_type: str
    source_label: str


class MissingEvidence(BaseModel):
    description: str
    reason: str


class Conflict(BaseModel):
    description: str
    sources: List[str]


class ProvenanceRecord(BaseModel):
    source_label: str
    source_location: str
    claim_verified: bool


class GenomicEvidenceReview(BaseModel):
    case_id: str
    gene: str
    variant: str
    evidence_supporting: List[EvidenceItem]
    evidence_against: List[EvidenceItem]
    missing_evidence: List[MissingEvidence]
    conflicts: List[Conflict]
    provenance: List[ProvenanceRecord]
    status: Status
    confidence: Confidence
    next_action: NextAction
    human_review_required: bool
