def test_bateaux(bateaux) :
    """Voici un algorithme qui teste si les bateaux que rentrent le joueur correspondent à une disposition valide.
    On attend une liste de 5 bateaux représentés par leur coordonnées, triés par ordre croissant de taille."""

    if type(bateaux) != list or bateaux == [] :
        return False

    for i in range(len(bateaux)) :
        if type(bateaux[i]) != list or bateaux[i] == [] :
            return False

    def domaine_coor(i) :
        return (i <= 9 and i >= 0)

    def global_coor() :
        c = True
        for i in range(len(bateaux)) :
            for j in range(len(bateaux[i])) :
                (a,b) = bateaux[i][j]
                c = c and domaine_coor(a) and domaine_coor(b)
        return c

    def recurrence_liste(L) :
        c = True
        for i in range(len(L)-1) :
            if L[i] >= L[i+1] :
                c = False
        return c

    def bateaux_integres() :
        c = True
        for i in range(len(bateaux)) :
            c = c and recurrence_liste(bateaux[i])
        return c

    def eclate_liste(L) :
        Lprime = []
        for i in range(len(L)) :
            for j in range(len(L[i])) :
                Lprime.append(L[i][j])
        return Lprime

    def chevauchement() :
        L = eclate_liste(bateaux)
        L.sort()
        return recurrence_liste(L)

    c1 = (len(bateaux) == 5)

    c2 = (len(bateaux[0]) == 2
          and len(bateaux[1]) == 3
          and len(bateaux[2]) == 3
          and len(bateaux[3]) == 4
          and len(bateaux[4]) == 5)

    c3 = (global_coor())

    c4 = (bateaux_integres())

    c5 = (chevauchement())

    return (c1 and c2 and c3 and c4 and c5)
