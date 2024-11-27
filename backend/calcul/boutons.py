import numpy as np
import pandas as pd
import time

from .calcul import calculate_reco_intermediaire, ajuster_valeur
from .data import get_data

from loguru import logger


def get_All_taux_bouton(questions, marques, start, stop, step, type=None):

    start2 = time.time()
    (
        df_simulateur_reco,
        df_prod,
        df_brand,
        df_merged,
        df_delta,
    ) = get_data(True)

    increments = np.round(np.linspace(start, stop, int((stop - start) / step) + 1), 1)

    final_results = []

    if type == "I":
        if questions == ["all"]:
            questions = [
                "Q22.6",
                "Q22.7",
                "Q22.8",
                "Q22.2",
                "Q18.1",
                "Q15",
                "Q18.2",
                "Q22.5",
            ]

        for incr in increments:
            for question in questions:
                final_results.append(
                    get_taux_bouton(
                        df_simulateur_reco,
                        df_prod,
                        df_brand,
                        df_merged,
                        df_delta,
                        incr,
                        question,
                        marques,
                    )
                )
    else:
        if marques == ["all"]:
            marques = [1, 2, 3, 4, 5, 6, 7, 8]
        for marque in marques:
            for incr in increments:
                final_results.append(
                    get_taux_bouton(
                        df_simulateur_reco,
                        df_prod,
                        df_brand,
                        df_merged,
                        df_delta,
                        incr,
                        questions,
                        marque,
                    )
                )

    logger.info(time.time() - start2)
    return final_results


def get_taux_bouton(
    df_simulateur_reco,
    df_prod,
    df_brand,
    df_merged,
    df_delta,
    incrementation,
    question,
    marque,
):
    start = time.time()
    df_merged = df_merged[df_merged["Brand"] == marque].copy()

    df_merged2 = df_merged.copy()

    mask = (df_merged2["Question"] == question)

    df_merged2.loc[mask, "Valeur"] += incrementation

    temp_df = df_merged2[mask].copy()

    temp_df["Valeur"] = temp_df.apply(ajuster_valeur, axis=1)
    temp_df["reco_intermediaire"] = temp_df.apply(calculate_reco_intermediaire, axis=1)

    temp_df["reco_intermediaire"] = pd.to_numeric(temp_df["reco_intermediaire"], errors="coerce" )

    df_merged2.loc[mask, "reco_intermediaire"] = temp_df["reco_intermediaire"]

    df_grouped = (
        df_merged.groupby(["CodeAA", "Brand"])
        .agg({"reco_intermediaire": "sum"})
        .reset_index()
    )

    df_grouped.rename(
        columns={"reco_intermediaire": "reco", "non_reco_intermediaire": "non_reco"},
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

    df_grouped["delta"] = pd.to_numeric(df_grouped["delta"], errors="coerce")
    df_grouped2["delta"] = pd.to_numeric(df_grouped2["delta"], errors="coerce")

    constante_reco = df_simulateur_reco[df_simulateur_reco["Question"] == "_"][
        "coefficients"
    ].iloc[0]

    df_grouped["reco"] = df_grouped["reco"] + float(constante_reco)
    df_grouped2["reco"] = df_grouped2["reco"] + float(constante_reco)

    df_grouped['reco'] += df_grouped['delta']
    df_grouped2['reco'] += df_grouped2['delta']

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

    df_result2.rename(columns={"reco": "taux_reco_new"}, inplace=True)

    df_result["taux_reco"] = df_result["taux_reco"] / 61
    df_result2["taux_reco_new"] = df_result2["taux_reco_new"] / 61

    df_result_final = pd.merge(
        df_result, df_brand[["Brand", "Product_C"]], on="Brand", how="left"
    )
    df_result_final = pd.merge(
        df_result_final[["Product_C", "Brand", "taux_reco"]],
        df_result2[["taux_reco_new", "Brand"]],
        on="Brand",
        how="left",
    )

    df_result_final["evolution"] = (
        df_result_final["taux_reco_new"] - df_result_final["taux_reco"]
    )
    df_result_final["evolution"] = df_result_final["evolution"].round(1)
    df_result_final["taux_reco_new"] = df_result_final["taux_reco_new"].round(1)
    df_result_final["taux_reco"] = df_result_final["taux_reco"].round(1)


    df_result_final = df_result_final[
        ["Product_C", "Brand", "taux_reco", "taux_reco_new", "evolution"]
    ]
    df_result_final.rename(columns={"Product_C": "marque"}, inplace=True)
    df_result_final["incrementation"] = incrementation
    df_result_final["question"] = question
    logger.debug(start - time.time())

    return df_result_final.to_dict(orient="records")
