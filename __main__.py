from humain import *
from hasard import *
from plateau import *
from chasse_peche import *
from time import sleep
import statistics as stats
import pickle as cornichon
import matplotlib.pyplot as plt

print()


def main():
    liste_defenseur = [Humain, HasardDefense, HasardDefenseCornichon, ConfigInit]
    liste_attaquant = [Humain, HasardDebile, HasardMalin, ChasseEtPeche, ChassePecheCroix, ChassePecheCroixProba,
                       ChassePecheProba, ChassePecheProbaCroixDecroissanceLineaire,
                       ChassePecheProbaCroixDecroissanceExpo]
    tester_liste_joueurs(liste_defenseur, liste_attaquant)

    att_def = True
    # att_def = choisir_mode()

    perf = performances()
    if not perf:
        interface = demander_interface()
    else:
        interface = False

    if not interface:
        liste_defenseur = liste_defenseur[1:]
        liste_attaquant = liste_attaquant[1:]

    classe_participants = choisir_participants(att_def, liste_defenseur, liste_attaquant)

    if perf:
        nb_essais = int(input("Nombre d'essais : "))
        l = []
        p = 0
        for i in range(nb_essais):
            l.append(lancer_partie(classe_participants, att_def, interface, perf))
            v = int(p * nb_essais / 100)
            if i == v:
                print("{}%".format(p))
                p += 1

        moy = stats.mean(l)
        print(nom_classe(classe_participants[1]), " :")
        print("moyenne : {}, médiane : {}, écart-type : {} ({} essais)".format(moy, stats.median(l),
                                                                               stats.pstdev(l, moy), nb_essais))
        plt.hist(l, range=(1, 100), bins=99)
        plt.show()
    else:
        lancer_partie(classe_participants, att_def, interface, perf)


def lancer_partie(classe_participants, att_def, interface, perf):
    plateau1 = Plateau()
    plateau2 = Plateau()

    if att_def:
        classe_def, classe_att = classe_participants
        defenseur, attaquant = classe_def(plateau1, plateau2), classe_att(plateau2, plateau1)

        defenseur.placer_bateaux()

        if interface:
            plateau1.init_interface(660)
            plateau1.afficher_interface()

        compteur = 0
        while not (plateau1.defaite()):
            attaquant.attaquer()
            compteur += 1
            if interface:
                if not perf:
                    sleep(0.1)

        if interface:
            plateau1.cacher_interface()
            pygame.display.quit()
            pygame.quit()

        if not perf:
            print("Partie terminée en {} coups".format(compteur))
        return compteur
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


def performances():
    """Fonction qui permet de choisir si on test les perfs des algorithmes"""
    mode = -1
    while not (mode in [0, 1]):
        print("Modes :")
        print("0 : performances")
        print("1 : Jeu")
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


def enregistrer_defense_alea(iterations):
    file = open("donnees/meta_cornichon.txt", "r")
    debut = int(file.read())
    file.close()
    fin = debut + iterations
    for i in range(debut, fin):
        file = open('donnees/defense-' + str(i), 'wb')
        bateaux = position_bateaux_global()
        cornichon.dump(bateaux, file)
        file.close()
    file = open("donnees/meta_cornichon.txt", "w")
    file.write(str(fin))


if __name__ == "__main__":
    # main()
    pass
