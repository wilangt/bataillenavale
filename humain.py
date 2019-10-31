from plateau import *
from joueur import *
from pygame.locals import *


class Humain(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True
        self.defenseur = True

    def position_bateaux(self):
        pass

    def choisir_cible(self):
        pas_quad = self.plateau_adverse.get_pas_quad()
        self.plateau_adverse.afficher_interface()
        continuer = True
        pygame.event.clear()
        while continuer:
            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if event.type == QUIT:  # Si un de ces événements est de type QUIT
                    pygame.display.quit()
                    pygame.quit()
                    raise NameError("Abandon")

                if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > pas_quad and event.pos[
                        0] > pas_quad:
                    return pix_to_coor(event.pos[0], event.pos[1], pas_quad)

    def analyser(self, res):
        if res == 0:
            print("plouf")
        elif res == 1:
            print("touché")
        elif res == 2:
            print("touché coulé")

class ConfigInit(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = False
        self.defenseur = True

    def position_bateaux(self):
        return [[(1, 1), (1, 2)], [(5, 4), (5, 5), (5, 6)], [(5, 9), (6, 9), (7, 9)], [(6, 1), (7, 1), (8, 1), (9, 1)],
                [(1, 5), (1, 6), (1, 7), (1, 8), (1, 9)]]
