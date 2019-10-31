import numpy as np
from interface import *


class Plateau:
    """Classe qui permet de connaitre l'état du plateau, et de le modifier au cours de la partie
    L'argument 'bateaux' est une liste de bateaux"""

    def __init__(self):
        # Partie Jeu
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
        if self.interfaceInit and not(self.interfaceAffichee):
            self.screen = pygame.display.set_mode((self.dimensionFenetre, self.dimensionFenetre))
            self.screen.blit(self.interface, (0, 0))
            pygame.display.flip()
            self.interfaceAffichee = True

    def rafraichirInterface(self):
        self.screen.blit(self.interface, (0, 0))
        pygame.display.flip()

    def cacherInterface(self):
        if self.interfaceAffichee:
            pygame.display.quit()
            self.interfaceAffichee = False

    def __repr__(self):
        """Affiche le plateau"""
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

class Humain:
    def __init__(self):
        self.type = "humain"

    def placerBateaux(self):
        return [[(1,1),(1,2)],[(5,4),(5,5),(5,6)],[(5,9),(6,9),(7,9)],[(6,1),(7,1),(8,1),(9,1)],[(1,5),(1,6),(1,7),(1,8),(1,9)]]

    def attaquer(self,plateauAllie, plateauAdverse):
        pas_quad = plateauAdverse.pas_quad
        dimensionFenetre = plateauAdverse.dimensionFenetre
        background = plateauAdverse.interface
        plateauAdverse.afficherInterface()
        continuer = True
        pygame.event.clear()
        while continuer:
            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if event.type == QUIT:  # Si un de ces événements est de type QUIT
                    continuer = False  # On arrête la boucle
                    pygame.display.quit()
                    pygame.quit()
                    raise NameError("Abandon")

                if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > pas_quad and event.pos[
                    0] > pas_quad:
                    coor = pixToCoor(event.pos[0], event.pos[1], pas_quad)
                    if plateauAdverse.plateauVisible[coor] != 0:
                        print("boloss")  # Le joueur a deja tiré à cet endroit
                    else:
                        res = plateauAdverse.feu(coor)
                        if res == 0:
                            print("plouf")
                            dessinerRect(coor, couleur("rouge"), dimensionFenetre, background)
                        elif res == 1:
                            print("touché")
                            dessinerRect(coor, couleur("vert"), dimensionFenetre, background)
                        elif res == 2:
                            print("touché coulé")
                            dessinerRect(coor, couleur("noir"), dimensionFenetre, background)
                    continuer = False
