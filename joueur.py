from fonctions_annexes import *


class Joueur:
    """Classe maitresse, dont découle toutes les autres classes de joueurs"""

    def __init__(self, plateau_allie, plateau_adverse):
        self.plateau_allie = plateau_allie
        self.plateau_adverse = plateau_adverse
        self.defenseur = False
        self.attaquant = False

    def position_bateaux(self):
        raise NameError("Erreur, pas de fonction placerBateaux")

    def placer_bateaux(self):
        bateaux = self.position_bateaux()
        if test_bateaux(bateaux):
            self.plateau_allie.placer_bateaux(bateaux)
        else:
            raise NameError("Erreur, les bateaux n'ont pas été placés correctement")

    def choisir_cible(self):
        raise NameError("Erreur, pas de fonction choisirCible")

    def attaquer(self):
        self.analyser(self.plateau_adverse.feu(self.choisir_cible()))

    def analyser(self, resultat):
        pass

    def est_defenseur(self):
        return self.defenseur

    def est_attaquant(self):
        return self.attaquant
