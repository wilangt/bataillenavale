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
        i,j=cible
        if res == 1:
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = False
        if res != 0:
            L =[(i-1,j-1),(i-1,j+1),(i+1,j+1),(i+1,j-1)]
            k = 3
            while k >= 0:
                (a, b) = L[k]
                if not ((0 <= a <= 9) and (0 <= b <= 9)):
                    L.pop(k)
                k -= 1
            for l in L:
                self.chasse[l] = 0
        if res == 2:
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = True
            self.poisson = []
            self.peche = []


class Chasse_peche_croix(Chasse_et_peche):  # A ajouter à main
    def __init__(self, plateau_allie, plateau_adverse):
        Chasse_et_peche.__init__(self, plateau_allie, plateau_adverse)
        self.croix_pair = randint(0, 1)  # positions de coordonnées pair ou impair
        self.bateaux = self.plateau_adverse.bateaux[1:]

    def choisir_cible_chasse(self):
        # print(self.chasse)
        matrice_croix = self.matrice_poids_croix()
        # print(matrice_croix)
        matrice_probabilite = self.matrice_poids_probabilite(self.chasse, self.bateaux)  # Ajouter get_att
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
        """ATTENTION : mat est une matrice numpy de 0 et de 1 et une liste d'entiers naturels"""
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

    def choisir_cible_peche(self) :
        n = len(self.poisson)
        (a,b) = self.poisson[-1]
        for (i,j) in [(a-1,b-1), (a-1,b+1), (a+1,b-1), (a+1,b+1)] :
            if (0<=i<=9) and (0<=j<=9) :
                self.chasse[i, j] = 0
        if n == 1 :
            matrice_poids = self.matrice_poids_probabilite(self.chasse, self.bateaux)
            cibles = [(a,b-1), (a,b+1), (a-1,b), (a+1,b)]
        if n >= 2 :
            self.poisson.sort()
            (a,b) = self.poisson[0]
            (c,d) = self.poisson[-1]
            bat = [i for i in self.bateaux if i > n]
            matrice_poids = self.matrice_poids_probabilite(self.chasse, bat)
            if a == c :
                cibles = [(a, b-1), (a, d+1)]
            else :
                cibles = [(a-1, b), (c+1, b)]
        cible = (0,(-1,-1))
        for (i,j) in cibles :
            if (0<=i<=9) and (0<=j<=9) and matrice_poids[i, j] >= cible[0] :
                cible = (matrice_poids[i, j],(i,j))
        return cible[1]

    def analyser(self, res, cible):
        if res == 0 :
            self.chasse[cible] = 0
        if res == 1 :
            self.poisson.append(cible)
            self.mode_chasse = False
        if res == 2 :
            for couple in self.poisson :
                self.chasse[couple] = 0
            (a,b) = cible
            for i in range(a-1, a+1) :
                for j in range(b-1, b+1) :
                    if (0<=i<=9) and (0<=j<=9) :
                        self.chasse[i, j] = 0
            self.bateaux.remove(len(self.poisson) + 1)
            self.poisson = []
            self.mode_chasse = True


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
