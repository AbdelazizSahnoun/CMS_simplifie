class Installations:
    def __init__(self, id, nom, type):
        self.id = id
        self.nom = nom
        self.type = type

    def asDictionary(self):
        return {"ID": self.id, "Type": self.type, "nom": self.nom}

    def __str__(self):
        return self.nom + " " + self.type
