from classes import *
from fonctions_annexes import *
from interface import *
import pygame
from pygame.locals import *
print()

def main():

    listeDefenseur = [Humain]
    listeAttaquant = [Humain]

    attDef = choisirMode()
    classeParticipants = choisirParticipants(attDef, listeDefenseur, listeAttaquant)

    if attDef:
        classeDef, classeAtt = classeParticipants
        defenseur, attaquant = classeDef(), classeAtt()
        plateau = Plateau()
        plateauFantome = Plateau()
        plateau.creerPlateau(defenseur.placerBateaux())
        plateau.initInterface(500)

        plateau.afficherInterface()
        compteur = 0
        while not(plateau.defaite()):
            attaquant.attaquer(plateauFantome, plateau)
            compteur +=1

        plateau.cacherInterface()
        pygame.display.quit()
        pygame.quit()
        print("Partie terminée en {} coups".format(compteur))

    else:
        classeDef1, classeAtt1, classeDef2, classeAtt2 = classeParticipants
        defenseur1, attaquant1, defenseur2, attaquant2 = classeDef1(), classeAtt1(), classeDef2(), classeAtt2()




def choisirMode():
    mode = -1
    while not (mode in [0, 1]):
        print("Modes :")
        print("0 : Attaquant VS Défenseur")
        print("1 : Joueur VS Joueur")
        try : mode = int(input())
        except : pass
        print("")
    return not (bool(mode))


def choisirParticipants(attDef, listeD, listeA):
    if attDef:
        return demanderPoste("Defenseur", listeD), demanderPoste("Attaquant", listeA)
    else:
        return demanderPoste("Defenseur 1", listeD), demanderPoste("Attaquant 1", listeA), \
               demanderPoste("Defenseur 2", listeD), demanderPoste("Attaquant 2", listeA)


def demanderPoste(nomPoste, liste):
    poste = -1
    while not (poste in list(range(len(liste)))):
        print("{} :".format(nomPoste))
        for i in range(len(liste)):
            print("{} : {}".format(i, nomClasse(liste[i])))
        try:
            poste = int(input())
        except:
            pass
        print("")
    return liste[poste]

def nomClasse(classe):
    nom = str(classe)
    if '.' in nom: point = nom.index('.')
    else: point = 7
    return nom[point+1:-2]

if __name__ == "__main__":
    main()
