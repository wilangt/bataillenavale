
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

def coor(a,b) :
    return (0<=a<=9) and (0<=b<=9)