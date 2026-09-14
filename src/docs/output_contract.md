# Genomic Evidence Agent — Output Contract

## Purpose

The output contract defines the standard structure used by the Genomic Evidence Agent to report an evidence-review result.

The structure is designed to preserve evidence, uncertainty, conflicts, provenance and human review.

It is not a diagnostic report and does not perform autonomous pathogenicity classification.

## Required fields

### case_id
Identifies the synthetic test case being reviewed.

### gene
Stores the gene associated with the variant in the test case.

### variant
Stores the variant identifier used in the case.

### evidence_supporting
Lists evidence items that support the specific evidence question being reviewed.

Each evidence item contains:
- claim
- evidence_type
- source_label

### evidence_against
Lists evidence items that do not support, or may argue against, the specific evidence question.

Each evidence item contains:
- claim
- evidence_type
- source_label

### missing_evidence
Records important evidence that is not available in the supplied evidence set.

Each missing-evidence item contains:
- description
- reason

Missing evidence must not be treated as evidence of absence.

### conflicts
Records disagreements between evidence sources.

Each conflict contains:
- description
- sources

The system must not silently select one conflicting source over another.

### provenance
Records where each substantive evidence claim came from.

Each provenance record contains:
- source_label
- source_location
- claim_verified

Claims without adequate provenance require review.

### status
Describes the workflow state of the evidence review.

Allowed values:

- `EVIDENCE_PACKET_COMPLETE`
- `EVIDENCE_DOES_NOT_SUPPORT_SPECIFIED_CLAIM`
- `CRITICAL_EVIDENCE_MISSING`
- `CONFLICT_REQUIRES_REVIEW`
- `PROVENANCE_FAILURE`
- `UNSUPPORTED_ASSERTION`
- `VARIANT_IDENTITY_UNCERTAIN`
- `HUMAN_REVIEW_REQUIRED`

These are workflow states, not clinical diagnoses or pathogenicity classifications.

### confidence
Describes confidence in the evidence-assembly process.

Allowed values:

- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`

Confidence does not represent confidence that a variant is pathogenic or benign.

### next_action
Specifies the next workflow action.

Allowed values:

- `STOP_AND_REVIEW`
- `CONTINUE_EVIDENCE_RETRIEVAL`
- `RESOLVE_VARIANT_IDENTITY`
- `VERIFY_PROVENANCE`
- `INVESTIGATE_CONFLICT`
- `REQUEST_MISSING_EVIDENCE`

### human_review_required
A Boolean field indicating whether scientist review is required.

Allowed values:

- `true`
- `false`

Human review remains mandatory for consequential scientific interpretation.

## Safety boundary

The output contract does not contain fields for:

- diagnosis;
- autonomous pathogenicity classification;
- patient-care recommendations.

The system must preserve uncertainty and must not invent evidence, sources or citations.
