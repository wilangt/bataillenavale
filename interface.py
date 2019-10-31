import pygame
from pygame.locals import *

pygame.init()


def coorToPix(i, j, pas_quad):
    return (i + 1) * pas_quad + 1, (j + 1) * pas_quad + 1


def pixToCoor(i, j, pas_quad):
    return (i // pas_quad) - 1, (j // pas_quad) - 1


def dessinerRect(coor, couleur, DIM, background):
    pas_quad = (DIM) // 11
    screen = pygame.display.set_mode((DIM, DIM))
    i, j = coor
    rect = pygame.Rect(coorToPix(i, j, pas_quad), (pas_quad - 1, pas_quad - 1))
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
    else:
        return (0, 0, 0)
