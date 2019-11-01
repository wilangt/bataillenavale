from joueur import *
from random import randint
from random import choice
from fonctions_annexes import test_bateaux


class HasardDebile(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True

    def choisir_cible(self):
        return randint(0, 9), randint(0, 9)


class HasardMalin(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True

    def choisir_cible(self):
        a_tenter = [(i, j) for i in range(10) for j in range(10) if self.plateau_adverse.jamais_vu((i, j))]
        return choice(a_tenter)


class HasardDefense(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = False
        self.defenseur = True

    def position_bateaux(self):
        def position_1_bateau(taille):
            xpoupe = randint(0, 9 - taille)
            ypoupe = randint(0, 9)
            if bool(randint(0, 1)):  # Horizontal ou vertical
                bateau = [(xpoupe + i, ypoupe) for i in range(taille)]
            else:
                bateau = [(ypoupe, xpoupe + i) for i in range(taille)]
            return bateau

        bateaux=[[], [], [], [], []]
        compteur = 0
        while not test_bateaux(bateaux):
            compteur += 1
            bateaux = [position_1_bateau(k) for k in [2, 3, 3, 4, 5]]
            if compteur > 1000:
                raise NameError("Trop de tentatives ({}) pour placer les bateaux".format(compteur))

        print("bateaux placés en {} coup(s)".format(compteur))
        return bateaux
