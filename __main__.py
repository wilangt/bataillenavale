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
    else:
        classeDef1, classeAtt1, classeDef2, classeAtt2 = classeParticipants
        defenseur1, attaquant1, defenseur2, attaquant2 = classeDef1(), classeAtt1(), classeDef2(), classeAtt2()


    return True

    bateaux = [[(1, 1), (1, 2)], [(5, 4), (5, 5), (5, 6)], [(5, 9), (6, 9), (7, 9)], [(6, 1), (7, 1), (8, 1), (9, 1)],
               [(1, 5), (1, 6), (1, 7), (1, 8), (1, 9)]]
    plateau = Plateau(bateaux)

    LIGHTGREY = (220, 220, 220)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 100)
    RED = (100, 0, 0)
    GREEN = (0, 100, 0)
    DIM = 704
    pas_quad = (DIM) // 11

    background = initFenetre(DIM)

    # Variable qui continue la boucle si = True, stoppe si = False
    continuer = True

    compteur = 0  # Compteur de coups

    # Boucle infinie
    while continuer:
        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == QUIT or plateau.defaite():  # Si un de ces événements est de type QUIT
                if plateau.defaite(): print("Fin de la partie, " + str(compteur) + " coups")
                continuer = False  # On arrête la boucle
                pygame.display.quit()
                pygame.quit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > pas_quad and event.pos[
                0] > pas_quad:
                compteur += 1
                coor = pixToCoor(event.pos[0], event.pos[1], pas_quad)
                if plateau.plateauVisible[coor] != 0:
                    print("boloss")  # Le joueur a deja tiré à cet endroit
                else:
                    res = plateau.feu(coor)
                    if res == 0:
                        print("plouf")
                        dessinerRect(coor, RED, DIM, background)
                    elif res == 1:
                        print("touché")
                        dessinerRect(coor, GREEN, DIM, background)
                    elif res == 2:
                        print("touché coulé")
                        dessinerRect(coor, BLACK, DIM, background)


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
