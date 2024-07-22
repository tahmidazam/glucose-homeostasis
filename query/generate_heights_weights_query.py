import numpy

from constants.column_keys import ColumnKey
from constants.filter import Filter
from constants.table_name import TableName
from constants.item_category import ItemCategory


def generate_heights_weights_query(subject_ids: tuple[numpy.int64]) -> str:
    """
    Generate a query to retrieve the heights and weights of the patients in the ICU stays.

    Sets up a common table expression, which:

    - Converts height and weight values to metres and kilograms respectively.
    - Only allows records that have height- or weight-related item identifiers and are in the subject identifier tuple passed as an argument.
    - Only allows non-null numerical values, subject identifiers, ICU stay identifiers, and chart times; and non-zero numerical values.

    From this common table expression chart time, subject identifier, ICU stay identifier, and the rounded, converted height and weight values are selected.

    The records are finally sorted by subject identifier, ICU stay identifier, and chart time.
    :param subject_ids: The subject ids to include.
    :return: The SQL query.
    """
    subject_ids: tuple[int, ...] = tuple([int(n) for n in subject_ids])

    return f"""
    WITH {TableName.CONVERTED_VALUES.value} AS (
        SELECT 
            {ColumnKey.CHART_TIME.value}, 
            {ColumnKey.ITEM_ID.value}, 
            {ColumnKey.SUBJECT_ID.value}, 
            {ColumnKey.ICU_STAY_ID.value},
            CASE
                {"\n".join([f"WHEN {ColumnKey.ITEM_ID.value} = {itemid} THEN {ColumnKey.VALUE_NUMERICAL.value} * {ItemCategory.WEIGHT_CONVERSION_FACTORS.value[itemid]}" for itemid in ItemCategory.WEIGHT_ITEM_IDS.value])}
                {"\n".join([f"WHEN {ColumnKey.ITEM_ID.value} = {itemid} THEN {ColumnKey.VALUE_NUMERICAL.value} * {ItemCategory.HEIGHT_CONVERSION_FACTORS.value[itemid]}" for itemid in ItemCategory.HEIGHT_ITEM_IDS.value])}
                ELSE {ColumnKey.VALUE_NUMERICAL.value}
            END AS {ColumnKey.VALUE_NUMERICAL.value}
        FROM mimiciii.{TableName.CHARTEVENTS.value}
        WHERE {ColumnKey.VALUE_NUMERICAL.value} IS NOT NULL
        AND {ColumnKey.VALUE_NUMERICAL.value} <> 0
        AND {ColumnKey.ITEM_ID.value} IN {ItemCategory.WEIGHT_ITEM_IDS.value + ItemCategory.HEIGHT_ITEM_IDS.value}
        AND {ColumnKey.SUBJECT_ID.value} IN {subject_ids}
        AND {ColumnKey.ICU_STAY_ID.value} IS NOT NULL
        AND {ColumnKey.CHART_TIME.value} IS NOT NULL
    )
    
    SELECT 
        {ColumnKey.CHART_TIME.value}, 
        {ColumnKey.SUBJECT_ID.value}, 
        {ColumnKey.ICU_STAY_ID.value},
        CASE WHEN {ColumnKey.ITEM_ID.value} IN {ItemCategory.WEIGHT_ITEM_IDS.value} AND {ColumnKey.VALUE_NUMERICAL.value} < {Filter.WEIGHT_UPPER_BOUND.value} THEN ROUND(CAST({ColumnKey.VALUE_NUMERICAL.value} as numeric), 2) ELSE NULL END AS {ColumnKey.WEIGHT.value},
        CASE WHEN {ColumnKey.ITEM_ID.value} IN {ItemCategory.HEIGHT_ITEM_IDS.value} AND {ColumnKey.VALUE_NUMERICAL.value} < {Filter.HEIGHT_UPPER_BOUND.value} THEN ROUND(CAST({ColumnKey.VALUE_NUMERICAL.value} as numeric), 2) ELSE NULL END AS {ColumnKey.HEIGHT.value}
    FROM {TableName.CONVERTED_VALUES.value}
    ORDER BY {ColumnKey.SUBJECT_ID.value}, {ColumnKey.ICU_STAY_ID.value}, {ColumnKey.CHART_TIME.value}
    """
