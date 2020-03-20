import numpy as np
import random
import chasse_peche
import pickle as cornichon
import os
import plateau
from fonctions_annexes import *


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))


def derivee_couteuse(sortie, y):
    # print(sortie)
    # print(y)
    return sortie - y


def transformer_y(y):
    return np.array([[x] for x in y])


class Resal:
    def __init__(self, couches):
        self.couches = couches
        self.nombre_couche = len(couches)
        self.biais = [np.random.randn(y, 1) for y in couches[1:]]
        self.poids = [np.random.randn(y, x) for (x, y) in zip(couches[:-1], couches[1:])]
        # print(self.biais)
        # print(self.poids)

    def evaluation(self, a):
        for b, p in zip(self.biais, self.poids):
            a = sigmoid(np.dot(p, a) + b)
        return a

    def DGS(self, donnees_entrainement, epoque, taille_mini_nacho, eta, donnees_test=None):
        n_test = 0
        if donnees_test:
            n_test = len(donnees_test)
        n = len(donnees_entrainement)
        for j in range(epoque):
            random.shuffle(donnees_entrainement)
            mini_nachos = [
                donnees_entrainement[k:k + taille_mini_nacho] for k in range(0, n, taille_mini_nacho)
            ]
            for mini_nacho in mini_nachos:
                self.maj_mini_nacho(mini_nacho, eta)
            if donnees_test:
                print("Époque {}: {:.2f}% ({} tests)".format(j, self.tester_IA(donnees_test) * 100, n_test))
            else:
                print("Époque {} terminée".format(j))

    def maj_mini_nacho(self, mini_nacho, eta):
        nabla_b = [np.zeros(b.shape) for b in self.biais]
        nabla_p = [np.zeros(p.shape) for p in self.poids]
        for (x, y, z) in mini_nacho:
            x = transformer_y(x)
            y = transformer_y(y)
            delta_nabla_b, delta_nabla_p = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_p = [nw + dnw for nw, dnw in zip(nabla_p, delta_nabla_p)]
        self.poids = [w - (eta / len(mini_nacho)) * nw for w, nw in zip(self.poids, nabla_p)]
        self.biais = [b - (eta / len(mini_nacho)) * nb for b, nb in zip(self.biais, nabla_b)]

    def trouver_cibles(self, x):
        x = transformer_y(x)
        reponse = self.evaluation(x)
        cibles = [(i // 10, i % 10) for i in range(100) if reponse[i][0] > np.max(reponse) - 0.0001]
        return cibles

    def lister_cibles(self, x):
        x = transformer_y(x)
        reponse = self.evaluation(x)
        cibles = [(reponse[i][0], (i // 10, i % 10)) for i in range(100)]
        return cibles

    def tester_IA(self, donnees_test):
        s = 0
        nb_cibles = 0
        nb_cibles_valide = 0
        for x, y, z in donnees_test:
            cibles = self.trouver_cibles(x)  # cibles de l'IA
            nb_cibles += len(cibles)
            for cible in cibles:
                if cible in z:  # z = cibles de CPP
                    nb_cibles_valide += 1
        return nb_cibles_valide / nb_cibles

    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biais]
        nabla_w = [np.zeros(w.shape) for w in self.poids]
        # feedforward
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biais, self.poids):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        delta = derivee_couteuse(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for c in range(2, self.nombre_couche):
            z = zs[-c]
            sp = sigmoid_prime(z)
            delta = np.dot(self.poids[-c + 1].transpose(), delta) * sp
            nabla_b[-c] = delta
            nabla_w[-c] = np.dot(delta, activations[-c - 1].transpose())
        return nabla_b, nabla_w


def demander_ia(dossier):
    liste_ia = os.listdir("ia_enregistrees/" + dossier + "/")
    n = len(liste_ia)
    liste_choix = list(range(n))
    choix = -2
    print("Quelle IA ?")
    while not choix in (liste_choix + [-1]):
        for num_ia in range(n):
            print("{} : {}".format(num_ia, liste_ia[num_ia]))
        if 'chasse' in dossier:
            print("-1 : Chasse de ChasseEtPeche")
        elif 'peche' in dossier:
            print("-1 : Pêche de ChasseEtPeche")
        choix = int(input())
    if choix == -1 :
        return None
    else:
        return liste_ia[choix]


class IaSl(chasse_peche.ChassePecheProba):
    def __init__(self, plateau_allie, plateau_adverse):
        chasse_peche.ChassePecheProba.__init__(self, plateau_allie, plateau_adverse)
        self.nom_ia_chasse = None
        self.resal_chasse = None
        self.nom_ia_peche = None
        self.resal_peche = None

    def attribuer_nom(self, nom):
        self.nom_ia_chasse, self.nom_ia_peche = nom

    def initialiser_ia(self):
        if self.plateau_adverse != self.plateau_allie:
            if self.nom_ia_chasse is not None:
                file = open("ia_enregistrees/ia_sl_chasse/{}".format(self.nom_ia_chasse), "rb")
                self.resal_chasse = cornichon.load(file)
                file.close()
            if self.nom_ia_peche is not None:
                file = open("ia_enregistrees/ia_sl_peche/{}".format(self.nom_ia_peche), "rb")
                self.resal_peche = cornichon.load(file)
                file.close()

    def test_initialisation(self):
        if self.resal_chasse is None and self.resal_peche is None:
            self.initialiser_ia()

    def choisir_cible_chasse(self):
        if self.nom_ia_chasse is not None:
            cibles = self.resal_chasse.trouver_cibles(self.plateau_adverse.renvoyer_vecteur_init(1))
            cibles_valides = [(i, j) for (i, j) in cibles if self.plateau_adverse.jamais_vu((i, j))]
            if cibles_valides:
                return random.choice(cibles_valides)
            else:
                cibles = self.resal_chasse.lister_cibles(self.plateau_adverse.renvoyer_vecteur_init(1))
                cibles.sort(reverse=True)
                for (p, (i, j)) in cibles:
                    if self.plateau_adverse.jamais_vu((i, j)):
                        return i, j
        else:
            matrice_poids = self.matrice_poids_probabilite(self.chasse, self.bateaux)
            cibles = [(i, j) for j in range(10) for i in range(10) if matrice_poids[i, j] > matrice_poids.max() - 0.0001]
            cible = random.choice(cibles)
            return cible

    def choisir_cible_peche(self):
        if self.nom_ia_peche is not None:
            cibles = self.resal_peche.trouver_cibles(self.plateau_adverse.renvoyer_vecteur_init(2))
            cibles_valides = [(i, j) for (i, j) in cibles if self.plateau_adverse.jamais_vu((i, j))]
            if cibles_valides:
                return random.choice(cibles_valides)
            else:
                cibles = self.resal_peche.lister_cibles(self.plateau_adverse.renvoyer_vecteur_init(2))
                cibles.sort(reverse=True)
                for (p, (i, j)) in cibles:
                    if self.plateau_adverse.jamais_vu((i, j)):
                        return i, j
        else:
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

    def analyser(self,res,cible):
        if res == 0:
            self.chasse[cible] = 0
        if res == 1:
            self.chasse[cible] = 0
            self.mode_chasse = False
        if res == 2:
            p = self.plateau_adverse.plateauVisible # ça ne marche pas, il faut accéder à plateau visble
            (a,b) = cible
            v = [(a - 1, b - 1), (a - 1, b + 1), (a + 1, b - 1), (a + 1, b + 1)]
            for (i,j) in v:
                if p[i,j] == 1:
                    v.pop((i,j))
            for (k,l) in v:
                i = 1
                if k == a:
                    if l == b+1:
                        while coor(k,b+i) and p[k,b+i] == 1 :
                            i+=1
                    else:
                        while coor(k,b-i) and p[k,b-i] == 1 :
                            i+=1
                else :
                    if k == a+1:
                        while coor(a+i,l) and p[a+i,l] == 1 :
                            i+=1
                    else:
                        while coor(a-i,l) and p[a-i,l] == 1 :
                            i+=1

            self.bateaux.remove(i)
            self.mode_chasse = True
