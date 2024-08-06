import pandas as pd
import sqlalchemy

from curation.constants import ColumnKey
from curation.plot_count_history import plot_count_history
from .lookup import generate_ndc_lookup, generate_gsn_lookup, generate_name_lookup, generate_class_lookup
from .plotting import plot_classification_performance, plot_class_dimensions
from .query_prescriptions import query_prescriptions


def generate_df_prescriptions(engine: sqlalchemy.Engine) -> pd.DataFrame:
    # Query the prescriptions table.
    df_prescriptions = query_prescriptions(engine=engine)

    # Initialising the count history of unidentified prescriptions.
    unidentified_prescription_count: tuple[tuple[str, int], ...] = ()
    unidentified_prescription_count += (("initial", len(df_prescriptions)),)

    # Looking up NDCs and merging found RxCUIs in.
    df_ndc_lookup = generate_ndc_lookup(df_prescriptions['ndc'])
    df_prescriptions = pd.merge(left=df_prescriptions, right=df_ndc_lookup, how='left', on='ndc')

    # Counting unidentified prescriptions after NDC lookup.
    df_unidentified_prescriptions = df_prescriptions[df_prescriptions[ColumnKey.RXCUI.value].isna()]
    unidentified_prescription_count += (("NDC", len(df_unidentified_prescriptions)),)

    # Looking up GSNs and merging found RxCUIs in.
    df_gsn_lookup = generate_gsn_lookup(s_gsn=df_unidentified_prescriptions['gsn'])
    df_prescriptions = pd.merge(left=df_prescriptions, right=df_gsn_lookup, how='left', on=['gsn'])
    df_prescriptions[ColumnKey.RXCUI.value] = df_prescriptions['rxcui_x'].fillna(df_prescriptions['rxcui_y'])
    df_prescriptions.drop(columns=['rxcui_x', 'rxcui_y'], inplace=True)

    # Counting unidentified prescriptions after GSN lookup.
    df_unidentified_prescriptions = df_prescriptions[df_prescriptions[ColumnKey.RXCUI.value].isna()]
    unidentified_prescription_count += (("GSN", len(df_unidentified_prescriptions)),)

    # Looking up drug names and merging found RxCUIs in.
    df_name_lookup = generate_name_lookup(df_unidentified_prescriptions[ColumnKey.DRUG.value],
                                          column_key=ColumnKey.DRUG)
    df_prescriptions = pd.merge(left=df_prescriptions, right=df_name_lookup, how='left', on=['drug'])
    df_prescriptions[ColumnKey.RXCUI.value] = df_prescriptions['rxcui_x'].fillna(df_prescriptions['rxcui_y'])
    df_prescriptions.drop(columns=['rxcui_x', 'rxcui_y'], inplace=True)

    # Counting unidentified prescriptions after drug name lookup.
    df_unidentified_prescriptions = df_prescriptions[df_prescriptions[ColumnKey.RXCUI.value].isna()]
    unidentified_prescription_count += (("drug name", len(df_unidentified_prescriptions)),)

    # Looking up generic drug names and merging found class names in.
    df_generic_name_lookup = generate_name_lookup(
        s_value=df_unidentified_prescriptions[ColumnKey.DRUG_NAME_GENERIC.value],
        column_key=ColumnKey.DRUG_NAME_GENERIC
    )
    df_prescriptions = pd.merge(
        left=df_prescriptions,
        right=df_generic_name_lookup,
        how='left',
        on=[ColumnKey.DRUG_NAME_GENERIC.value]
    )
    df_prescriptions[ColumnKey.RXCUI.value] = df_prescriptions['rxcui_x'].fillna(df_prescriptions['rxcui_y'])
    df_prescriptions.drop(columns=['rxcui_x', 'rxcui_y'], inplace=True)

    # Counting unidentified prescriptions after drug name lookup.
    df_unidentified_prescriptions = df_prescriptions[df_prescriptions[ColumnKey.RXCUI.value].isna()]
    unidentified_prescription_count += (("generic drug name", len(df_unidentified_prescriptions)),)

    # Plotting the history of the number of unidentified prescriptions.
    plot_count_history(
        count_history=unidentified_prescription_count,
        title='Unidentified prescription count',
        upper_x_lim=6000000,
        left=0.2
    )

    # Classifying drugs using their RxCUI and merging them in.
    df_class_lookup = generate_class_lookup(df_prescriptions[ColumnKey.RXCUI.value])
    df_prescriptions = pd.merge(left=df_prescriptions, right=df_class_lookup, how='left', on=ColumnKey.RXCUI.value)

    # Plotting the classification performance and class dimensions.
    plot_classification_performance(df_prescriptions=df_prescriptions)
    plot_class_dimensions(df_prescriptions=df_prescriptions)

    return df_prescriptions
