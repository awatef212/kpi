import pandas as pd

from . import MYSQL_DB_HOST, MYSQL_DB_NAME, MYSQL_DB_PASSWORD, MYSQL_DB_USER, PROCESS
from sqlalchemy import create_engine

simulateur_reco = "Simulateur_KPI_Num_Reco"
simulateur_non_reco = "Simulateur_KPI_Num_Non_Reco"


def get_simulateur_from_DB(engine, table_name):
    query = f"SELECT * FROM {table_name};"
    return pd.read_sql_query(query, engine)

def get_prod_from_DB(engine):
    query = "SELECT CodeAA, Brand, Q21_2, Q21_3, Q22_4, Q23_2, Q23_7, Q24_2, Q24_3, Q25_2 FROM AllProd;"
    return pd.read_sql_query(query, engine)

def get_delta(engine):
    query = "SELECT CodeAA, Brand, delta from AllProd;"
    return pd.read_sql_query(query, engine)

def get_brand(engine):
    query = "SELECT distinct Brand, Product_C from AllProd;"
    return pd.read_sql_query(query, engine)


def get_df_merged(engine):
    query = "SELECT * FROM df_merged;"
    return pd.read_sql_query(query, engine)


def get_data(bool):
    url = f"mysql+mysqlconnector://{MYSQL_DB_USER}:{MYSQL_DB_PASSWORD}@{MYSQL_DB_HOST}/{MYSQL_DB_NAME}"
    engine = create_engine(url)

    try:
        df_simulateur_reco = get_simulateur_from_DB(
            engine=engine, table_name=simulateur_reco
        )

        df_prod = get_prod_from_DB(engine)
        df_brand = get_brand(engine)
        df_delta = get_delta(engine)
        if bool:
            df_merged = get_df_merged(engine)
            return df_simulateur_reco, df_prod, df_brand, df_merged, df_delta
        else:
            return df_simulateur_reco, df_prod, df_brand, df_delta
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")
    finally:
        pass


def get_question():
    return pd.DataFrame(
        {
            "Question": [
                "Q21.2",
                "Q23.2",
                "Q23.7",
                "Q21.3",
                "Q24.3",
                "Q25.2",
                "Q22.4",
                "Q24.2",
            ],
            "Noms": [
                "PFS",
                "Disponibilités de créneaux d’aphérèse et de production",
                "Modalité d’administration",
                "Durée de la réponse complète",
                "Développement d’un portefeuille de produits innovants/intéressants",
                "Partenariat avec des associations de patients",
                "Neurotoxicité",
                "Expert dans la prise en charge des DLBCL",
            ],
        }
    ).to_dict(orient="records")
