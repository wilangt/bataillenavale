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
    superperf = superperformances()
    if not perf or not superperf:
        interface = demander_interface()
    else:
        interface = False

    if not interface:
        liste_defenseur = liste_defenseur[1:]
        liste_attaquant = liste_attaquant[1:]

    if not superperf:
        classe_participants = choisir_participants(att_def, liste_defenseur, liste_attaquant)

        if perf:
            nb_essais = int(input("Nombre d'essais : "))
            l, Y = [], [0 for x in range(100)]
            p, val = 0, 0
            for i in range(nb_essais):
                val = lancer_partie(classe_participants, att_def, interface, perf)
                l.append(val)
                Y[val] += 1
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

    else:
        super_defenseur, super_attaquants = superchoisir_participants(liste_defenseur, liste_attaquant)
        nb_classes = len(super_attaquants)
        nb_essais = int(input("Nombre d'essais : "))
        superpositions_bateaux = superchoisir_positions_bateaux(super_defenseur, nb_essais)
        superl = []
        p = 0
        barre = BarreDeProgression(titre='Sabordage en cours...')
        fig = plt.figure()
        fig.suptitle('Comparaison des performances des algorithmes pour {} essais'.format(nb_essais), fontsize=14,
                     fontweight='bold')
        ax1, ax2 = plt.subplot(121), plt.subplot(122)
        for i in range(nb_classes):
            l, Y, Ycumul = [], [0 for x in range(101)], [0 for x in range(101)]
            val = 0
            for j in range(nb_essais):
                val = superlancer_partie(super_defenseur, super_attaquants[i], superpositions_bateaux[j])
                if val > 100:
                    val = 100
                l.append(val)
                Y[val] += 1
                for k in range(val, 101):
                    Ycumul[k] += 1
                v = int(p * nb_essais * nb_classes / 100) - i * nb_essais
                if j == v:
                    p += 1
                    barre.maj(p)
            superl.append(l)
            ax1.plot([x for x in range(101)], Y, label=nom_classe(super_attaquants[i]))
            ax2.plot([x for x in range(101)], Ycumul, label=nom_classe(super_attaquants[i]))
        ax1.set_xlabel("Nombre de coups nécessaires pour gagner")
        ax1.set_ylabel("Nombre de parties")
        ax1.legend()
        ax2.set_xlabel("Nombre de coups nécessaires pour gagner")
        ax2.set_ylabel("Nombre de parties cumulées")
        ax2.legend()
        print("\nNombre d'essais : {}".format(nb_essais))
        for i in range(len(super_attaquants)):
            l = superl[i]
            moy = stats.mean(l)
            print(nom_classe(super_attaquants[i]), " :")
            print("moyenne : {}, médiane : {}, écart-type : {}".format(round(moy,2), round(stats.median(l),2),
                                                                                   round(stats.pstdev(l, moy),2)))
        plt.show()


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


def superlancer_partie(super_defenseur, super_attaquant, superposition_bateaux):
    plateau1 = Plateau()
    plateau2 = Plateau()
    defenseur, attaquant = super_defenseur(plateau1, plateau2), super_attaquant(plateau2, plateau1)
    defenseur.plateau_allie.placer_bateaux(superposition_bateaux)
    compteur = 0
    while not (plateau1.defaite()):
        attaquant.attaquer()
        compteur += 1
    return compteur


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
    """Fonction qui permet de choisir si on test les performances des algorithmes"""
    mode = -1
    while not (mode in [0, 1]):
        print("Modes :")
        print("0 : Performances")
        print("1 : Jeu")
        try:
            mode = int(input())
        except ValueError:
            pass
        print("")
    return not (bool(mode))


def superperformances():
    """Fonction qui permet de choisir si on teste les perf sur un ou plusieurs algorithmes"""
    mode = -1
    while not (mode in [0, 1]):
        print("Modes :")
        print("0 : Performances")
        print("1 : Superperformances")
        try:
            mode = int(input())
        except ValueError:
            pass
        print("")
    return bool(mode)


def choisir_participants(att_def, liste_d, liste_a):
    """Fonction qui demande le type de joueur à partir du mode de jeu et des liste d'attaquants/défenseurs disponible"""
    if att_def:
        return demander_poste("Defenseur", liste_d), demander_poste("Attaquant", liste_a)
    else:
        return demander_poste("Defenseur 1", liste_d), demander_poste("Attaquant 1", liste_a), \
               demander_poste("Defenseur 2", liste_d), demander_poste("Attaquant 2", liste_a)


def superchoisir_participants(liste_d, liste_a):
    """Fonction qui demande une liste de joueurs"""
    return demander_poste("Defenseur", liste_d), superdemander_postes("Attaquants", liste_a)


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


def superdemander_postes(nom_poste, liste):
    """Fonction qui demande une liste de types de joueur"""
    postes = []
    compt = 0
    print("{} :".format(nom_poste))
    for i in range(len(liste)):
        print("{} : {}".format(i, nom_classe(liste[i])))
    print("")
    print("Combien de classes souhaitez-vous comparer ?")
    nb = int(input())
    print("")
    print("Tapez une classe, faites entrez, et réitérez jusqu'à avoir choisi toutes les classes à comparer.")
    while compt != nb:
        p = -1
        while not (p in list(range(len(liste)))):
            try:
                p = int(input())
            except ValueError:
                pass
        if p not in postes:
            postes.append(p)
            compt += 1
    print("")
    postes.sort()
    return [liste[p] for p in postes]


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
    barre = BarreDeProgression()
    for i in range(debut, fin):
        barre.maj(100*(i-debut+1)/iterations)
        file = open('donnees/defense-' + str(i), 'wb')
        bateaux = position_bateaux_global()
        cornichon.dump(bateaux, file)
        file.close()
    file = open("donnees/meta_cornichon.txt", "w")
    file.write(str(fin))


def superchoisir_positions_bateaux(super_defenseur, nb_essais):
    plateau1, plateau2 = Plateau(), Plateau()
    defenseur = super_defenseur(plateau1, plateau2)
    return [defenseur.position_bateaux() for _ in range(nb_essais)]


if __name__ == "__main__":
    main()
    # enregistrer_defense_alea(10000)
