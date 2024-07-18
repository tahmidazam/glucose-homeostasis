import numpy

from constants.column_keys import ColumnKey
from constants.table_name import TableName

WEIGHT_ITEM_IDS: tuple[int, int, int, int, int, int, int] = (580, 581, 763, 226846, 224639, 226512, 226531)
WEIGHT_CONVERSION_FACTORS = {
    580: 1,
    581: 1,
    763: 1,
    224639: 1,
    226512: 1,
    226531: 0.45359237,
    226846: 1
}


def generate_weights_sql_query(subject_ids: tuple[numpy.int64, ...]) -> str:
    subject_ids: tuple[int, ...] = tuple([int(n) for n in subject_ids])

    return f"""SELECT
                CASE
                    {"\n".join([f"WHEN {ColumnKey.ITEM_ID.value} = {itemid} THEN {ColumnKey.VALUE_NUMERICAL.value} * {WEIGHT_CONVERSION_FACTORS[itemid]}" for itemid in WEIGHT_ITEM_IDS])}
                ELSE {ColumnKey.VALUE_NUMERICAL.value}
            END AS {ColumnKey.WEIGHT.value},
            {ColumnKey.VALUE_NUMERICAL.value},
            {ColumnKey.SUBJECT_ID.value}, 
            {ColumnKey.ICU_STAY_ID.value}, 
            {ColumnKey.CHART_TIME.value}
            FROM mimiciii.{TableName.CHARTEVENTS.value}
            WHERE {ColumnKey.ITEM_ID.value} IN {WEIGHT_ITEM_IDS}
            AND {ColumnKey.VALUE_NUMERICAL.value} IS NOT NULL
            AND {ColumnKey.SUBJECT_ID.value} IS NOT NULL
            AND {ColumnKey.ICU_STAY_ID.value} IS NOT NULL
            AND {ColumnKey.SUBJECT_ID.value} IN {tuple(subject_ids)}
            """
