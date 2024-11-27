import json

from flask import Flask, jsonify
from flask_cors import CORS

from calcul.boutons import get_All_taux_bouton
from calcul.data import get_question
from calcul.taux_reco import get_taux_reco
from calcul.taux_reco_incr import get_taux_reco_incr
from calcul.taux_reco_incr_lies import get_taux_reco_incr_lies
from database.insertion import insertion

from loguru import logger

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    # insertion()
    return "Welcome to the KPI simulator!"


@app.route("/taux")
def taux_reco():
    try:
        response = get_taux_reco()
        return jsonify(response)
    except Exception as e:
        app.logger.error("Erreur dans taux_reco : %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/taux/<incrementations>/<questions>/<marques>")
def taux_reco_incrementations(incrementations, questions, marques):
    questions_list = questions.split(",")
    marques_list = marques.split(",")
    incrementations_list = incrementations.split(",")
    incrementation2 = [float(incr) for incr in incrementations_list]
    marques2 = [int(marque) for marque in marques_list]
    df_result = get_taux_reco_incr(incrementation2, questions_list, marques2)
    resultats = [
        {
            "resultat": json.loads(json.dumps(df_result)),
        }
    ]
    print('route("/taux/<incrementations>/<questions>/<marques>")')
    return jsonify(resultats)


@app.route("/get_data")
def get_data():
    return jsonify(get_question())


@app.route("/taux_bouton_I/<questions>/<marque>/<start>/<stop>/<step>")
def get_bouton_I(questions, marque, start, stop, step):

    questions_list = questions.split(",")
    questions_l = [str(q) for q in questions_list]
    marque = int(marque)
    try:

        response = get_All_taux_bouton(
            questions_l, marque, float(start), float(stop), float(step), "I"
        )
        return jsonify(response)
    except Exception as e:
        app.logger.error("Erreur dans taux_reco : %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/taux_bouton_I_liee/<questions>/<marque>/<start>/<stop>/<step>")
def get_bouton_I_liee(questions, marque, start, stop, step):

    questions_list = questions.split(",")
    questions_l = [str(q) for q in questions_list]
    marque = int(marque)
    logger.debug(questions)
    logger.debug(type(questions))

    response = get_taux_reco_incr_lies(
        questions_l, marque, float(start), float(stop), float(step)
    )
    return jsonify(response)

@app.route("/taux_bouton_S/<question>/<marques>")
def get_bouton_S(question, marques):
    if "all" in marques:
        marques_list_int = [1, 2, 3, 4, 5, 6, 7, 8]
    else:
        marque_list = marques.split(",")
        marques_list_int = [int(marque) for marque in marque_list]
    response = get_All_taux_bouton(question, marques_list_int)
    return jsonify(response)
    # except Exception as e:
    #         app.logger.error("Erreur dans taux_reco : %s", str(e))
    #

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
