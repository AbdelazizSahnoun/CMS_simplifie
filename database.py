from os import name
import sqlite3
import csv
import io
from sqlite3.dbapi2 import Date
import urllib
import xml.etree.ElementTree as ET
from datetime import *
from .patinoires import Patinoire

from .glissade import Glissade

from .installations import Installations


class Database:
    liste_nouvelles_instalaltions = []
    liste_nouvelles_patinoires = []
    liste_nouvelles_glissades = []
    last_insert_condition_date = datetime.min

    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db/database.db")

        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    # L'idee derriere les insert qui suvient
    # est que lors de la premiere importation des donnes,
    # on ne check pas s'il y a des nouvelles installations,
    # ce n'est qu'aux importations quotidienne
    # qu'on va regarder s'il existe des nouvelles installations
    # c'est la raison d'avoir le boolean firstime
    # les nouvelles installations sont determinés par le nom

    def insert_in_Piscine_Installation_Aquatique(
        self,
        piscineID,
        Type,
        Nom,
        Arrondissement,
        Adresse,
        Propriete,
        Gestion,
        Point_X,
        Point_Y,
        Equipement,
        Longitude,
        Latitude,
        firstime,
    ):

        existe = False
        cursor = self.get_connection().cursor()
        if firstime is not True:
            cursor.execute(
                "SELECT nom from Piscine_Installation_Aquatique"
                " WHERE nom= ?",
                (Nom,),
            )
            result = cursor.fetchone()
            if result is not None:
                existe = True
        if existe is False:
            cursor.execute(
                "insert into Piscine_Installation_Aquatique"
                "(piscine_id,type,nom,arrondissement"
                ",adresse,propriete"
                ",gestion,point_X,point_Y,equipement,"
                "longitude,latitude)"
                " values(?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    piscineID,
                    Type,
                    Nom,
                    Arrondissement,
                    Adresse,
                    Propriete,
                    Gestion,
                    Point_X,
                    Point_Y,
                    Equipement,
                    Longitude,
                    Latitude,
                ),
            )

        self.get_connection().commit()
        if existe is False and firstime is not True:

            self.liste_nouvelles_instalaltions.append(
                {
                    "Nom": Nom,
                    "Type": Type,
                    "Arrondissement": Arrondissement,
                    "Adresse": Adresse,
                }
            )

    def insert_in_glissades(
        self,
        nom,
        nom_arr,
        cle,
        date_mise_a_jour,
        ouvert,
        deblaye,
        condition,
        firstime,
    ):

        existe = False
        cursor = self.get_connection().cursor()
        if firstime is not True:
            cursor.execute("SELECT nom from Glissades" " WHERE nom= ?", (nom,))
            result = cursor.fetchone()
            if result is not None:
                existe = True
        if existe is False:
            cursor.execute(
                "insert into Glissades(nom,ouvert,deblaye,condition)"
                " values(?,?,?,?)",
                (nom, ouvert, deblaye, condition),
            )

            cursor.execute(
                "SELECT rowid from Glissades order by ROWID DESC limit 1"
            )
            result = cursor.fetchone()
            id = result[0]

            cursor.execute(
                "insert into Arrondissement(glissade_id,nom_arrondissement,"
                "cle,date_mise_a_jour)"
                "values(?,?,?,?)",
                (id, nom_arr, cle, date_mise_a_jour),
            )
        self.get_connection().commit()
        if existe is False and firstime is not True:
            cursor.execute(
                "SELECT nom,nom_arrondissement,date_mise_a_jour"
                " from Glissades INNER JOIN Arrondissement"
                " ON Glissades.glissade_id=Arrondissement.glissade_id"
                " WHERE nom=?",
                (nom,),
            )
            result = cursor.fetchall()
            if len(result) != 0:
                self.liste_nouvelles_glissades.append(
                    {
                        "Nom": result[0][0],
                        "Arrondissement": result[0][1],
                        "Date mise à jour": result[0][2],
                    }
                )

    def insert_in_arrondissement_patinoires(self, nom_arr, firstime):
        existe = False
        cursor = self.get_connection().cursor()
        if firstime is not True:
            cursor.execute(
                "SELECT nom_arrondissement from Arrondissement_Patinoires"
                " where nom_arrondissement=?",
                (nom_arr,),
            )
            result = cursor.fetchone()
            if result is not None:
                existe = True

        if existe is False:
            cursor.execute(
                "insert into Arrondissement_Patinoires"
                "(nom_arrondissement) values(?)",
                (nom_arr,),
            )
            self.get_connection().commit()

    def insert_in_patinoires(self, nom_arr, nom, firstime):

        existe = False
        cursor = self.get_connection().cursor()
        if firstime is not True:
            cursor.execute(
                "SELECT nom_patinoire from Patinoires where nom_patinoire=?",
                (nom,),
            )
            result = cursor.fetchone()
            if result is not None:
                existe = True
        if existe is False:
            cursor.execute(
                "SELECT id_arrondissement from Arrondissement_Patinoires"
                " where nom_arrondissement=?",
                (nom_arr,),
            )
            result = cursor.fetchone()
            index_arr = result[0]
            cursor.execute(
                "insert into Patinoires"
                "(id_arrondissement,nom_patinoire) values(?,?)",
                (index_arr, nom),
            )
            self.get_connection().commit()

        if existe is False and firstime is not True:
            cursor.execute(
                "SELECT nom_patinoire,nom_arrondissement from Patinoires"
                " INNER JOIN Arrondissement_Patinoires ON "
                "Patinoires.id_arrondissement"
                " =Arrondissement_Patinoires.id_arrondissement"
                " WHERE nom_patinoire=?",
                (nom,),
            )
            result = cursor.fetchall()

            if len(result) != 0:
                self.liste_nouvelles_patinoires.append(
                    {
                        "Nom": result[0][0],
                        "Arrondissement": result[0][1],
                    }
                )

    def get_last_date(self, firstime):
        if firstime is not True:
            cursor = self.get_connection().cursor()
            cursor.execute(
                "SELECT date_heure FROM"
                " Condition ORDER BY id_condition DESC LIMIT 1",
                (),
            )
            result = cursor.fetchone()
            if result is not None:
                self.last_insert_condition_date = datetime.strptime(
                    result[0], "%Y-%m-%d %H:%M:%S"
                )

    def insert_in_conditions(
        self,
        nom_patinoire,
        date_heure,
        ouvert,
        deblaye,
        arrose,
        resurface,
        firstime,
    ):
        existe = False
        cursor = self.get_connection().cursor()

        if firstime is not True:
            # pour reduire le nombre de requetes sql
            try:
                current_date = datetime.strptime(
                    date_heure, "%Y-%m-%d %H:%M:%S"
                )
                if current_date <= self.last_insert_condition_date:
                    existe = True
            except ValueError:
                cursor.execute(
                    "SELECT date_heure from Condition where date_heure=?",
                    (date_heure,),
                )
                result = cursor.fetchone()
                if result is not None:
                    existe = True

        if existe is False:
            cursor.execute(
                "SELECT id_patinoire from Patinoires where nom_patinoire=?",
                (nom_patinoire,),
            )
            result = cursor.fetchone()
            index_pat = result[0]
            cursor.execute(
                "insert into Condition"
                "(id_patinoire,date_heure,ouvert,deblaye,arrose,resurface)"
                " values"
                "(?,?,?,?,?,?)",
                (
                    index_pat,
                    date_heure,
                    ouvert,
                    deblaye,
                    arrose,
                    resurface,
                ),
            )

    def initialize_installations_aquatiques(self, firstime):
        url_installations_aquatiques = "https://data.montreal.ca/dataset/4604afb7-a7c4-4626-a3ca-e136158133f2/resource/cbdca706-569e-4b4a-805d-9af73af03b14/download/piscines.csv"

        csv_file = urllib.request.urlopen(url_installations_aquatiques)
        data_installations_aquatiques = csv.reader(io.TextIOWrapper(csv_file))
        next(data_installations_aquatiques, None)
        for rows in data_installations_aquatiques:
            self.insert_in_Piscine_Installation_Aquatique(
                rows[0],
                rows[1],
                rows[2],
                rows[3],
                rows[4],
                rows[5],
                rows[6],
                rows[7],
                rows[8],
                rows[9],
                rows[10],
                rows[11],
                firstime,
            )

    # ces fonctions servent à ne pas importer à chaque
    # relancement du programme si la base de donnée existe déja

    def isPiscineInstallationsAquatiquesAlreadyDefined(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM Piscine_Installation_Aquatique")
        nb_rows = cursor.fetchone()
        if nb_rows[0] == 0:
            self.initialize_installations_aquatiques(True)

    def isGlissadesAlreadyDefined(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM Glissades")
        nb_rows = cursor.fetchone()
        if nb_rows[0] == 0:
            self.initialize_glissades(True)

    def isPatinoiresAlreadyDefined(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM Arrondissement_Patinoires")
        nb_rows = cursor.fetchone()
        if nb_rows[0] == 0:
            self.initialize_Patinoires(True)

    def initialize_glissades(self, firstime):
        url_xml_glissades = "http://www2.ville.montreal.qc.ca/services_citoyens/pdf_transfert/L29_GLISSADE.xml"

        xml_file = urllib.request.urlopen(url_xml_glissades)
        file = ET.parse(xml_file)
        root = file.getroot()
        data_glissades = []
        nom = ""
        nom_arr = ""
        cle = ""
        date_maj = ""
        ouvert = 0
        deblaye = 0
        condition = ""

        for elem in root.iter():
            if elem.tag == "nom":
                nom = elem.text
            if elem.tag == "nom_arr":
                nom_arr = elem.text
            if elem.tag == "cle":
                cle = elem.text
            if elem.tag == "date_maj":
                date_maj = elem.text
            if elem.tag == "ouvert":
                ouvert = elem.text
            if elem.tag == "deblaye":
                deblaye = elem.text
            if elem.tag == "condition":
                condition = elem.text
                data_glissades.append(
                    [nom, nom_arr, cle, date_maj, ouvert, deblaye, condition]
                )

        for row in data_glissades:
            self.insert_in_glissades(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                firstime,
            )

    def initialize_Patinoires(self, firstime):
        url_xml_patinoires = "https://data.montreal.ca/dataset/225ac315-49fe-476f-95bd-a1ce1648a98c/resource/5d1859cc-2060-4def-903f-db24408bacd0/download/l29-patinoire.xml"
        xml_file = urllib.request.urlopen(url_xml_patinoires)
        file = ET.parse(xml_file)
        root = file.getroot()

        nom_arr = ""
        nom_patinoire = ""
        date_heure = ""
        ouvert = ""
        deblaye = ""
        arrose = ""
        resurface = ""
        data_arrondissements = []
        data_patinoire = []
        data_conditions = []

        for elem in root.iter():
            if elem.tag == "nom_arr":
                nom_arr = elem.text.strip()
                data_arrondissements.append(nom_arr)
            if elem.tag == "nom_pat":
                nom_patinoire = elem.text.strip()
                data_patinoire.append([nom_arr, nom_patinoire])
            if elem.tag == "date_heure":
                date_heure = elem.text.strip()
            if elem.tag == "ouvert":
                ouvert = elem.text.strip()
            if elem.tag == "deblaye":
                deblaye = elem.text.strip()
            if elem.tag == "arrose":
                arrose = elem.text.strip()
            if elem.tag == "resurface":
                resurface = elem.text.strip()
                data_conditions.append(
                    [
                        nom_patinoire,
                        date_heure,
                        ouvert,
                        deblaye,
                        arrose,
                        resurface,
                    ]
                )

        for row in data_arrondissements:
            self.insert_in_arrondissement_patinoires(row, firstime)

        for row in data_patinoire:
            self.insert_in_patinoires(row[0], row[1], firstime)

        self.get_last_date(firstime)
        for row in data_conditions:
            self.insert_in_conditions(
                row[0], row[1], row[2], row[3], row[4], row[5], firstime
            )
        # les insert dans conditions peuvent causer
        # de la corruption, je les commit une seule
        # fois pour cette raison
        self.get_connection().commit()

    def intialiaze_all(self):
        print("Debut de l'importation des données quotidienne", flush=True)
        self.initialize_installations_aquatiques(False)
        self.initialize_glissades(False)
        self.initialize_Patinoires(False)
        print("Fin de l'importation des données quotidienne", flush=True)

    # j'ai remarque les donnes sur les patinoires contenait aussi les donnes
    # sur les glissades, afin de pas creer de duplicats et sachant
    # que les informations provenant des patinoires etaient plus completes
    # j'ai decidé de pas importer les glissades pour cette fonctionnalite
    def getAllInstallationsForArrondissement(self, nom_arr):
        list_installations = []
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT piscine_id,nom,type from"
            " Piscine_Installation_Aquatique where Arrondissement=?",
            (nom_arr,),
        )
        for row in cursor:
            list_installations.append(
                Installations(row[0], row[1], row[2]).asDictionary()
            )

        cursor.execute(
            "Select id_patinoire,nom_patinoire from Patinoires"
            " INNER JOIN Arrondissement_Patinoires on"
            " Arrondissement_Patinoires.id_arrondissement=="
            " Patinoires.id_arrondissement WHERE nom_arrondissement=?",
            (nom_arr,),
        )

        for row in cursor:
            donnes = row[1].split(",")
            list_installations.append(
                Installations(
                    row[0], donnes[1].strip(), donnes[0].strip()
                ).asDictionary()
            )

        if len(list_installations) == 0:
            return None
        else:
            return list_installations

    def getGlissadeConditionById(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT glissade_id,nom,ouvert,deblaye,condition"
            " FROM Glissades where glissade_id=?",
            (id,),
        )
        results = cursor.fetchall()

        if len(results) == 0:
            return None
        else:
            return Glissade(
                results[0][0],
                results[0][1],
                results[0][2],
                results[0][3],
                results[0][4],
            )

    def saveGlissade(self, glissade):
        connection = self.get_connection()
        if glissade.id is None:
            connection.execute(
                "insert into Glissades(nom,ouvert,deblaye,condition)"
                " values(?,?,?,?)",
                (
                    glissade.nom,
                    glissade.ouvert,
                    glissade.deblaye,
                    glissade.conditon,
                ),
            )
            connection.execute()
            cursor = connection.cursor()
            cursor.execute("select last_insert_rowid()")
            result = cursor.fetchall()
            glissade.id = result[0][0]
        else:
            connection.execute(
                "update Glissades set nom = ?, ouvert = ?,"
                "deblaye = ?,condition=? where rowid = ?",
                (
                    glissade.nom,
                    glissade.ouvert,
                    glissade.deblaye,
                    glissade.condition,
                    glissade.id,
                ),
            )
            connection.commit()
        return glissade

    def delete_glissade(self, glissade):
        connection = self.get_connection()
        connection.execute(
            "delete from Glissades where rowid = ?", (glissade.id,)
        )
        connection.commit()

    def getInstallationsByDate(self, date_maj):

        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT Patinoires.id_patinoire,Patinoires.nom_patinoire,"
            " nom_arrondissement,date_heure,ouvert,deblaye,arrose,"
            " resurface FROM Condition INNER JOIN Patinoires ON"
            " Condition.id_patinoire=Patinoires.id_patinoire"
            " INNER JOIN Arrondissement_Patinoires ON"
            " Patinoires.id_arrondissement="
            " Arrondissement_Patinoires.id_arrondissement"
            " WHERE date_heure like ? ORDER BY nom_patinoire ASC",
            ("%" + date_maj + "%",),
        )

        id = -1
        liste_patinoire = []
        patinoire = 0
        for row in cursor:
            if id != row[0]:
                patinoire = Patinoire(row[0], row[1], row[2])
                liste_patinoire.append(patinoire)
                id = row[0]

            patinoire.addConditions(row[3], row[4], row[5], row[6], row[7])

        if len(liste_patinoire) == 0:
            return None
        else:
            return liste_patinoire

    def getInstallationsByDateForCSV(self, date_maj):

        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT Patinoires.id_patinoire,Patinoires.nom_patinoire,"
            "nom_arrondissement,date_heure,ouvert,deblaye,arrose,resurface "
            "FROM Condition INNER JOIN Patinoires ON Condition.id_patinoire "
            "=Patinoires.id_patinoire INNER JOIN Arrondissement_Patinoires "
            "ON Patinoires.id_arrondissement"
            "=Arrondissement_Patinoires.id_arrondissement "
            "WHERE date_heure like ? ORDER BY nom_patinoire ASC ",
            ("%" + date_maj + "%",),
        )
        results = cursor.fetchall()

        if len(results) == 0:
            return None
        else:
            return results

    # methode pour tester les fonctionnalites de tweet et d'email
    def testAddNewInstallations(self):
        self.insert_in_Piscine_Installation_Aquatique(
            22,
            "Salon aquatique",
            "Test-01",
            "Verdun",
            "0000 Rue Lambert",
            "privé",
            "privé",
            "00",
            "00",
            "rien",
            "1",
            "1",
            False,
        )
        self.insert_in_glissades(
            "Test-01", "Verdun", "VER", "2021-11-08", 1, 1, "bonne", False
        )

        self.insert_in_patinoires("Verdun", "Patinoire Testuelle", False)
