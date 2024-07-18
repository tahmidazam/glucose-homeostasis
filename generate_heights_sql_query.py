import numpy

from column_keys import ColumnKey
from table_name import TableName

HEIGHT_ITEM_IDS = (1394, 226707, 226730)
HEIGHT_CONVERSION_FACTORS = {
    1394: 0.0254,
    226707: 0.0254,
    226730: 0.01
}


def generate_heights_sql_query(subject_ids: tuple[numpy.int64, ...]) -> str:
    subject_ids: tuple[int, ...] = tuple([int(n) for n in subject_ids])

    return f"""
            SELECT
                CASE
                    {"\n".join([f"WHEN {ColumnKey.ITEM_ID.value} = {itemid} THEN {ColumnKey.VALUE_NUMERICAL.value} * {HEIGHT_CONVERSION_FACTORS[itemid]}" for itemid in HEIGHT_ITEM_IDS])}
                ELSE {ColumnKey.VALUE_NUMERICAL.value}
            END AS {ColumnKey.HEIGHT.value},
            {ColumnKey.VALUE_NUMERICAL.value},
            {ColumnKey.SUBJECT_ID.value}, 
            {ColumnKey.ICU_STAY_ID.value}, 
            {ColumnKey.CHART_TIME.value}
            FROM mimiciii.{TableName.CHARTEVENTS.value}
            WHERE {ColumnKey.ITEM_ID.value} IN {HEIGHT_ITEM_IDS}
            AND {ColumnKey.VALUE_NUMERICAL.value} IS NOT NULL
            AND {ColumnKey.SUBJECT_ID.value} IS NOT NULL
            AND {ColumnKey.ICU_STAY_ID.value} IS NOT NULL
            AND {ColumnKey.SUBJECT_ID.value} IN {subject_ids}
            """
