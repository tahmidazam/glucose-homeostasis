import logging

from tabulate import tabulate


def log_identifier_summary(icu_stay_ids: [int], subject_ids: [int], hospital_admission_ids: [int]):
    """
    Logs the summary of unique identifiers.
    :param icu_stay_ids: The unique ICU stay identifiers.
    :param subject_ids: The unique subject identifiers.
    :param hospital_admission_ids: The unique hospital admission identifiers.
    """
    table: str = tabulate([["ICU stay", len(icu_stay_ids)], ["Subject", len(subject_ids)],
                           ["Hospital admission", len(hospital_admission_ids)]], headers=["Identifier", "Count"],
                          tablefmt="pretty")

    # Newline prefixed to prevent the logging prefix from offsetting top table border.
    logging.info("\n" + table)
