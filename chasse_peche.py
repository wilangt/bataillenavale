from joueur import *
from random import randint
from random import choice
from random import random
import numpy as np


class Chasse_et_peche(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True
        self.defenseur = False
        self.mode_chasse = True  # True = on tir au hasard; False = on pêche tant que le bateau visé nest pas coulé
        self.chasse = np.mat([[True for i in range(10)] for j in range(10)])  # liste des cibles possibles lorsqu'on
        # est dans le mode chasse
        self.poisson = []  # bateau en cours de destruction
        self.croix_pair = randint(0, 1)  # positions de coordonnées pair ou impair

    def choisir_cible_chasse(self):
        a_tenter = [(i, j) for i in range(10) for j in range(10) if self.chasse[i, j]]
        return choice(self.choix(a_tenter))

    def choisir_cible_peche(self):
        n = len(self.poisson)
        (i, j) = self.poisson[-1]
        if n == 1:
            v = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
            k = 3
            while k >= 0:
                (a, b) = v[k]
                if not ((0 <= a <= 9) and (0 <= b <= 9)):
                    v.pop(k)
                k -= 1
        else:
            if self.poisson[0][0] == self.poisson[1][0]:
                v = [(i, self.poisson[0][1] - 1), (i, j + 1)]
            else:
                v = [(self.poisson[0][0] - 1, j), (i + 1, j)]
            k = 1
            while k >= 0:
                (a, b) = v[k]
                if (not ((0 <= a <= 9) and (0 <= b <= 9))) or (not self.chasse[a, b]):
                    v.pop(k)
                k -= 1
        return choice(v)

    def choisir_cible(self):
        if self.mode_chasse:
            return self.choisir_cible_chasse()
        else:
            return self.choisir_cible_peche()

    def analyser(self, res, cible):
        self.chasse[cible] = False
        if res == 1:
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = False
        if res == 2:
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = True
            (i, j), (k, l) = self.poisson[0], self.poisson[-1]
            for a in range(max(0, i - 1), min(10, k + 2)):
                for b in range(max(0, j - 1), min(10, l + 2)):
                    self.chasse[a, b] = False
            self.poisson = []
            self.peche = []

    def choix(self, cibles_avant):
        """
        Renvoie une liste de cible dont les coordonnées situées sur le mauvais coté de la croix ont été enlevées avec une 
        probabilité qui dépend du nombre de tour (proba_mauvaise_croix). Si 'proba_mauvaise_croix' renvoie 1 tout le temps, la 
        liste renvoyée est identique à celle passée en argument. Il reste à vérifier que la distribution obtenue est bien la
        distribution souhaitée
        """
        proba = self.proba_mauvaise_croix(self.plateau_adverse.get_nb_tours())
        return [cible for cible in cibles_avant if (cible[0] + cible[1]) % 2 == self.croix_pair or proba > random()]

    def proba_mauvaise_croix(self, n):
        return 1


class Chasse_peche_croix(Chasse_et_peche):  # A ajouter à main
    def proba_mauvaise_croix(self, n):
        return 0


class Chasse_peche_croix_proba(Chasse_peche_croix):  # A ajouter à main / marche pas
    """Les croix sont parfaite : quelque soit la probabilité d'une case rayée, elle ne sera jamais choisi"""

    def choisir_cible_chasse(self):
        cibles_candidates = self.choix(self.chasse)
        matrice_probabilite = self.probabilite_chasse(self.chasse, self.plateau_adverse.bateaux[1:])  # Ajouter get_att
        for couple in cibles_candidates:
            matrice_probabilite[couple] += 100
        cible = np.unravel_index(np.argmax(matrice_probabilite, axis=None), matrice_probabilite.shape)
        return cible

    def probabilite_chasse(self, mat, bat_restants):
        """ATTENTION : mat est une matrice numpy de 0 et de 1 et bat_restants une liste d'entiers"""

        mat = np.array(mat)
        def prob_un_bateau(mat, k):
            prob = mat.copy()
            nb = bat_restants[k]
            for i in range(10):
                compt = 1
                for j in range(10):
                    if prob[i, j] == 0:
                        compt = 0
                    prob[i, j] = compt
                    compt += 1
            for i in range(10):
                for j in range(10):
                    if prob[i, j] < nb:
                        prob[i, j] = 0
                    else:
                        prob[i, j] = 1
                        for l in range(1, nb):
                            prob[i, j - l] += 1
            return prob

        mat_tot = np.zeros((10, 10))
        for k in range(len(bat_restants)):
            mat_tot += prob_un_bateau(mat, k)
            mat_tot += prob_un_bateau(mat.transpose(), k).transpose()
        mat_tot = mat_tot/np.max(mat_tot)
        return mat_tot


class Chasse_peche_croix_proba_parfaite(Chasse_peche_croix_proba):  # A ajouter à main
    """Ne tiens pas compte des croix, uniquement de la densité de probabilité"""

    def proba_mauvaise_croix(self, n):
        return 1


class Chasse_peche_croix_proba_decroissance_lineaire(Chasse_peche_croix_proba):  # A ajouter à main
    """L'importance des croix diminue linéairement"""

    def proba_mauvaise_croix(self, n):
        return (n / 100)


class Chasse_peche_croix_proba_decroissance_expo(Chasse_peche_croix_proba):  # A ajouter à main
    """L'importance des croix diminue exponentiellement"""

    def proba_mauvaise_croix(self, n):
        lambd = 0.05
        return 1 - (lambd * np.exp(-lambd * n))
