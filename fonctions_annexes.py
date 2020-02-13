import sys
import time


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
        for n in range(len(liste)):
            s += liste[n]
        return s

    def moyenne(liste):
        return somme(liste) / len(liste)

    def k_termes(n, m):
        return (m * (m + 1)) / 2 - (n * (n - 1)) / 2

    for k in range(5):
        l1, l2 = [], []
        for j in range(len(bateaux[k])):
            (a, b) = bateaux[k][j]
            l1.append(a), l2.append(b)
        c1 = moyenne(l1) == l1[0] and somme(l2) == k_termes(l2[0], l2[-1])
        c2 = moyenne(l2) == l2[0] and somme(l1) == k_termes(l1[0], l1[-1])
        if not (c1 or c2):
            return False

    interface = [[0 for _ in range(10)] for _ in range(10)]
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


def coor(a, b):
    return (0 <= a <= 9) and (0 <= b <= 9)


class BarreDeProgression:
    """Cette classe permet de créer des barres de chargement"""

    def __init__(self, taille=30, titre='Chargement'):
        self.taille = taille
        self.titre = titre
        self.pourcentage = 0
        self.pourcentage_precedent = 0
        self.temps = time.time()
        self.temps_restant = 'Calcul...'

        print("\nC'est parti !")
        self.maj()

    def maj(self, pourcentage=0):
        self.pourcentage = pourcentage
        etapes = int(self.pourcentage / 100 * self.taille)

        if self.pourcentage - self.pourcentage_precedent >= 5:
            self.temps_restant = (time.time() - self.temps) * (100 - pourcentage) / 5
            self.temps = time.time()
            self.pourcentage_precedent = self.pourcentage

        temps_restant = self.temps_restant

        if etapes == 0:
            visuel = self.taille * ' '
        else:
            visuel = etapes * '=' + (self.taille - etapes) * ' '

        if self.pourcentage == 100:
            sys.stdout.write('\rTerminé !' + (self.taille + 100) * ' ' + '\n')
        else:
            if type(self.temps_restant) != str:
                temps_restant = format_temps(int(self.temps_restant))
            sys.stdout.write('\r' + self.titre + ' [' + visuel + '] ' + str(
                int(self.pourcentage)) + '%        Temps restant : ' + temps_restant)
        sys.stdout.flush()


def format_temps(temps):
    if temps > 3600:
        h = temps // 3600
        m = (temps // 60) % 60
        s = temps % 60
        return str(h) + ' h. ' + str(m) + ' m. ' + str(s) + ' s.   '
    elif temps > 60:
        m = temps // 60
        s = temps % 60
        return str(m) + ' m. ' + str(s) + ' s.          '
    else:
        return str(temps) + ' s.                '

