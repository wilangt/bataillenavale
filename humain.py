from plateau import *
from joueur import *
from pygame.locals import *


class Humain(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True
        self.defenseur = True

    def position_bateaux(self):
        self.plateau_allie.init_interface(500)
        self.plateau_allie.afficher_interface()
        pas_quad = self.plateau_allie.get_pas_quad()
        continuer = True
        pygame.event.clear()

        liste_bateaux = [[], [], [], [], []]
        taille_bateaux = [2, 3, 3, 4, 5]
        bateau_actuel = 0
        compteur = 0

        while continuer:
            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if event.type == QUIT:  # Si un de ces événements est de type QUIT
                    pygame.display.quit()
                    pygame.quit()
                    raise NameError("Abandon")

                if event.type == MOUSEBUTTONDOWN and event.button == 1 and event.pos[1] > pas_quad and event.pos[
                        0] > pas_quad:
                    coor = pix_to_coor(event.pos[0], event.pos[1], pas_quad)
                    liste_bateaux[bateau_actuel].append(coor)
                    self.plateau_allie.afficher_rectangle(coor, "blanc")
                    compteur += 1
                    if compteur >= taille_bateaux[bateau_actuel]:
                        compteur = 0
                        bateau_actuel += 1
                    if bateau_actuel >= 5:
                        continuer = False
                        self.plateau_allie.cacher_interface()
                    print(liste_bateaux)
        return liste_bateaux

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
