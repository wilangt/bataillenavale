from plateau import *
from joueur import *
from pygame.locals import *
from joueur import *
from random import randint
from random import choice
from fonctions_annexes import test_bateaux


class Chasse_et_peche(Joueur):
    def __init__(self, plateau_allie, plateau_adverse):
        Joueur.__init__(self, plateau_allie, plateau_adverse)
        self.attaquant = True
        self.defenseur = False
        self.mode_chasse = True  # True = on tir au hasard; False = on pêche tant que le bateau visé nest pas coulé
        self.chasse = [(i, j) for i in range(10) for j in range(10)] # liste des cibles possibles lorsqu'on est dans le mode chasse
        self.poisson = []   # bateau en cours de destruction
    
    def choisir_cible_chasse(self):
        return choice(self.chasse)
    
    def choisir_cible_peche(self):
        n = len(self.poisson)
        (i, j) = self.poisson[-1]
        if n == 1:
            v = [(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)]
            k = 3
            while k >= 0:
                (a, b) = v[k]
                if (not ((0 <= a <= 9) and (0 <= b <= 9))):
                    v.pop(k)
                k -= 1
        else:
            if self.poisson[0][0] == self.poisson[1][0]:
                v = [(i, self.poisson[0][1] - 1), (i, j + 1)]
            else:
                v = [(self.poisson[0][0] - 1, j), (i + 1, j)]
            k = 1
            while k >= 0:
                (a, b) = v[k]
                if (not ((0 <= a <= 9) and (0 <= b <= 9))) or (v[k] not in self.chasse):
                    v.pop(k)
                k -= 1
        return choice(v)
        
    def choisir_cible(self):
        if self.mode_chasse:
            return self.choisir_cible_chasse()
        else:
            return self.choisir_cible_peche()
                
    def analyser(self, res, cible):
        if cible in self.chasse:
            self.chasse.pop(self.chasse.index(cible))
        if res == 1:
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = False
        if res == 2:
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = True
            (i,j) , (k,l) = self.poisson[0] , self.poisson[-1]
            for a in range(i-1,k+2):
                for b in range(j-1,l+2):
                    if (a,b) in self.chasse:
                        self.chasse.pop(self.chasse.index((a,b)))
            self.poisson = []
            self.peche = []
