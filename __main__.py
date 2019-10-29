from classes import *
from fonctions_annexes import *
from interface import *
import pygame
from pygame.locals import *

def main():
    bateaux = [[(1,1),(1,2)],[(5,4),(5,5),(5,6)],[(5,9),(6,9),(7,9)],[(6,1),(7,1),(8,1),(9,1)],[(1,5),(1,6),(1,7),(1,8),(1,9)]]
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
                if plateau.defaite() : print("Fin de la partie, "+str(compteur)+" coups")
                continuer = False  # On arrête la boucle
                pygame.display.quit()
                pygame.quit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > pas_quad and event.pos[
                0] > pas_quad:
                compteur += 1
                coor = pixToCoor(event.pos[0], event.pos[1], pas_quad)
                if plateau.plateauVisible[coor]!=0:
                    print("boloss") # Le joueur a deja tiré à cet endroit
                else :
                    res = plateau.feu(coor)
                    if res == 0 :
                        print("plouf")
                        dessinerRect(coor,RED, DIM, background)
                    elif res ==1 :
                        print("touché")
                        dessinerRect(coor, GREEN, DIM, background)
                    elif res == 2 :
                        print("touché coulé")
                        dessinerRect(coor, BLACK, DIM, background)




if __name__ == "__main__":
    main()
