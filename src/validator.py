from schemas import (
    Status,
    Confidence,
    NextAction,
)


def validate_review(review):
    """
    Deterministically validate a Genomic Evidence Agent review.

    Input:
        review: A GenomicEvidenceReview object.

    Output:
        True if the review passes all validation rules.

    Raises:
        ValueError if a safety or schema rule is violated.
    """

    # ---------------------------------------------------------
    # 1. Check that enum values are approved.
    # ---------------------------------------------------------

    if review.status not in Status:
        raise ValueError(
            f"Invalid status: {review.status}"
        )

    if review.confidence not in Confidence:
        raise ValueError(
            f"Invalid confidence: {review.confidence}"
        )

    if review.next_action not in NextAction:
        raise ValueError(
            f"Invalid next_action: {review.next_action}"
        )

    # ---------------------------------------------------------
    # 2. Critical missing evidence cannot be marked as
    #    supported for review.
    # ---------------------------------------------------------

    if (
        review.status == "SUPPORTED_FOR_REVIEW"
        and len(review.missing_evidence) > 0
    ):
        raise ValueError(
            "Critical missing evidence cannot be paired "
            "with SUPPORTED_FOR_REVIEW."
        )

    # ---------------------------------------------------------
    # 3. A material conflict requires conflict or
    #    human-review status.
    # ---------------------------------------------------------

    if len(review.conflicts) > 0:
        allowed_conflict_statuses = {
            Status.CONFLICT_REQUIRES_REVIEW,
            Status.HUMAN_REVIEW_REQUIRED,
        }

        if review.status not in allowed_conflict_statuses:
            raise ValueError(
                "Material source conflict requires "
                "conflict or human-review status."
            )

    # ---------------------------------------------------------
    # 4. Substantive evidence claims must have provenance.
    # ---------------------------------------------------------

    substantive_claims = (
        review.evidence_supporting
        + review.evidence_against
    )

    for claim in substantive_claims:
        if not claim.source_label:
            raise ValueError(
                "Substantive claims must have provenance."
            )

    # ---------------------------------------------------------
    # 5. Diagnosis or autonomous clinical classification
    #    must never be allowed.
    # ---------------------------------------------------------

    prohibited_terms = [
        "diagnose",
        "diagnosis",
        "pathogenic",
        "benign",
        "clinical classification",
    ]

    for claim in substantive_claims:
        text = claim.claim.lower()

        for term in prohibited_terms:
            if term in text:
                raise ValueError(
                    "Diagnosis or autonomous clinical "
                    "classification is not allowed."
                )

    # ---------------------------------------------------------
    # 6. Human review cannot be paired with an autonomous
    #    clinical action.
    # ---------------------------------------------------------

    autonomous_actions = {
        "DIAGNOSE",
        "CLASSIFY_VARIANT",
        "RECOMMEND_TREATMENT",
        "TAKE_CLINICAL_ACTION",
    }

    if (
        review.human_review_required
        and review.next_action in autonomous_actions
    ):
        raise ValueError(
            "Human review cannot be paired with "
            "an autonomous clinical action."
        )

    return True
  REPAIR_PROMPT = """
You are repairing a genomic evidence-review output that failed schema or
business-rule validation.

VALIDATION ERRORS
The validator will provide the exact validation errors. Treat these errors
as the only fields that may require correction.

REPAIR RULES
1. Correct ONLY fields identified by the validation errors.
2. Preserve all supported evidence, source labels, provenance, conflicts,
   uncertainty, and other valid fields unchanged.
3. Never invent missing evidence, sources, citations, results, or values.
4. Never remove or weaken supported evidence to make validation pass.
5. Use ONLY the approved enum values defined by the output schema.
6. Do not make a diagnosis or autonomous pathogenicity/benign classification.
7. If a required value is genuinely unavailable, preserve that uncertainty
   using the appropriate allowed schema value rather than inventing one.
8. Return ONLY the corrected structured output matching the schema exactly.
9. Do not include explanations, commentary, or markdown outside the output.

REPAIR LIMIT
Maximum repair attempts: 2.

If validation still fails after the second repair attempt, do not continue
repairing. Fail safely and require human review.
"""
