from humain import *
from hasard import *
from plateau import *
from time import sleep

print()


def main():
    liste_defenseur = [Humain]
    liste_attaquant = [Humain, HasardDebile, HasardMalin]

    att_def = choisir_mode()
    classe_participants = choisir_participants(att_def, liste_defenseur, liste_attaquant)

    plateau1 = Plateau()
    plateau2 = Plateau()

    if att_def:
        classe_def, classe_att = classe_participants
        defenseur, attaquant = classe_def(plateau1, plateau2), classe_att(plateau2, plateau1)

        if defenseur.est_defenseur():
            defenseur.placer_bateaux()
        else:
            raise NameError("Erreur, le défenseur n'est pas défenseur")

        plateau1.init_interface(500)
        plateau1.afficher_interface()

        compteur = 0
        while not (plateau1.defaite()):
            attaquant.attaquer()
            compteur += 1
            sleep(0.01)

        plateau1.cacher_interface()
        pygame.display.quit()
        pygame.quit()
        print("Partie terminée en {} coups".format(compteur))

    else:
        classe_def1, classe_att1, classe_def2, classe_att2 = classe_participants
        defenseur1, attaquant1, defenseur2, attaquant2 = classe_def1(), classe_att1(), classe_def2(), classe_att2()
        # Attention, format de classe pas a jour : il manque les plateaux


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
