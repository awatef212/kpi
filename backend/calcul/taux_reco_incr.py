import numpy as np
import pandas as pd
import time

from loguru import logger

from .data import get_data
from .calcul import calculate_reco_intermediaire, ajuster_valeur


def get_taux_reco_incr(incrementation, questions, marques):
    # sourcery skip: extract-duplicate-method
    start = time.time()
    df_simulateur_reco, df_prod, df_brand, df_merged, df_delta = get_data(True)

    df_merged2 = df_merged.copy()
    for question, marque, incr in zip(questions, marques, incrementation):
        mask = (df_merged2["Question"] == question) & (df_merged2["Brand"] == marque)

        df_merged2.loc[mask, "Valeur"] += incr

        temp_df = df_merged2[mask].copy()

        temp_df["Valeur"] = temp_df.apply(ajuster_valeur, axis=1)
        temp_df["reco_intermediaire"] = temp_df.apply(
            calculate_reco_intermediaire, axis=1
        )

        temp_df["reco_intermediaire"] = pd.to_numeric(
            temp_df["reco_intermediaire"], errors="coerce"
        )

        df_merged2.loc[mask, "reco_intermediaire"] = temp_df["reco_intermediaire"]

    df_grouped = (
        df_merged.groupby(["CodeAA", "Brand"])
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

    df_grouped2 = (
        df_merged2.groupby(["CodeAA", "Brand"])
        .agg({"reco_intermediaire": "sum"})
        .reset_index()
    )
    df_grouped2.rename(
        columns={"reco_intermediaire": "reco"},
        inplace=True,
    )
    df_grouped2 = pd.merge(
        df_grouped2,
        df_delta[["Brand", "CodeAA", "delta"]],
        on=["Brand", "CodeAA"],
        how="left",
    )

    constante_reco = df_simulateur_reco[df_simulateur_reco["Question"] == "_"][
        "coefficients"
    ].iloc[0]
    df_grouped["delta"] = pd.to_numeric(df_grouped["delta"], errors="coerce")
    df_grouped2["delta"] = pd.to_numeric(df_grouped2["delta"], errors="coerce")

    df_grouped["reco"] = df_grouped["reco"] + float(constante_reco)
    df_grouped2["reco"] = df_grouped2["reco"] + float(constante_reco)

    df_grouped["reco"] += df_grouped["delta"]
    df_grouped2["reco"] += df_grouped2["delta"]
    df_grouped2["ranking"] = df_grouped2.groupby("CodeAA")["reco"].rank(
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

    df_result.rename(columns={"reco": "taux_reco"}, inplace=True)

    df_result2 = (
        df_grouped2.groupby(["Brand"])
        .agg(
            {
                "reco": "sum",
            }
        )
        .reset_index()
    )
    total_ranks_per_brand = df_grouped2.groupby("Brand")["ranking"].count()

    ranking_counts_per_brand = df_grouped2.groupby(["Brand", "ranking"]).size()

    percentage_per_rank_and_brand = (
        ranking_counts_per_brand / total_ranks_per_brand
    ) * 100

    percentage_per_rank_pivot = percentage_per_rank_and_brand.unstack().fillna(0)

    percentage_per_rank_pivot = percentage_per_rank_pivot[[1, 2, 3]]

    percentage_per_rank_pivot.columns = [
        "pourcentage_1er_new",
        "pourcentage_2eme_new",
        "pourcentage_3eme_new",
    ]

    df_result2 = df_result2.merge(percentage_per_rank_pivot, on="Brand", how="left")

    df_result2["pourcentage_1er_new"] = pd.to_numeric(df_result2["pourcentage_1er_new"])
    df_result2["pourcentage_2eme_new"] = pd.to_numeric(
        df_result2["pourcentage_2eme_new"]
    )
    df_result2["pourcentage_3eme_new"] = pd.to_numeric(
        df_result2["pourcentage_3eme_new"]
    )

    df_result2["pourcentage_1er_new"] = df_result2["pourcentage_1er_new"].round(1)
    df_result2["pourcentage_2eme_new"] = df_result2["pourcentage_2eme_new"].round(1)
    df_result2["pourcentage_3eme_new"] = df_result2["pourcentage_3eme_new"].round(1)

    df_result2.rename(columns={"reco": "taux_reco_new"}, inplace=True)

    df_result["taux_reco"] = df_result["taux_reco"] / 61
    df_result2["taux_reco_new"] = df_result2["taux_reco_new"] / 61
    df_result["taux_reco"] = df_result["taux_reco"].round(1)
    df_result2["taux_reco_new"] = df_result2["taux_reco_new"].round(1)

    df_result_final = pd.merge(
        df_result, df_brand[["Brand", "Product_C"]], on="Brand", how="left"
    )
    df_result_final = pd.merge(
        df_result_final[["Product_C", "Brand", "taux_reco"]],
        df_result2[
            [
                "taux_reco_new",
                "Brand",
                "pourcentage_1er_new",
                "pourcentage_2eme_new",
                "pourcentage_3eme_new",
            ]
        ],
        on="Brand",
        how="left",
    )

    df_result_final["evolution"] = (
        df_result_final["taux_reco_new"] - df_result_final["taux_reco"]
    )
    df_result_final["evolution"] = df_result_final["evolution"].round(1)
    df_result_final = df_result_final[
        [
            "Product_C",
            "Brand",
            "taux_reco",
            "taux_reco_new",
            "evolution",
            "pourcentage_1er_new",
            "pourcentage_2eme_new",
            "pourcentage_3eme_new",
        ]
    ]
    df_result_final.rename(columns={"Product_C": "marque"}, inplace=True)
    logger.debug(start - time.time())
    return df_result_final.to_dict(orient="records")
