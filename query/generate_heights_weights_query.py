import numpy

from constants.column_keys import ColumnKey
from constants.filter_info import FilterInfo
from constants.table_name import TableName

HEIGHT_ITEM_IDS: [int, ...] = (1394, 226707, 226730)
HEIGHT_CONVERSION_FACTORS = {
    1394: 0.0254,
    226707: 0.0254,
    226730: 0.01
}

WEIGHT_ITEM_IDS: tuple[int, ...] = (580, 581, 763, 226846, 224639, 226512, 226531)
WEIGHT_CONVERSION_FACTORS = {
    580: 1,
    581: 1,
    763: 1,
    224639: 1,
    226512: 1,
    226531: 0.45359237,
    226846: 1
}


def generate_heights_weights_query(subject_ids: tuple[numpy.int64]) -> str:
    subject_ids: tuple[int, ...] = tuple([int(id) for id in subject_ids])

    return f"""
    WITH {TableName.CONVERTED_VALUES.value} AS (
        SELECT 
            {ColumnKey.CHART_TIME.value}, 
            {ColumnKey.ITEM_ID.value}, 
            {ColumnKey.SUBJECT_ID.value}, 
            {ColumnKey.ICU_STAY_ID.value},
            CASE
                {"\n".join([f"WHEN {ColumnKey.ITEM_ID.value} = {itemid} THEN {ColumnKey.VALUE_NUMERICAL.value} * {WEIGHT_CONVERSION_FACTORS[itemid]}" for itemid in WEIGHT_ITEM_IDS])}
                {"\n".join([f"WHEN {ColumnKey.ITEM_ID.value} = {itemid} THEN {ColumnKey.VALUE_NUMERICAL.value} * {HEIGHT_CONVERSION_FACTORS[itemid]}" for itemid in HEIGHT_ITEM_IDS])}
                ELSE {ColumnKey.VALUE_NUMERICAL.value}
            END AS {ColumnKey.VALUE_NUMERICAL.value}
        FROM mimiciii.{TableName.CHARTEVENTS.value}
        WHERE {ColumnKey.VALUE_NUMERICAL.value} IS NOT NULL
        AND {ColumnKey.VALUE_NUMERICAL.value} <> 0
        AND {ColumnKey.ITEM_ID.value} IN {WEIGHT_ITEM_IDS + HEIGHT_ITEM_IDS}
        AND {ColumnKey.SUBJECT_ID.value} IN {subject_ids}
        AND {ColumnKey.ICU_STAY_ID.value} IS NOT NULL
        AND {ColumnKey.CHART_TIME.value} IS NOT NULL
    )
    
    SELECT 
        {ColumnKey.CHART_TIME.value}, 
        {ColumnKey.SUBJECT_ID.value}, 
        {ColumnKey.ICU_STAY_ID.value},
        CASE WHEN {ColumnKey.ITEM_ID.value} IN {WEIGHT_ITEM_IDS} AND {ColumnKey.VALUE_NUMERICAL.value} < 300 THEN ROUND(CAST({ColumnKey.VALUE_NUMERICAL.value} as numeric), 2) ELSE NULL END AS {ColumnKey.WEIGHT.value},
        CASE WHEN {ColumnKey.ITEM_ID.value} IN {HEIGHT_ITEM_IDS} AND {ColumnKey.VALUE_NUMERICAL.value} < 3 THEN ROUND(CAST({ColumnKey.VALUE_NUMERICAL.value} as numeric), 2) ELSE NULL END AS {ColumnKey.HEIGHT.value}
    FROM {TableName.CONVERTED_VALUES.value}
    ORDER BY {ColumnKey.SUBJECT_ID.value}, {ColumnKey.ICU_STAY_ID.value}, {ColumnKey.CHART_TIME.value}
    """
