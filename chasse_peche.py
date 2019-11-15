from joueur import *
from random import randint
from random import choice
import numpy as np
np.set_printoptions(precision=3)


class Chasse_et_peche(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True
        self.defenseur = False
        self.mode_chasse = True  # True = on tir au hasard; False = on pêche tant que le bateau visé nest pas coulé
        self.chasse = np.mat([[1 for i in range(10)] for j in range(10)])  # liste des cibles possibles lorsqu'on
        # est dans le mode chasse
        self.poisson = []  # bateau en cours de destruction

    def choisir_cible_chasse(self):
        return choice([(i, j) for i in range(10) for j in range(10) if self.chasse[i, j]])

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
        self.chasse[cible] = 0
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
                    self.chasse[a, b] = 0
            self.poisson = []
            self.peche = []


class Chasse_peche_croix(Chasse_et_peche):  # A ajouter à main
    def __init__(self, plateau_allie, plateau_adverse):
        Chasse_et_peche.__init__(self, plateau_allie, plateau_adverse)
        self.croix_pair = randint(0, 1)  # positions de coordonnées pair ou impair

    def choisir_cible_chasse(self):
        # print(self.chasse)
        matrice_croix = self.matrice_poids_croix()
        # print(matrice_croix)
        matrice_probabilite = self.matrice_poids_probabilite(self.chasse, self.plateau_adverse.bateaux[1:])  # Ajouter get_att
        # print(matrice_probabilite)
        matrice_poids = np.multiply(matrice_probabilite, matrice_croix)
        # print(matrice_poids)
        cibles = [(i, j) for j in range(10) for i in range(10) if matrice_poids[i, j] > matrice_poids.max() - 0.0001]
        cible = choice(cibles)
        # print(cible)
        # print()
        return cible

    def matrice_poids_probabilite(self, mat, bat_restants):
        return mat

    def matrice_poids_croix(self):
        """
        :return: matrice np composé de 1 sur les bonnes croix et de poids sur les mauvaises
        """
        poids = self.poids_croix(self.plateau_adverse.get_nb_tours())
        return np.mat([[1 - (poids * (int((i+j) % 2 == self.croix_pair))) for j in range(10)] for i in range(10)])

    def poids_croix(self, n):
        return 1


class Chasse_peche_croix_proba(Chasse_peche_croix):  # A ajouter à main / marche pas
    """Les croix sont parfaite : quelque soit la probabilité d'une case rayée, elle ne sera jamais choisi"""

    def matrice_poids_probabilite(self, mat, bat_restants):
        """ATTENTION : mat est une matrice numpy de 0 et de 1 et bat_restants une liste d'entiers"""

        mat = np.array(mat, dtype=int)
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

        mat_tot = np.zeros((10, 10), dtype=int)
        for k in range(len(bat_restants)):
            mat_tot += prob_un_bateau(mat, k)
            mat_tot += prob_un_bateau(mat.transpose(), k).transpose()
        # print(mat_tot)
        mat_tot = mat_tot/np.max(mat_tot)
        return mat_tot


class Chasse_peche_proba(Chasse_peche_croix_proba):  # A ajouter à main
    """Ne tiens pas compte des croix, uniquement de la densité de probabilité"""

    def poids_croix(self, n):
        return 0


class Chasse_peche_proba_croix_decroissance_lineaire(Chasse_peche_croix_proba):  # A ajouter à main
    """L'importance des croix diminue linéairement"""

    def poids_croix(self, n):
        return 1 - (n / 100)


class Chasse_peche_proba_croix_decroissance_expo(Chasse_peche_croix_proba):  # A ajouter à main
    """L'importance des croix diminue exponentiellement"""

    def poids_croix(self, n):
        lambd = 0.05
        return (lambd * np.exp(-lambd * n))
