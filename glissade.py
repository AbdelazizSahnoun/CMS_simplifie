class Glissade:
    def __init__(self, id, nom, ouvert, deblaye, condition):
        self.id = id
        self.nom = nom
        self.ouvert = ouvert
        self.deblaye = deblaye
        self.condition = condition

    def asDictionary(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "ouvert": self.ouvert,
            "deblaye": self.deblaye,
            "condition": self.condition,
        }
