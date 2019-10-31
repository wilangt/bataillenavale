import numpy as np
import pygame
from pygame.locals import *
pygame.init()


class Plateau:
    """Classe qui permet de connaitre l'état du plateau, et de le modifier au cours de la partie
    L'argument 'bateaux' est une liste de bateaux"""

    def __init__(self):
        self.plateauCache = np.zeros((10, 10), dtype=int)  # Plateau pour l'arbitre (avec toutes les infos)
        self.plateauVisible = np.zeros((10, 10), dtype=int)  # Plateau visible par le joueur
        self.bateaux = [0, 2, 3, 3, 4, 5]
        self.interfaceInit = False
        self.interfaceAffichee = False
        # exemple de coorBateaux :
        # [[(1,1),(1,2)],[(5,4),(5,5),(5,6)],[(5,9),(6,9),(7,9)],[(6,1),(7,1),(8,1),(9,1)],[(1,5),(1,6),(1,7),(1,8),(1,9)]]

    def creerPlateau(self, bateaux):
        """initialise le plateau à partir des coordonnées de bateau données à la création du plateau"""
        for k in range(5):
            for coor in bateaux[k]:
                self.plateauCache[coor] = (k + 1)

    def afficherPlateauCache(self):
        """Affiche le plateau"""
        print(self.plateauCache)

    def afficherPlateauVisible(self):
        """Affiche le plateau"""
        print(self.plateauCache)

    def initInterface(self, dimensionFenetre):
        """Initialise l'interface pygame"""
        # Variables partie interface
        self.dimensionFenetre = dimensionFenetre
        self.pas_quad = (dimensionFenetre) // 11
        self.dimensionFenetre = dimensionFenetre

        # Arrière plan
        background = pygame.Surface((self.dimensionFenetre, self.dimensionFenetre))
        background.fill(couleur("bleu"))

        # Quadrillage
        for i in range(1, 11):
            pygame.draw.line(background, couleur("blanc"), (i * self.pas_quad, 0),
                             (i * self.pas_quad, self.dimensionFenetre))
            pygame.draw.line(background, couleur("blanc"), (0, i * self.pas_quad),
                             (self.dimensionFenetre, i * self.pas_quad))

        self.interface = background
        self.interfaceInit = True

    def afficherInterface(self):
        """affiche interface pygame"""
        if self.interfaceInit and not(self.interfaceAffichee):
            self.screen = pygame.display.set_mode((self.dimensionFenetre, self.dimensionFenetre))
            self.screen.blit(self.interface, (0, 0))
            pygame.display.flip()
            self.interfaceAffichee = True

    def rafraichirInterface(self):
        """rafraichi interface pygame"""
        self.screen.blit(self.interface, (0, 0))
        pygame.display.flip()

    def cacherInterface(self):
        """cache l'interface pygame"""
        if self.interfaceAffichee:
            pygame.display.quit()
            self.interfaceAffichee = False

    def __repr__(self):
        """Affiche le plateau (terminal)"""
        print(self.plateauVisible)
        return ""

    def feu(self, coor):
        """Feu sur une coordonnée"""
        cible = self.plateauCache[coor]
        if cible == 0:
            self.plateauVisible[coor] = -1
            return 0
        else:
            self.plateauCache[coor] = 0
            self.bateaux[cible] -= 1
            if self.bateaux[cible] == 0:
                self.plateauVisible[coor] = 2
                return 2
            else:
                self.plateauVisible[coor] = 1
                return 1

    def defaite(self):
        """Vérifie si il reste des bateaux sur le plateau"""
        return self.bateaux == [0, 0, 0, 0, 0, 0]

def coorToPix(i, j, pas_quad):
    """Fonction qui transforme une coordonnée BN en coordonnée pixel (seulement l'interieur des cases)"""
    return (i + 1) * pas_quad + 1, (j + 1) * pas_quad + 1


def pixToCoor(i, j, pas_quad):
    """Fonction qui transforme une coordonnée pixel en coordonnée BN"""
    return (i // pas_quad) - 1, (j // pas_quad) - 1


def dessinerRect(coor, couleur, DIM, background):
    """Fonction qui dessine un rectangle"""
    pas_quad = (DIM) // 11
    screen = pygame.display.set_mode((DIM, DIM))
    i, j = coor
    rect = pygame.Rect(coorToPix(i, j, pas_quad), (pas_quad - 1, pas_quad - 1))
    pygame.draw.rect(background, couleur, rect)
    screen.blit(background, (0, 0))
    pygame.display.flip()


def couleur(couleur):
    """Fonction qui renvoie le 3-uplet RGB d'une couleur passée en argument"""
    if couleur == "blanc":
        return (255, 255, 255)
    elif couleur == "noir":
        return (0, 0, 0)
    elif couleur == "bleu":
        return (0, 0, 100)
    elif couleur == "rouge":
        return (100, 0, 0)
    elif couleur == "vert":
        return (0, 100, 0)
    else:
        return (0, 0, 0)
