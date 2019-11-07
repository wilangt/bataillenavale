from humain import *
from hasard import *
from plateau import *
from time import sleep

print()


def main():
    liste_defenseur = [Humain, HasardDefense, ConfigInit]
    liste_attaquant = [Humain, HasardDebile, HasardMalin]
    tester_liste_joueurs(liste_defenseur, liste_attaquant)

    att_def = True
    # att_def = choisir_mode()

    interface = demander_interface()
    if not interface:
        liste_defenseur = liste_defenseur[1:]
        liste_attaquant = liste_attaquant[1:]

    classe_participants = choisir_participants(att_def, liste_defenseur, liste_attaquant)

    plateau1 = Plateau()
    plateau2 = Plateau()

    if att_def:
        classe_def, classe_att = classe_participants
        defenseur, attaquant = classe_def(plateau1, plateau2), classe_att(plateau2, plateau1)

        defenseur.placer_bateaux()

        if interface:
            plateau1.init_interface(500)
            plateau1.afficher_interface()

        compteur = 0
        while not (plateau1.defaite()):
            attaquant.attaquer()
            compteur += 1
            if interface:
                sleep(0.01)

        plateau1.cacher_interface()
        pygame.display.quit()
        pygame.quit()
        print("Partie terminée en {} coups".format(compteur))

    """
    # A completer : flemme, et utile seulement dans longtemps
    else:
        classe_def1, classe_att1, classe_def2, classe_att2 = classe_participants
        defenseur1, attaquant1, defenseur2, attaquant2 = classe_def1(), classe_att1(), classe_def2(), classe_att2()
        # Attention, format de classe pas a jour : il manque les plateaux
    """


def choisir_mode():
    """Fonction qui permet de choisir le mode de jeu (Att VS Def ou J VS J). Renvoie le booleen AttDef"""
    mode = -1
    while not (mode in [0, 1]):
        print("Modes :")
        print("0 : Attaquant VS Défenseur")
        print("1 : Joueur VS Joueur")
        try:
            mode = int(input())
        except ValueError:
            pass
        print("")
    return not (bool(mode))


def choisir_participants(att_def, liste_d, liste_a):
    """Fonction qui demande le type de joueur à partir du mode de jeu et des liste d'attaquants/défenseurs disponible"""
    if att_def:
        return demander_poste("Defenseur", liste_d), demander_poste("Attaquant", liste_a)
    else:
        return demander_poste("Defenseur 1", liste_d), demander_poste("Attaquant 1", liste_a), \
               demander_poste("Defenseur 2", liste_d), demander_poste("Attaquant 2", liste_a)


def demander_poste(nom_poste, liste):
    """Fonction qui demande le type de joueur à partir de son poste et de la liste des classes disponible"""
    poste = -1
    while not (poste in list(range(len(liste)))):
        print("{} :".format(nom_poste))
        for i in range(len(liste)):
            print("{} : {}".format(i, nom_classe(liste[i])))
        try:
            poste = int(input())
        except ValueError:
            pass
        print("")
    return liste[poste]


def demander_interface():
    """Fonction qui demande si il faut afficher une interface"""
    interface = -1
    while not (interface in [0, 1]):
        print("Interface :")
        print("0 : Non")
        print("1 : Oui")
        try:
            interface = int(input())
        except ValueError:
            pass
        print("")
    return bool(interface)


def tester_liste_joueurs(liste_def, liste_att):
    p = Plateau()
    for i in liste_def:
        if not i(p, p).est_defenseur():
            raise NameError("Erreur, le defenseur {} n'est pas defenseur".format(nom_classe(i)))
    for i in liste_att:
        if not i(p, p).est_attaquant():
            raise NameError("Erreur, l'attaquant {} n'est pas attaquant".format(nom_classe(i)))


def nom_classe(classe):
    """Fonction qui retourne le nom de la classe passée en argument"""
    nom = str(classe)
    if '.' in nom:
        point = nom.index('.')
    else:
        point = 7
    return nom[point + 1:-2]


if __name__ == "__main__":
    main()

#coucou