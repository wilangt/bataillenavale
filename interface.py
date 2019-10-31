import pygame
from pygame.locals import *

def fondEcran(DIM):

    screen = pygame.display.set_mode((DIM, DIM))

    # Arrière plan
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(couleur("bleu"))

    # Quadrillage
    pas_quad = (DIM) // 11
    for i in range(1, 11):
        pygame.draw.line(background, couleur("blanc"), (i * pas_quad, 0), (i * pas_quad, DIM))
        pygame.draw.line(background, couleur("blanc"), (0, i * pas_quad), (DIM, i * pas_quad))

    return background

def initFenetre(DIM):

    WHITE = (255, 255, 255)
    # Initialisation de la bibliothèque Pygame
    pygame.init()

    # Création de la fenêtre
    screen = pygame.display.set_mode((DIM, DIM))
    pygame.display.set_caption('Bataille Navale')

    background = fondEcran(DIM)

    # Blitter le tout dans la fenêtre
    screen.blit(background, (0, 0))
    pygame.display.flip()

    return background


def coorToPix(i,j, pas_quad):
    return ((i+1)*pas_quad+1,(j+1)*pas_quad+1)

def pixToCoor(i,j, pas_quad):
    return (i//pas_quad)-1,(j//pas_quad)-1

def dessinerRect(coor,couleur, DIM, background):
    pas_quad = (DIM) // 11
    screen = pygame.display.set_mode((DIM, DIM))
    i,j = coor
    rect = pygame.Rect(coorToPix(i,j, pas_quad), (pas_quad-1, pas_quad-1))
    pygame.draw.rect(background, couleur, rect)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def couleur(couleur):
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
    else :
        return (0, 0, 0)
