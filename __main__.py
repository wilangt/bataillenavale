from humain import *
from hasard import *
from plateau import *
from chasse_peche import *
from ia_sl import *
from random import randint
from time import sleep
import statistics as stats
import pickle as cornichon
import matplotlib.pyplot as plt

print()

types_ia = ["ia_sl_chasse", "ia_sl_peche", "is_sl_tf_chasse", "ia_sl_tf_peche"]
nb_ia = 1
"""Nombre de classe d'IA différentes. A modifier à chaque nouvelle classe créée."""


def main():

    mode = demander_mode()

    if mode == -1:
        # Cas pathologique
        return None

    liste_defenseur = [Humain, HasardDefense, HasardDefenseCornichon, ConfigInit]
    liste_attaquant = [Humain, HasardDebile, HasardMalin, ChasseEtPeche, ChassePecheCroix, ChassePecheCroixProba,
                       ChassePecheProba, ChassePecheProbaCroixDecroissanceLineaire,
                       ChassePecheProbaCroixDecroissanceExpo, IaSl]
    tester_liste_joueurs(liste_defenseur, liste_attaquant)

    att_def = True
    # att_def = choisir_mode()

    if mode == 'Jeu':
        interface = demander_interface()
        classe_participants = choisir_participants(att_def, liste_defenseur, liste_attaquant)
        lancer_partie(classe_participants, att_def, interface)

    elif mode == 'Performances':
        liste_defenseur = liste_defenseur[1:]
        liste_attaquant = liste_attaquant[1:]
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
            print("moyenne : {}, médiane : {}, écart-type : {}".format(round(moy, 2), round(stats.median(l), 2), round(stats.pstdev(l, moy), 2)))
        plt.show()

    elif mode == 'Enregistrer un cornichon':
        cornichon = demander_cornichon()
        liste_defenseur = liste_defenseur[1:]
        if cornichon == 0:
            print("Combien de grilles ?\r")
            iterations = int(input())
            enregistrer_defense_alea(iterations)
        elif cornichon == 1:
            liste_attaquant = liste_attaquant[6:7]
            defenseur, attaquant = choisir_participants(att_def, liste_defenseur, liste_attaquant)
            print("Combien de parties ? (22 grilles environ par partie)\r")
            nb_parties = int(input())
            enregistrer_triplet(defenseur, attaquant, nb_parties, 1)
        elif cornichon == 2:
            liste_attaquant = liste_attaquant[3:4]
            defenseur, attaquant = choisir_participants(att_def, liste_defenseur, liste_attaquant)
            print("Combien de parties ? (18 grilles environ par partie)\r")
            nb_parties = int(input())
            enregistrer_triplet(defenseur, attaquant, nb_parties, 2)

    elif mode == 'Enregistrer une IA':
        dossier = -1
        while not (dossier in list(range(len(types_ia)))):
            print("Quel dossier ?")
            for i in range(len(types_ia)):
                print("{} : {}".format(i, types_ia[i]))
            try:
                dossier = int(input())
            except ValueError:
                pass
            print("")
        dossier = types_ia[dossier]
        liste_ia = os.listdir("ia_enregistrees/{}/".format(dossier))
        nom = liste_ia[0]
        while nom in liste_ia:
            try:
                nom = input('Quel nom ?\n')
            except ValueError:
                pass
            if nom in liste_ia:
                print('Nom déjà pris !\n')
        print("")
        nb_couches = int(input("Combien de couches intermédiaires ?\n"))
        print("Rentrez une à une la taille des couches intermédiaires, en enclenchant à chaque fois la touche entrée")
        couches_intermediaires = []
        for i in range(nb_couches):
            couches_intermediaires.append(int(input()))
        print("")
        creerIA(nom, dossier, couches_intermediaires)

    elif mode == 'Entraîner une IA':
        dossier = -1
        while not (dossier in list(range(len(types_ia)))):
            print("Quel dossier ?")
            for i in range(len(types_ia)):
                print("{} : {}".format(i, types_ia[i]))
            try:
                dossier = int(input())
            except ValueError:
                pass
            print("")
        dossier = types_ia[dossier]
        liste_ia = os.listdir("ia_enregistrees/{}/".format(dossier))
        nom = -1
        while not (nom in list(range(len(liste_ia)))):
            print("Quelle IA ?")
            for i in range(len(liste_ia)):
                print("{} : {}".format(i, liste_ia[i]))
            try:
                nom = int(input())
            except ValueError:
                pass
            print("")
        nom = liste_ia[nom]
        cas_de_base = str(input('Cas de base ? (o/n)\n'))
        if cas_de_base == 'o':
            entrainerIA(nom, dossier)
        else:
            if "chasse" in dossier:
                file = open("donnees/cornichon_chasse.txt", "r")
            elif "peche" in dossier:
                file = open("donnees/cornichon_peche.txt", "r")
            max = int(file.read())
            file.close()
            nb_entrainement = max + 1
            while nb_entrainement > max :
                try:
                    nb_entrainement = int(input("Combien de données d'entraînement ?\n"))
                except ValueError:
                    pass
                if nb_entrainement > max:
                    print('Pas assez de données !\n')
            nb_test = max + 1
            while nb_test > max :
                try:
                    nb_test = int(input('Combien de données de test ?\n'))
                except ValueError:
                    pass
                if nb_entrainement > max:
                    print('Pas assez de données !\n')
            epoque = int(input("Combien d'époques ?\n"))
            taille_mini_nacho = nb_entrainement + 1
            while taille_mini_nacho > nb_entrainement :
                try:
                    taille_mini_nacho = int(input('Quelle taille de mini-batch ?\n'))
                except ValueError:
                    pass
                if taille_mini_nacho > nb_entrainement:
                    print('Pas assez de données !\n')
            eta = float(input("Quelle valeur pour eta ?\n"))
            entrainerIA(nom, dossier, nb_entrainement, nb_test, epoque, taille_mini_nacho, eta)


def lancer_partie(classe_participants, att_def, interface, enregistrer_vecteur=0):
    plateau1 = Plateau()
    plateau2 = Plateau()

    if att_def:
        classe_def, classe_att = classe_participants
        c_p = None
        if type(classe_att) == tuple:
            classe_att, c_p = classe_att
        defenseur, attaquant = classe_def(plateau1, plateau2), classe_att(plateau2, plateau1)
        if c_p is not None:
            attaquant.attribuer_nom(c_p)
        attaquant.enregistrer_vecteur = enregistrer_vecteur

        defenseur.placer_bateaux()

        attaquant.test_initialisation()

        if interface:
            plateau1.init_interface(660)
            plateau1.afficher_interface()

        compteur = 0
        while not (plateau1.defaite()):
            attaquant.attaquer()
            compteur += 1
            if interface:
                sleep(0.5)

        if interface:
            plateau1.cacher_interface()
            pygame.display.quit()
            pygame.quit()

        if not enregistrer_vecteur:
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
    c_p = None
    if type(super_attaquant) == tuple:
        super_attaquant, c_p = super_attaquant
    defenseur, attaquant = super_defenseur(plateau1, plateau2), super_attaquant(plateau2, plateau1)
    if c_p is not None:
        attaquant.attribuer_nom(c_p)
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


def demander_mode():
    """Fonction qui permet de choisir quel mode de traitement on choisit"""
    liste_des_modes = ['Jeu', 'Performances', 'Enregistrer un cornichon', 'Enregistrer une IA', 'Entraîner une IA', 'Mode manuel']
    mode = -1
    n = len(liste_des_modes)
    while not (mode in [x for x in range(n)]):
        print("Modes :")
        for i in range(n) :
            print("{} : ".format(i) + liste_des_modes[i])
        try:
            mode = int(input())
        except ValueError:
            pass
        print("")
    return liste_des_modes[mode]


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
    """Fonction qui demande le type de joueur à partir de son poste et de la liste des classes disponibles"""
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
    if "ia" in nom_classe(liste[poste]):
        return superdemander_ia(poste, liste)
    else:
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
    print("Tapez une classe, faites entrez, et réitérez jusqu'à avoir choisi toutes les classes à comparer. Plusieurs IA du même type peuvent être comparées")
    while compt != nb:
        p = -1
        while not (p in list(range(len(liste)))):
            try:
                p = int(input())
            except ValueError:
                pass
        postes.append(p)
        compt += 1
    print("")
    postes.sort()
    l = []
    for p in postes:
        if p < len(liste) - nb_ia:
            l.append(liste[p])
        else:
            l.append(superdemander_ia(p, liste))
    return l


def superdemander_ia(poste, liste):
    if poste == len(liste) - nb_ia:
        c, p = 0, 1
    else:
        pass
    liste_ia_chasse = os.listdir("ia_enregistrees/{}/".format(types_ia[c]))
    chasse = -2
    while not (chasse in ([-1] + list(range(len(liste_ia_chasse))))):
        print("Quelle IA de chasse ?")
        for i in range(len(liste_ia_chasse)):
            print("{} : {}".format(i, liste_ia_chasse[i]))
        print("-1 : Chasse de ChasseEtPeche")
        try:
            chasse = int(input())
        except ValueError:
            pass
        print("")
    liste_ia_peche = os.listdir("ia_enregistrees/{}/".format(types_ia[p]))
    peche = -2
    while not (peche in ([-1] + list(range(len(liste_ia_peche))))):
        print("Quelle IA de pêche ?")
        for i in range(len(liste_ia_peche)):
            print("{} : {}".format(i, liste_ia_peche[i]))
        print("-1 : Pêche de ChasseEtPeche")
        try:
            peche = int(input())
        except ValueError:
            pass
        print("")
    if chasse == -1:
        chasse = None
    else:
        chasse = liste_ia_chasse[chasse]
    if peche == -1:
        peche = None
    else:
        liste_ia_peche[peche]
    return (liste[poste], (chasse, peche))


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


def demander_cornichon():
    """Fonction qui demande quel cornichon enregistrer"""
    cornichon = -1
    while not (cornichon in [0, 1]):
        print("Type de cornichon :")
        print("0 : Grilles")
        print("1 : Triplet chasse (entrée, sortie, cibles)")
        print("2 : Triplet pêche (entrée, sortie, cibles)")
        try:
            cornichon = int(input())
        except ValueError:
            pass
        print("")
    return cornichon


def tester_liste_joueurs(liste_def, liste_att):
    p = Plateau()
    for i in liste_def:
        if not i(p, p).est_defenseur():
            raise NameError("Erreur, le défenseur {} n'est pas défenseur".format(nom_classe(i)))
    for i in liste_att:
        if not i(p, p).est_attaquant():
            raise NameError("Erreur, l'attaquant {} n'est pas attaquant".format(nom_classe(i)))


def nom_classe(classe):
    """Fonction qui retourne le nom de la classe passée en argument"""
    chasse = ''
    peche = ''
    if type(classe) == tuple:
        classe, (chasse, peche) = classe
        if chasse is not None:
            chasse = ' / Chasse : ' + chasse
        if peche is not None:
            peche = ' / Pêche : ' + peche
    nom = str(classe)
    if '.' in nom:
        point = nom.index('.')
    else:
        point = 7
    return nom[point + 1:-2] + chasse + peche


def enregistrer_defense_alea(iterations):
    file = open("donnees/cornichon_defense.txt", "r")
    debut = int(file.read())
    file.close()
    fin = debut + iterations
    barre = BarreDeProgression()
    for i in range(debut, fin):
        barre.maj(100 * (i - debut + 1) / iterations)
        file = open('donnees/defense-' + str(i), 'wb')
        bateaux = position_bateaux_global()
        cornichon.dump(bateaux, file)
        file.close()
    file = open("donnees/cornichon_defense.txt", "w")
    file.write(str(fin))


def enregistrer_triplet(defenseur, attaquant, nb_parties, indice):
    barre = BarreDeProgression()
    for i in range(nb_parties):
        barre.maj(100 * (i + 1) / nb_parties)
        lancer_partie((defenseur, attaquant), True, False, indice)


def superchoisir_positions_bateaux(super_defenseur, nb_essais):
    plateau1, plateau2 = Plateau(), Plateau()
    defenseur = super_defenseur(plateau1, plateau2)
    return [defenseur.position_bateaux() for _ in range(nb_essais)]


def lancer_entrainement_chasse(resal, n, m, epoque, taille_mini_nacho, eta):
    """
    entraine un résal
    :param resal: résal en question
    :param n: nb entrainement
    :param m: nb test
    :return: None
    """
    donnees_entrainement = []
    donnees_test = []
    file = open("donnees/cornichon_chasse.txt", "r")
    dernier_plus_1 = int(file.read())
    file.close()
    for i in range(n):
        n = randint(0, dernier_plus_1 - 1)
        file = open("donnees/chasse-" + str(n), "rb")
        donnees_entrainement.append(cornichon.load(file))
        file.close()
    for i in range(m):
        n = randint(0, dernier_plus_1 - 1)
        file = open("donnees/chasse-" + str(n), "rb")
        donnees_test.append(cornichon.load(file))
        file.close()
    resal.DGS(donnees_entrainement, epoque, taille_mini_nacho, eta, donnees_test)


def prototype(couches_intermediaires=None, nb_entrainement=5000, nb_test=50, epoque=50, taille_mini_nacho=10, eta=1.):
    """
    permet de tester une configuration d'IA

    :param couches_intermediaires: couches intermédiaires du RN
    :param nb_entrainement: Ok
    :param nb_test: Ok
    :param eta: Ok
    :param taille_mini_nacho: Ok
    :param epoque: Ok
    :return: None
    """
    if couches_intermediaires is None:
        couches_intermediaires = [125]

    resal = Resal([205]+couches_intermediaires+[100])
    lancer_entrainement(resal, nb_entrainement, nb_test, epoque, taille_mini_nacho, eta)


def creerIA(nom, dossier, couches_intermediaires):
    resal = Resal([205] + couches_intermediaires + [100])
    file = open("ia_enregistrees/{}/{}".format(dossier, nom), "wb")
    cornichon.dump(resal, file)
    file.close()


def entrainerIA(nom, dossier, nb_entrainement=5000, nb_test=100, epoque=20, taille_mini_nacho=10, eta=.1):
    file = open("ia_enregistrees/{}/{}".format(dossier, nom), "rb")
    resal = cornichon.load(file)
    file.close()
    lancer_entrainement_chasse(resal, nb_entrainement, nb_test, epoque, taille_mini_nacho, eta)
    file = open("ia_enregistrees/{}/{}".format(dossier, nom), "wb")
    cornichon.dump(resal, file)
    file.close()


if __name__ == "__main__":
    main()
