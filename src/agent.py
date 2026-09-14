from tools import (
    get_variant_case,
    retrieve_evidence,
    check_evidence_completeness,
)


MAX_ITERATIONS = 6


def run_review(case_id):
    """
    Run a small genomic evidence-review workflow.

    The agent:
    1. Observes the current state.
    2. Identifies the next sub-goal.
    3. Chooses one registered tool.
    4. Executes the tool.
    5. Updates the state.
    6. Checks whether it should stop.
    """

    # The state stores everything collected during the review.
    state = {
        "case_id": case_id,
        "case": None,
        "evidence": None,
        "missing_evidence": None,
        "status": "IN_PROGRESS",
        "next_action": None,
    }

    # Prevent the agent from running indefinitely.
    for iteration in range(MAX_ITERATIONS):

        print(f"\nIteration {iteration + 1}")
        print("Current state:", state)

        # ---------------------------------------------------------
        # 1. OBSERVE STATE → IDENTIFY NEXT SUB-GOAL
        # ---------------------------------------------------------

        if state["case"] is None:
            next_goal = "Retrieve the requested case."
            tool = get_variant_case

        elif state["evidence"] is None:
            next_goal = "Retrieve evidence for this case."
            tool = retrieve_evidence

        elif state["missing_evidence"] is None:
            next_goal = "Check whether required evidence categories are missing."
            tool = check_evidence_completeness

        else:
            # All three tools have been used.
            next_goal = "Stop evidence assembly and hand over for review."
            tool = None

        print("Next sub-goal:", next_goal)

        # ---------------------------------------------------------
        # 2. CHECK STOP CONDITION
        # ---------------------------------------------------------

        if tool is None:
            state["status"] = "HUMAN_REVIEW_REQUIRED"
            state["next_action"] = "STOP_AND_REVIEW"
            break

        # ---------------------------------------------------------
        # 3. CHOOSE AND EXECUTE REGISTERED TOOL
        # ---------------------------------------------------------

        if tool == get_variant_case:
            state["case"] = tool(case_id)

        elif tool == retrieve_evidence:
            state["evidence"] = tool(case_id)

        elif tool == check_evidence_completeness:
            state["missing_evidence"] = tool(
                state["case"],
                state["evidence"],
            )

        # ---------------------------------------------------------
        # 4. UPDATE STATE
        # ---------------------------------------------------------

        print("State updated.")

    else:
        # This happens if the loop reaches six iterations.
        state["status"] = "HUMAN_REVIEW_REQUIRED"
        state["next_action"] = "STOP_AND_REVIEW"
        print("Maximum iterations reached.")

    return state


# ---------------------------------------------------------
# Manual test
# ---------------------------------------------------------

result = run_review("GEA-003")

print("\nFINAL RESULT")
print(result)
