class Patinoire:
    def __init__(self, id, nom, nom_arr):
        self.id = id
        self.nom = nom
        self.nom_arr = nom_arr
        self.conditions = []

    def addConditions(self, date_heure, ouvert, deblaye, arrose, resurface):
        self.conditions.append(date_heure)
        self.conditions.append(ouvert)
        self.conditions.append(deblaye)
        self.conditions.append(arrose)
        self.conditions.append(resurface)

    def asDictionary(self):
        retour = {}
        retour["ID"] = self.id
        retour["Nom"] = self.nom
        retour["Arrondisement"] = self.nom_arr

        liste = []
        i = 0
        while i < len(self.conditions):
            temp = {
                "Date de mise à jour": self.conditions[i],
                "Ouvert": self.conditions[i + 1],
                "Deblaye": self.conditions[i + 2],
                "Arrose": self.conditions[i + 3],
                "Resurface": self.conditions[i + 4],
            }
            liste.append(temp)
            i += 5

        retour["Conditions"] = liste
        return retour
