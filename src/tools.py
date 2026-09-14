import json


def get_variant_case(case_id):
    """
    Read data/cases.json and return the case with the given case_id.

    Input:
        case_id (str): The ID of the case to find, e.g. "GEA-001"

    Output:
        dict: The case information from cases.json

    Raises:
        ValueError: If the case_id is not found.
    """

    # Open the local cases file.
    with open("data/cases.json", "r", encoding="utf-8") as file:
        cases = json.load(file)

    # Look through the cases for the requested case ID.
    for case in cases:
        if case["case_id"] == case_id:
            return case

    # Give a clear error if the case does not exist.
    raise ValueError(f"Case '{case_id}' was not found.")
import json


def retrieve_evidence(case_id):
    """
    Read data/evidence.json and return only evidence for the given case_id.

    Input:
        case_id (str): The ID of the case, e.g. "GEA-001"

    Output:
        list: Evidence items belonging only to that case

    Raises:
        ValueError: If no evidence exists for the case_id.
    """

    # Open the local evidence file.
    with open("data/evidence.json", "r", encoding="utf-8") as file:
        evidence = json.load(file)

    # Keep only evidence that belongs to the requested case.
    matching_evidence = []

    for item in evidence:
        if item["case_id"] == case_id:
            matching_evidence.append(item)

    # Give a clear error if no evidence was found.
    if not matching_evidence:
        raise ValueError(f"No evidence found for case '{case_id}'.")

    return matching_evidence
