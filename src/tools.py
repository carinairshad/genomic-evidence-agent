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
