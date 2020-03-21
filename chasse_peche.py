from joueur import *
from random import randint
from random import choice
import numpy as np
import pickle as cornichon


class ChasseEtPeche(Joueur):
    def __init__(self, plateau_allie, plateau_adverse, enregistrer_vecteur=0):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True
        self.defenseur = False
        self.mode_chasse = True  # True = on tire au hasard; False = on pêche tant que le bateau visé nest pas coulé
        self.chasse = np.mat([[1 for _ in range(10)] for _ in range(10)])  # liste des cibles possibles lorsqu'on
        # est dans le mode chasse
        self.poisson = []  # bateau en cours de destruction
        self.colonne = True  # si le poisson est en colonne
        self.peche = []

    def choisir_cible_chasse(self):
        return choice([(i, j) for i in range(10) for j in range(10) if self.chasse[i, j]])

    def choisir_cible_peche(self):
        n = len(self.poisson)
        (i, j) = self.poisson[-1]
        (a, b) = self.poisson[0]
        if n == 1:
            v = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
            k = 3
            while k >= 0:
                (a, b) = v[k]
                if not (coor(a, b)):
                    v.pop(k)
                k -= 1
        else:
            if a == i:
                self.colonne = False
                v = [(i, b - 1), (i, j + 1)]
            else:
                v = [(a - 1, j), (i + 1, j)]
            k = 1
            while k >= 0:
                (a, b) = v[k]
                if (not (coor(a, b))) or (not self.chasse[a, b]):
                    v.pop(k)
                k -= 1
        if self.enregistrer_vecteur == 2:
            enregistrer_cornichon(self.plateau_adverse.renvoyer_vecteur_init(self.enregistrer_vecteur), renvoyer_vecteur_sortie_peche(v), v, 'peche')
        return choice(v)

    def choisir_cible(self):
        if self.mode_chasse:
            return self.choisir_cible_chasse()
        else:
            return self.choisir_cible_peche()

    def analyser(self, res, cible):
        self.chasse[cible] = 0
        i, j = cible
        if res == 1:
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = False
        if res != 0:
            l_maj = [(i - 1, j - 1), (i - 1, j + 1), (i + 1, j + 1), (i + 1, j - 1)]
            k = 3
            while k >= 0:
                (a, b) = l_maj[k]
                if not (coor(a, b)):
                    l_maj.pop(k)
                k -= 1
            for l_min in l_maj:
                self.chasse[l_min] = 0
        if res == 2:
            self.poisson.append(cible)
            self.poisson.sort()
            (a, b), (c, d) = self.poisson[0], self.poisson[-1]
            if self.colonne:
                if coor(a - 1, 1):
                    self.chasse[a - 1, b] = 0
                if coor(c + 1, 1):
                    self.chasse[c + 1, b] = 0
            else:
                if coor(b - 1, 1):
                    self.chasse[a, b - 1] = 0
                if coor(d + 1, 1):
                    self.chasse[a, d + 1] = 0
            self.colonne = True
            self.mode_chasse = True
            self.poisson = []
            self.peche = []


class ChassePecheCroix(ChasseEtPeche):
    def __init__(self, plateau_allie, plateau_adverse, enregistrer_vecteur=0):
        ChasseEtPeche.__init__(self, plateau_allie, plateau_adverse)
        self.croix_pair = randint(0, 1)  # positions de coordonnées pair ou impair
        self.bateaux = self.plateau_adverse.bateaux[1:]
        self.enregistrer_vecteur = enregistrer_vecteur

    def choisir_cible_chasse(self):
        matrice_croix = self.matrice_poids_croix()
        matrice_probabilite = self.matrice_poids_probabilite(self.chasse, self.bateaux)  # Ajouter get_att
        matrice_poids = np.multiply(matrice_probabilite, matrice_croix)
        cibles = [(i, j) for j in range(10) for i in range(10) if matrice_poids[i, j] > matrice_poids.max() - 0.0001]
        cible = choice(cibles)
        if self.enregistrer_vecteur == 1:
            enregistrer_cornichon(self.plateau_adverse.renvoyer_vecteur_init(self.enregistrer_vecteur), renvoyer_vecteur_sortie_chasse(matrice_poids), cibles, 'chasse')
        return cible

    def matrice_poids_probabilite(self, mat, bat_restants):
        return mat

    def matrice_poids_croix(self):
        """
        :return: matrice np composé de 1 sur les bonnes croix et de poids sur les mauvaises
        """
        poids = self.poids_croix(self.plateau_adverse.get_nb_tours())
        return np.mat([[1 - (poids * (int((i + j) % 2 == self.croix_pair))) for j in range(10)] for i in range(10)])

    def poids_croix(self, n):
        return 1


class ChassePecheCroixProba(ChassePecheCroix):  # A ajouter à main / marche pas
    """Les croix sont parfaite : quelque soit la probabilité d'une case rayée, elle ne sera jamais choisi"""

    def matrice_poids_probabilite(self, mat, bat_restants):  # ici
        """ATTENTION : mat est une matrice numpy de 0 et de 1 et une liste d'entiers naturels"""
        mat = np.array(mat, dtype=int)

        def prob_un_bateau(matrice, n):
            prob = matrice.copy()
            nb = bat_restants[n]
            for i in range(10):
                compteur = 1
                for j in range(10):
                    if prob[i, j] == 0:
                        compteur = 0
                    prob[i, j] = compteur
                    compteur += 1
            for i in range(10):
                for j in range(10):
                    if prob[i, j] < nb:
                        prob[i, j] = 0
                    else:
                        prob[i, j] = 1
                        for m in range(1, nb):
                            prob[i, j - m] += 1
            return prob

        mat_tot = np.zeros((10, 10), dtype=int)
        for k in range(len(bat_restants)):
            mat_tot += prob_un_bateau(mat, k)
            mat_tot += prob_un_bateau(mat.transpose(), k).transpose()
        # print(mat_tot)
        if np.max(mat_tot) == 0:
            for i in range(10):
                for j in range(10):
                    if self.plateau_adverse.jamais_vu((i,j)):
                        mat_tot[i,j] = 1
        mat_tot = mat_tot / np.max(mat_tot)
        return mat_tot

    def choisir_cible_peche(self):  # ici
        n = len(self.poisson)
        cibles = []
        matrice_poids = np.zeros((10, 10), dtype=int)
        (a, b) = self.poisson[-1]
        for (i, j) in [(a - 1, b - 1), (a - 1, b + 1), (a + 1, b - 1), (a + 1, b + 1)]:
            if coor(i, j):
                self.chasse[i, j] = 0
        if n == 1:
            matrice_poids = self.matrice_poids_probabilite(self.chasse, self.bateaux)
            cibles = [(a, b - 1), (a, b + 1), (a - 1, b), (a + 1, b)]
        if n >= 2:
            self.poisson.sort()
            (a, b) = self.poisson[0]
            (c, d) = self.poisson[-1]
            bat = [i for i in self.bateaux if i > n]
            matrice_poids = self.matrice_poids_probabilite(self.chasse, bat)
            if a == c:
                cibles = [(a, b - 1), (a, d + 1)]
            else:
                cibles = [(a - 1, b), (c + 1, b)]
        cible = (0, (-1, -1))
        for (i, j) in cibles:
            if coor(i, j) and matrice_poids[i, j] >= cible[0]:
                cible = (matrice_poids[i, j], (i, j))
        return cible[1]

    def analyser(self, res, cible):
        if res == 0:
            self.chasse[cible] = 0
        if res == 1:
            self.poisson.append(cible)
            self.mode_chasse = False
        if res == 2:
            for couple in self.poisson:
                self.chasse[couple] = 0
            (a, b) = cible
            if (a, b) > self.poisson[0]:
                (c, d) = self.poisson[0]
            else:
                (c, d) = self.poisson[-1]
            for (k, l) in [(a, b), (c, d)]:
                for i in range(k - 1, k + 1):
                    for j in range(l - 1, l + 1):
                        if coor(i, j):
                            self.chasse[i, j] = 0
            self.bateaux.remove(len(self.poisson) + 1)
            self.poisson = []
            self.mode_chasse = True


class ChassePecheProba(ChassePecheCroixProba):  # A ajouter à main
    """Ne tiens pas compte des croix, uniquement de la densité de probabilité"""

    def poids_croix(self, n):
        return 0


class ChassePecheProbaCroixDecroissanceLineaire(ChassePecheCroixProba):  # A ajouter à main
    """L'importance des croix diminue linéairement"""

    def poids_croix(self, n):
        return 1 - (n / 100)


class ChassePecheProbaCroixDecroissanceExpo(ChassePecheCroixProba):  # A ajouter à main
    """L'importance des croix diminue exponentiellement"""

    def poids_croix(self, n):
        lambdaa = 0.05
        return lambdaa * np.exp(-lambdaa * n)


def renvoyer_vecteur_sortie_chasse(mat):
    return [mat[i,j] for i in range(10) for j in range(10)]


def renvoyer_vecteur_sortie_peche(l):       # matrice de taille 100 avec proba 1 dans les cases autour de celles qu'on vient de toucher et qui sont encore possibles, proba de 0 dans toutes les autres cases.
    L = [0 for i in range(100)]
    for k in l:
        (i,j) = k
        L[10*i+j] = 1
    return L


def enregistrer_cornichon(entree, sortie, cibles, mode):
    file = open("donnees/cornichon_" + mode + ".txt", "r")
    indice = int(file.read())
    file.close()
    file = open("donnees/" + mode + "-" + str(indice), 'wb')
    cornichon.dump((entree, sortie, cibles), file)
    file.close()
    file = open("donnees/cornichon_" + mode + ".txt", "w")
    file.write(str(indice + 1))
    file.close()
