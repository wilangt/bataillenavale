import numpy as np


def test_bateaux(bateaux):
    """Voici un algorithme qui teste si les bateaux que rentrent le joueur correspondent à une disposition valide.
    On attend une liste de 5 bateaux représentés par leur coordonnées, triés par ordre croissant de taille."""

    if type(bateaux) != list or len(bateaux) != 5:
        return False

    for i in range(len(bateaux)):
        if type(bateaux[i]) != list:
            return False

    if (len(bateaux[0]), len(bateaux[1]), len(bateaux[2]), len(bateaux[3]), len(bateaux[4])) != (2, 3, 3, 4, 5):
        return False

    def condition(var):
        return (9 >= var) and (var >= 0)

    for k in range(5):
        bateaux[k].sort()
        for j in range(len(bateaux[k])):
            (a, b) = bateaux[k][j]
            if not (condition(a) and condition(b)):
                return False

    def somme(liste):
        s = 0
        for i in range(len(liste)):
            s += liste[i]
        return s

    def moyenne(liste):
        return somme(liste) / len(liste)

    def k_termes(n, m):
        return (m * (m + 1)) / 2 - (n * (n - 1)) / 2

    l1, l2 = [], []
    c1, c2 = True, True
    for k in range(5):
        l1, l2 = [], []
        for j in range(len(bateaux[k])):
            (a, b) = bateaux[k][j]
            l1.append(a), l2.append(b)
        c1 = moyenne(l1) == l1[0] and somme(l2) == k_termes(l2[0], l2[-1])
        c2 = moyenne(l2) == l2[0] and somme(l1) == k_termes(l1[0], l1[-1])
        if not (c1 or c2):
            return False

    interface = [[0 for i in range(10)] for j in range(10)]
    for k in range(5):
        (d1, d2), (f1, f2) = bateaux[k][0], bateaux[k][-1]
        for i in range(d1 - 1, f1 + 2):
            for j in range(d2 - 1, f2 + 2):
                if condition(i) and condition(j):
                    interface[i][j] += 1
        for i in range(len(bateaux[k])):
            (a, b) = bateaux[k][i]
            interface[a][b] += 1
    for i in range(10):
        for j in range(10):
            if interface[i][j] > 2:
                return False

    return True


def densite_proba(mat, bat_restants):
    """ATTENTION : mat est une matrice numpy de 0 et de 1 et bat_restants une liste d'entiers"""

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

    return mat_tot
