import numpy as np
import random
import chasse_peche
import pickle as cornichon
import os


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
                print("Époque {}: {:.2f}% ({} tests)".format(j, self.tester_IA(donnees_test)*100, n_test))
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
        return nb_cibles_valide/nb_cibles

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


def demander_ia():
    liste_ia = os.listdir("ia_sl/")
    n = len(liste_ia)
    liste_choix = list(range(n))
    choix = -1
    print("Quelle IA ?")
    while choix not in liste_choix:
        for num_ia in range(n):
            print("{} : {}".format(num_ia, liste_ia[num_ia]))
        choix = int(input())
    return liste_ia[choix]


class IaSl(chasse_peche.ChassePecheCroixProba):
    def __init__(self, plateau_allie, plateau_adverse):
        chasse_peche.ChassePecheCroixProba.__init__(self, plateau_allie, plateau_adverse)
        self.nom_ia = None
        if plateau_adverse != plateau_allie:
            if self.nom_ia == None:
                self.nom_ia = demander_ia()
            file = open("ia_sl/{}".format(self.nom_ia), "rb")
            self.resal = cornichon.load(file)
            file.close()

    def choisir_cible_chasse(self):
        cibles = self.resal.trouver_cibles(self.plateau_adverse.renvoyer_vecteur_init())
        cibles_valides = [(i, j) for (i, j) in cibles if self.plateau_adverse.jamais_vu((i, j))]
        if cibles_valides:
            return random.choice(cibles_valides)
        else:
            cibles = self.resal.lister_cibles(self.plateau_adverse.renvoyer_vecteur_init())
            cibles.sort(reverse=True)
            for (p, (i, j)) in cibles:
                if self.plateau_adverse.jamais_vu((i, j)):
                    return i, j
