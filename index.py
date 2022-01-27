from sqlite3.dbapi2 import Error
from flask import Flask, flash, redirect, url_for, abort
from flask import render_template
from flask import g
from flask import jsonify
from flask.ctx import AppContext
from .database import Database
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
from .schemas import glissade_update_schema
from flask import request
import json
import logging
import csv
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
import xml.etree.ElementTree as ET
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tweepy


app = Flask(__name__, static_url_path="", static_folder="static")
schema = JsonSchema(app)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        g._database = Database()
    return g._database


def runSchedule():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(get_db().intialiaze_all, "cron", hour="00", minute="00")
    sched.start()


with app.app_context():
    runSchedule()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.disconnect()


def readYamlFile():
    with open("courriel.yaml", "r") as f:
        try:
            yamlobjet = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            abort(503, description=e)
    return yamlobjet


# fonction qui traite les nouvelles installations
# et les transforme en string
# si le string final est vide c'est qu'il n'y a pas de
# de nouvelles installaltions
def getTextForPost(
    liste_nouvelles_installations,
    liste_nouvelles_glissades,
    liste_nouvelles_patinoires,
):
    text_retour = ""
    if (
        len(liste_nouvelles_installations) != 0
        or len(liste_nouvelles_glissades) != 0
        or len(liste_nouvelles_patinoires) != 0
    ):
        for row in liste_nouvelles_installations:
            text_retour += (
                "Nom : "
                + row["Nom"]
                + " Type : "
                + row["Type"]
                + " Arrondissement : "
                + row["Arrondissement"]
                + " Adresse : "
                + row["Adresse"]
                + "\n"
            )

        for row in liste_nouvelles_glissades:
            text_retour += (
                "Nom : "
                + row["Nom"]
                + " Arrondissement : "
                + row["Arrondissement"]
                + " Date mise à jour : "
                + row["Date mise à jour"]
                + "\n"
            )

        for row in liste_nouvelles_patinoires:
            text_retour += (
                "Nom : "
                + row["Nom"]
                + " Arrondissement : "
                + row["Arrondissement"]
                + "\n"
            )

    return text_retour


def sendTweet(data):

    if data != "":
        yamlobjet = readYamlFile()

        twitter_keys = {
            "consumer_key": yamlobjet["Twitter"]["consumer_key"],
            "consumer_secret": yamlobjet["Twitter"]["consumer_secret"],
            "access_token": yamlobjet["Twitter"]["access_token"],
            "access_token_secret": yamlobjet["Twitter"]["access_token_secret"],
        }

        auth = tweepy.OAuthHandler(
            twitter_keys["consumer_key"], twitter_keys["consumer_secret"]
        )

        auth.set_access_token(
            twitter_keys["access_token"], twitter_keys["access_token_secret"]
        )

        api = tweepy.API(auth)
        for row in data.splitlines():
            api.update_status(status=row)


def sendNouvellesInstallationsEmail(data):
    yamlobjet = readYamlFile()

    if data != "":
        body = yamlobjet["Destinataire"]["body"]

        msg = MIMEMultipart()
        msg["Subject"] = yamlobjet["Destinataire"]["subject"]
        msg["From"] = yamlobjet["Destinataire"]["source_address"]
        msg["destination_address"] = yamlobjet["Destinataire"][
            "destination_address"
        ]
        source_adress = yamlobjet["Destinataire"]["source_address"]

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(
            source_adress, yamlobjet["Destinataire"]["source_adress_mdp"]
        )

        body += data
        msg.attach(MIMEText(body, "plain"))
        text = msg.as_string()

        server.sendmail(
            source_adress,
            yamlobjet["Destinataire"]["destination_address"],
            text,
        )
        server.quit()


@app.route("/")
def index():
    try:
        # importation des donnes au depart
        aquatiques_installations = (
            get_db().isPiscineInstallationsAquatiquesAlreadyDefined()
        )
        glissades_installations = get_db().isGlissadesAlreadyDefined()
        patinoires_installations = get_db().isPatinoiresAlreadyDefined()
        liste_nouvelles_installations = get_db().liste_nouvelles_instalaltions
        liste_nouvelles_glissades = get_db().liste_nouvelles_glissades
        liste_nouvelles_patinoires = get_db().liste_nouvelles_patinoires
        # test pour essayer la fonctionnalité de tweet et d'email
        # get_db().testAddNewInstallations()
        data = getTextForPost(
            liste_nouvelles_installations,
            liste_nouvelles_glissades,
            liste_nouvelles_patinoires,
        )
        sendNouvellesInstallationsEmail(data)
        sendTweet(data)
        return redirect(
            url_for(
                "doc",
            )
        )
    except Error as e:
        abort(
            503,
            description=e,
        )


@app.route("/doc")
def doc():
    return render_template("doc.html")


@app.route("/api/installations/arrondissement/<nom_arr>", methods=["GET"])
def get_installations_par_arrondissement(nom_arr):
    retour = get_db().getAllInstallationsForArrondissement(nom_arr=nom_arr)
    if retour is None:
        return "", 404
    else:
        return jsonify(retour)


@app.route("/api/installations/glissades/<id>", methods=["GET"])
def getGlissade(id):
    retour = get_db().getGlissadeConditionById(id=id)
    if retour is None:
        return "", 404
    else:
        return jsonify(retour.asDictionary())


@app.errorhandler(JsonValidationError)
def validation_error(e):
    errors = [validation_error.message for validation_error in e.errors]
    return jsonify({"error": e.message, "errors": errors}), 400


@app.route("/api/installations/glissades/<id>", methods=["PUT"])
@schema.validate(glissade_update_schema)
def modifyGlissade(id):
    glissade = get_db().getGlissadeConditionById(id=id)
    if glissade is None:
        return "", 404
    else:
        data = request.get_json()
        glissade.nom = data["nom"]
        glissade.ouvert = data["ouvert"]
        glissade.deblaye = data["deblaye"]
        glissade.condition = data["condition"]
        get_db().saveGlissade(glissade)
        return jsonify(glissade.asDictionary())


@app.route("/api/installations/glissades/<id>", methods=["DELETE"])
def delete_person(id):
    glissade = get_db().getGlissadeConditionById(id)
    if glissade is None:
        return "", 404
    else:
        get_db().delete_glissade(glissade)
        return "", 200


@app.route("/api/installations/recentes", methods=["GET"])
def get_installations_recentes():
    retour = get_db().getInstallationsByDate("2021")
    if retour is None:
        return "", 404
    else:
        return jsonify(Installations=[e.asDictionary() for e in retour])


@app.route("/api/installations/recentes/xml", methods=["GET"])
def get_installations_recentes_xml():
    retour = get_db().getInstallationsByDate("2021")
    retour = toXMl(retour)
    if retour is None:
        return "", 404
    else:
        return app.response_class(retour, mimetype="application/xml")


@app.route("/api/installations/recentes/csv", methods=["GET"])
def get_installations_recentes_csv():
    retour = get_db().getInstallationsByDateForCSV("2021")
    retour = toCSV(retour)
    if (
        retour == "ID,Nom,Arrondissement,Date_de_mise_a_jour,"
        "Ouvert,Deblaye,Arrose,Resurface\n"
    ):
        return "", 404
    else:
        return app.response_class(retour, mimetype="application/csv")


def toXMl(liste):
    installations = ET.Element("Installations")

    for row in liste:
        installation = ET.SubElement(installations, "Installation")
        ET.SubElement(installation, "ID").text = str(row.id)
        ET.SubElement(installation, "Nom").text = row.nom
        ET.SubElement(installation, "Arrondissement").text = row.nom_arr
        conditions = ET.SubElement(installation, "Conditions")
        i = 0
        while i < len(row.conditions):
            condition = ET.SubElement(conditions, "condition")
            ET.SubElement(condition, "Date_de_mise_a_jour").text = str(
                row.conditions[i]
            )
            ET.SubElement(condition, "Ouvert").text = str(
                row.conditions[i + 1]
            )
            ET.SubElement(condition, "Deblaye").text = str(
                row.conditions[i + 2]
            )
            ET.SubElement(condition, "Arrose").text = str(
                row.conditions[i + 3]
            )
            ET.SubElement(condition, "Resurface").text = str(
                row.conditions[i + 4]
            )
            i += 5

    return ET.tostring(installations, encoding="UTF-8")


def toCSV(liste):
    retour = "ID,Nom,Arrondissement,Date_de_mise_a_jour"
    retour += ",Ouvert,Deblaye,Arrose,Resurface\n"

    for row in liste:
        retour += (
            str(row[0])
            + ","
            + str(row[1].replace(",", ""))
            + ","
            + str(row[2])
            + ","
            + str(row[3])
            + ","
            + str(row[4])
            + ","
            + str(row[5])
            + ","
            + str(row[6])
            + ","
            + str(row[7])
            + "\n"
        )
    return retour
