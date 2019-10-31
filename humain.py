from plateau import *


class Humain:
    def __init__(self):
        self.type = "humain"

    def placerBateaux(self):
        """Place les bateaux"""
        return [[(1, 1), (1, 2)], [(5, 4), (5, 5), (5, 6)], [(5, 9), (6, 9), (7, 9)], [(6, 1), (7, 1), (8, 1), (9, 1)],
                [(1, 5), (1, 6), (1, 7), (1, 8), (1, 9)]]

    def attaquer(self, plateauAllie, plateauAdverse):
        """Attaque la flotte adverse. Renvoie une coordonnée"""
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
