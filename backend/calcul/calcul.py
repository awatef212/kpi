import pandas as pd
import re

from loguru import logger

simulateur_reco = "Simulateur_KPI_Num_Reco"
simulateur_non_reco = "Simulateur_KPI_Num_Non_Reco"


def ajuster_valeur(row):
    min_val, max_val = row["min_max"].split("_")

    if row["Valeur"] < float(min_val):
        return float(min_val)
    elif row["Valeur"] > float(max_val):
        return float(max_val)
    else:
        return row["Valeur"]




def extract_question_condition(recode):
    if match := re.search(r'"([^"]+)"\s*(<=|>=|=|<|>)\s*(\d+)', recode):
        return match.group(1), match.group(0)
    return recode, None


def calculate_reco_intermediaire(row):
        return row["Valeur"] * row["coefficients"] if row["coefficients"] else 0




# def calculate_non_reco_intermediaire(row):
#     if row["Valeur"] == 0:
#         return 0
#     elif row["Condition"] is None:
#         # Si aucune condition, multipliez la Valeur par les coefficients
#         return (
#             row["Valeur"] * row["coefficients_non_reco"]
#             if row["coefficients_non_reco"]
#             else 0
#         )
#     else:
#         # Extraction de la question, de l'opérateur et du nombre de la condition
#         match = re.match(r'"([^"]+)"\s*(<=|>=|<|>|=)\s*(\d+\.?\d*)', row["Condition"])
#         if match:
#             question, operator, number = match.groups()
#             number = float(number)

#             # Comparaison de la Valeur avec la condition
#             if operator == "<=" and row["Valeur"] <= number:
#                 return row["coefficients_non_reco"]
#             elif operator == ">=" and row["Valeur"] >= number:
#                 return row["coefficients_non_reco"]
#             elif operator == "<" and row["Valeur"] < number:
#                 return row["coefficients_non_reco"]
#             elif operator == ">" and row["Valeur"] > number:
#                 return row["coefficients_non_reco"]
#             elif operator == "=" and row["Valeur"] == number:
#                 return row["coefficients_non_reco"]
#         return 0


def calculate_reco_intermediaire_2(df_original, incr):
    df = df_original.copy()
    df['reco_intermediaire'] = 0
    df['reco_intermediaire'] = df['reco_intermediaire'].astype(float)

    no_condition_df = df.copy()
    no_condition_df['Valeur'] = pd.to_numeric(no_condition_df['Valeur'], errors="coerce")
    no_condition_df['coefficients'] = pd.to_numeric(no_condition_df['coefficients'], errors="coerce")

    no_condition_df_value_zero = no_condition_df[no_condition_df['Valeur'] == 0].copy()
    no_condition_df_value = no_condition_df[no_condition_df['Valeur'] != 0].copy()
    if not no_condition_df_value.empty:
        no_condition_df_value.reset_index(drop=True, inplace=True)
        if incr:
            no_condition_df_value['Valeur'] = no_condition_df_value.apply(ajuster_valeur, axis=1 )
        no_condition_df_value['reco_intermediaire'] = no_condition_df_value['Valeur'] * no_condition_df_value['coefficients']

    return pd.concat(
        [no_condition_df_value_zero, no_condition_df_value],
        axis=0,
    )


