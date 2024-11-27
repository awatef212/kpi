
import pandas as pd
import time

from loguru import logger


from .calcul import calculate_reco_intermediaire_2
from .data import get_data


def get_taux_reco():
    df_simulateur_reco, df_prod, df_brand, df_delta = get_data(False)
    start = time.time()



    df_prod_melt = df_prod.melt(
        id_vars=["CodeAA", "Brand"], var_name="Question", value_name="Valeur"
    )
    df_prod_melt["Question"] = df_prod_melt["Question"].replace('_', '.')

    df_merged = df_prod_melt.merge(
        df_simulateur_reco[
            [
                "Question",
                "coefficients",
                "min_max",
            ]
        ],
        on="Question",
        how="left",
    )
    df_merged["Valeur"] = pd.to_numeric(df_merged["Valeur"], errors="coerce")
    df_merged["coefficients"] = pd.to_numeric(
        df_merged["coefficients"], errors="coerce"
    )
    intermediaire_values = calculate_reco_intermediaire_2(df_merged, False)
    df_delta["delta"] = pd.to_numeric(df_delta["delta"], errors="coerce")
    df_merged_joined = df_merged.merge(
        intermediaire_values,
        left_on=[
            "CodeAA",
            "Brand",
            "Question",
            "Valeur",
            "coefficients",
            "min_max",
        ],
        right_on=[
            "CodeAA",
            "Brand",
            "Question",
            "Valeur",
            "coefficients",
            "min_max",
        ],
        how="left",
    )
    intermediaire_values_renamed = intermediaire_values.rename(
        columns={"reco_intermediaire": "reco_intermediaire_new"}
    )
    df_merged_joined = df_merged.merge(
        intermediaire_values_renamed,
        left_on=[
            "CodeAA",
            "Brand",
            "Question",
            "Valeur",
            "coefficients",
            "min_max",
        ],
        right_on=[
            "CodeAA",
            "Brand",
            "Question",
            "Valeur",
            "coefficients",
            "min_max",
        ],
        how="left",
    )
    columns_to_drop = ["reco_intermediaire", "non_reco_intermediaire"]
    for col in columns_to_drop:
        if col in df_merged_joined.columns:
            df_merged_joined.drop(col, axis=1, inplace=True)
    df_merged_joined.rename(
        columns={"reco_intermediaire_new": "reco_intermediaire"}, inplace=True
    )
    constante_reco = df_simulateur_reco[df_simulateur_reco["Question"] == "_"][
        "coefficients"
    ].iloc[0]

    # url = f"mysql+mysqlconnector://{MYSQL_DB_USER}:{MYSQL_DB_PASSWORD}@{MYSQL_DB_HOST}/{MYSQL_DB_NAME}"
    # engine = create_engine(url)
    # df_merged_joined.to_sql("df_merged", engine, if_exists="replace", index=False)
    # engine.dispose()

    df_grouped = (
        df_merged_joined.groupby(["CodeAA", "Brand"])
        .agg({"reco_intermediaire": "sum"})
        .reset_index()
    )

    df_grouped.rename(
        columns={"reco_intermediaire": "reco"},
        inplace=True,
    )
    df_grouped = pd.merge(
        df_grouped,
        df_delta[["Brand", "CodeAA", "delta"]],
        on=["Brand", "CodeAA"],
        how="left",
    )

    df_grouped["reco"] = df_grouped["reco"] + float(constante_reco)
    df_grouped["reco"] += df_grouped["delta"]
    df_grouped["ranking"] = df_grouped.groupby("CodeAA")["reco"].rank(
        method="min", ascending=False
    )

    df_result = (
        df_grouped.groupby(["Brand"])
        .agg(
            {
                "reco": "sum",
            }
        )
        .reset_index()
    )

    total_ranks_per_brand = df_grouped.groupby("Brand")["ranking"].count()

    ranking_counts_per_brand = df_grouped.groupby(["Brand", "ranking"]).size()

    percentage_per_rank_and_brand = (
        ranking_counts_per_brand / total_ranks_per_brand
    ) * 100

    percentage_per_rank_pivot = percentage_per_rank_and_brand.unstack().fillna(0)

    percentage_per_rank_pivot = percentage_per_rank_pivot[[1, 2, 3]]

    percentage_per_rank_pivot.columns = [
        "pourcentage_1er",
        "pourcentage_2eme",
        "pourcentage_3eme",
    ]

    df_result = df_result.merge(percentage_per_rank_pivot, on="Brand", how="left")

    df_result["pourcentage_1er"] = pd.to_numeric(df_result["pourcentage_1er"])
    df_result["pourcentage_2eme"] = pd.to_numeric(df_result["pourcentage_2eme"])
    df_result["pourcentage_3eme"] = pd.to_numeric(df_result["pourcentage_3eme"])

    df_result["pourcentage_1er"] = df_result["pourcentage_1er"].round(1)
    df_result["pourcentage_2eme"] = df_result["pourcentage_2eme"].round(1)
    df_result["pourcentage_3eme"] = df_result["pourcentage_3eme"].round(1)

    df_result.rename(columns={"reco": "taux_reco"}, inplace=True)

    df_result["taux_reco"] = df_result["taux_reco"] / 61

    df_result["taux_reco"] = df_result["taux_reco"].round(1)

    df_result_final = pd.merge(
        df_result, df_brand[["Brand", "Product_C"]], on="Brand", how="left"
    )
    df_result_final["taux_reco_new"] = df_result_final["taux_reco"]
    df_result_final["evolution"] = (
        df_result_final["taux_reco_new"] - df_result_final["taux_reco"]
    )
    df_result_final["pourcentage_1er_new"] = df_result_final["pourcentage_1er"]
    df_result_final["pourcentage_2eme_new"] = df_result_final["pourcentage_2eme"]
    df_result_final["pourcentage_3eme_new"] = df_result_final["pourcentage_3eme"]
    df_result_final = df_result_final[
        [
            "Product_C",
            "Brand",
            "taux_reco",
            "taux_reco_new",
            "evolution",
            "pourcentage_1er",
            "pourcentage_2eme",
            "pourcentage_3eme",
            "pourcentage_1er_new",
            "pourcentage_2eme_new",
            "pourcentage_3eme_new",
        ]
    ]
    df_result_final.rename(columns={"Product_C": "marque"}, inplace=True)
    # df_result_final["marque"] = df_result_final["marque"].replace(
    #     {
    #         "BMS": "Brand 1",
    #         "GILEAD": "Brand 2",
    #         "NOVARTIS": "Brand 2",
    #     }
    # )

    logger.debug(start - time.time())
    print(df_result_final)
    return df_result_final.to_dict(orient="records")
