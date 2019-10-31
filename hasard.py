from joueur import *
from random import randint
from random import choice


class HasardDebile(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True

    def choisir_cible(self):
        return (randint(0, 9), randint(0, 9))


class HasardMalin(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True

    def choisir_cible(self):
        a_tenter = [(i, j) for i in range(10) for j in range(10) if self.plateau_adverse.jamais_vu((i, j))]
        return choice(a_tenter)
