from fonctions_annexes import *


class Joueur:
    """Classe maitresse, dont découle toutes les autres classes de joueurs"""

    def __init__(self, plateau_allie, plateau_adverse):
        self.plateau_allie = plateau_allie
        self.plateau_adverse = plateau_adverse
        self.defenseur = False
        self.attaquant = False
        self.enregistrer_vecteur = False

    def position_bateaux(self):
        """Fonction qui renvoie la position des bateaux sous forme d'une liste. A completer ou a supprimer"""
        raise NameError("Erreur, pas de fonction placerBateaux")

    def placer_bateaux(self):
        """Fonction qui place les bateaux sur le plateau. A ne pas toucher"""
        bateaux = self.position_bateaux()
        if test_bateaux(bateaux):
            self.plateau_allie.placer_bateaux(bateaux)
        else:
            raise NameError("Erreur, les bateaux n'ont pas été placés correctement")

    def choisir_cible(self):
        """Fonction qui étant donné une configuration, choisi une cible et la renvoie sous forme de coordonnées.
        A completer ou a supprimer"""
        raise NameError("Erreur, pas de fonction choisirCible")

    def attaquer(self):
        """Fonction qui ouvre le feu sur une position ennemie. A ne pas toucher"""
        cible = self.choisir_cible()
        self.analyser(self.plateau_adverse.feu(cible), cible)

    def analyser(self, resultat, cible):
        """Fonction qui analyse la réponse du tir. A completer ou a supprimer"""
        pass

    def est_defenseur(self):
        """Fonction qui permet de savoir si le joueur peut défendre"""
        return self.defenseur

    def est_attaquant(self):
        """Fonction qui permet de savoir si le joueur peut attaquer"""
        return self.attaquant


"""
Template pour sous-classes de joueur :
class Joueur(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = False
        self.defenseur = False

    def position_bateaux(self):
        pass
        # ICI remplir ou supprimer

    def choisir_cible(self):
        pass
        # ICI remplir ou supprimer

    def analyser(self, res):
        pass
        # ICI remplir ou supprimer

"""
