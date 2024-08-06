from curation.constants import ColumnKey
from curation.prescriptions.get_approximate_match import GetApproximateMatchResponse, get_approximate_match, Candidate


def identify_drug_using_approximate_match(row, column_key: ColumnKey):
    drug_raw_value: str = row[column_key.value].strip()

    if drug_raw_value is None or drug_raw_value == '':
        return row

    get_approximate_match_response: GetApproximateMatchResponse = get_approximate_match(term=drug_raw_value)

    sorted_candidates: list[Candidate] = sorted(get_approximate_match_response.approximate_group.candidate,
                                                key=lambda x: x.score, reverse=True)

    if len(sorted_candidates) == 0:
        return row

    rxcui = sorted_candidates[0].rxcui

    row['rxcui'] = rxcui

    return row
