import numpy as np
import pygame

pygame.init()


class Plateau:
    """Classe qui permet de connaitre l'état du plateau, et de le modifier au cours de la partie"""

    def __init__(self):
        self.plateauCache = np.zeros((10, 10), dtype=int)  # Plateau pour l'arbitre (avec toutes les infos)
        self.plateauVisible = np.zeros((10, 10), dtype=int)  # Plateau visible par le joueur
        self.bateaux = [0, 2, 3, 3, 4, 5]
        self.interfaceInit = False
        self.interfaceAffichee = False
        self.dimension_fenetre = 0
        self.interface = None
        # exemple de coorBateaux :
        # [[(1,1),(1,2)],[(5,4),(5,5),(5,6)],[(5,9),(6,9),(7,9)],[(6,1),(7,1),(8,1),(9,1)],[(1,5),(1,6),(1,7),(1,8),(1,9)]]

    def placer_bateaux(self, bateaux):
        """initialise le plateau à partir des coordonnées de bateau données à la création du plateau"""
        for k in range(5):
            for coor in bateaux[k]:
                self.plateauCache[coor] = (k + 1)

    def afficher_plateau_cache(self):
        """Affiche le plateau"""
        print(self.plateauCache)

    def afficher_plateau_visible(self):
        """Affiche le plateau"""
        print(self.plateauCache)

    def init_interface(self, dimension_fenetre):
        """Initialise l'interface pygame"""
        # Variables partie interface
        self.dimension_fenetre = dimension_fenetre
        pas_quad = self.get_pas_quad()

        # Arrière plan
        background = pygame.Surface((self.dimension_fenetre, self.dimension_fenetre))
        background.fill(couleur_rgb("bleu"))

        # Quadrillage
        for i in range(1, 11):
            pygame.draw.line(background, couleur_rgb("blanc"), (i * pas_quad, 0),
                             (i * pas_quad, self.dimension_fenetre))
            pygame.draw.line(background, couleur_rgb("blanc"), (0, i * pas_quad),
                             (self.dimension_fenetre, i * pas_quad))

        self.interface = background
        self.interfaceInit = True

    def afficher_interface(self):
        """affiche interface pygame"""
        if self.interfaceInit and not self.interfaceAffichee:
            screen = pygame.display.set_mode((self.dimension_fenetre, self.dimension_fenetre))
            screen.blit(self.interface, (0, 0))
            pygame.display.flip()
            self.interfaceAffichee = True

    def rafraichir_interface(self):
        """rafraichi interface pygame"""
        screen = pygame.display.set_mode((self.dimension_fenetre, self.dimension_fenetre))
        screen.blit(self.interface, (0, 0))
        pygame.display.flip()

    def cacher_interface(self):
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
            self.afficher_rectangle(coor, "rouge")
            self.plateauVisible[coor] = -1
            return 0
        else:
            self.plateauCache[coor] = 0
            self.bateaux[cible] -= 1
            if self.bateaux[cible] == 0:
                self.afficher_rectangle(coor, "noir")
                self.plateauVisible[coor] = 2
                return 2
            else:
                self.afficher_rectangle(coor, "vert")
                self.plateauVisible[coor] = 1
                return 1

    def afficher_rectangle(self, coor, couleur):
        if self.interfaceInit and self.plateauVisible[coor] == 0:
            dessiner_rect(coor, couleur_rgb(couleur), self.get_pas_quad(), self.interface)
            if self.interfaceAffichee:
                screen = pygame.display.set_mode((self.dimension_fenetre, self.dimension_fenetre))
                screen.blit(self.interface, (0, 0))
                pygame.display.flip()

    def defaite(self):
        """Vérifie si il reste des bateaux sur le plateau"""
        return self.bateaux == [0, 0, 0, 0, 0, 0]

    def get_dimension_fenetre(self):
        return self.dimension_fenetre

    def get_pas_quad(self):
        return self.dimension_fenetre // 11

    def jamais_vu(self, coor):
        return self.plateauVisible[coor] == 0


def coor_to_pix(i, j, pas_quad):
    """Fonction qui transforme une coordonnée BN en coordonnée pixel (seulement l'interieur des cases)"""
    return (i + 1) * pas_quad + 1, (j + 1) * pas_quad + 1


def pix_to_coor(i, j, pas_quad):
    """Fonction qui transforme une coordonnée pixel en coordonnée BN"""
    return (i // pas_quad) - 1, (j // pas_quad) - 1


def dessiner_rect(coor, couleur, pas_quad, background):
    """Fonction qui dessine un rectangle"""
    # screen = pygame.display.set_mode((dim, dim))
    i, j = coor
    rect = pygame.Rect(coor_to_pix(i, j, pas_quad), (pas_quad - 1, pas_quad - 1))
    pygame.draw.rect(background, couleur, rect)
    # screen.blit(background, (0, 0))
    # pygame.display.flip()


def couleur_rgb(couleur):
    """Fonction qui renvoie le 3-uplet RGB d'une couleur passée en argument"""
    if couleur == "blanc":
        return 255, 255, 255
    elif couleur == "noir":
        return 0, 0, 0
    elif couleur == "bleu":
        return 0, 0, 100
    elif couleur == "rouge":
        return 100, 0, 0
    elif couleur == "vert":
        return 0, 100, 0
    else:
        return 0, 0, 0