import numpy as np

class Plateau:
    """Classe qui permet de connaitre l'état du plateau, et de le modifier au cours de la partie
    L'argument 'bateaux' est une liste de bateaux"""

    def __init__(self, bateaux):
        self.coorBateaux = bateaux
        self.plateau = np.zeros((10,10),dtype=int)
        self.bateaux = [0,2,3,3,4,5]
        self.creerPlateau()
        # exemple de coorBateaux : [[(1,1),(1,2)],[(5,4),(5,5),(5,6)],[(5,9),(6,9),(7,9)],[(6,1),(7,1),(8,1),(9,1)],[(1,5),(1,6),(1,7),(1,8),(1,9)]]

    def creerPlateau(self):
        """initialise le plateau à partir des coordonnées de bateau données à la création du plateau"""
        for k in range(5):
            for coor in self.coorBateaux[k]:
                self.plateau[coor]=(k+1)

    def afficherPlateau(self):
        """Affiche le plateau"""
        print(self.plateau)

    def feu(self, coor):
        """Feu sur une coordonnée"""
        cible = self.plateau[coor]
        if cible==0:
            return 0
        else:
            self.plateau[coor]=0
            self.bateaux[cible] -= 1
            if self.bateaux[cible] == 0:
                return 2
            else:
                return 1

    def defaite(self):
        """Vérifie si il reste des bateaux sur le plateau"""
        return self.bateaux == [0,0,0,0,0,0]
