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
        self.mode_chasse = True """True = on tir au hasard; False = on pêche tant que le bateau visé nest pas coulé """
        self.peche = [] """liste des cibles possibles lorsqu'on est dans le mode peche"""
        self.poisson = [] """ bateau en cours de destruction """
    
    def choisir_cible(self):
        if self.mode_chasse:
            a_tenter = [(i, j) for i in range(10) for j in range(10) if self.plateau_adverse.jamais_vu((i, j))]
        return choice(a_tenter)
        else:
            def update():
                n = len(self.poisson)
                (i,j) = self.poisson[-1] 
                if n == 1:
                    v = [(i-1,j) , (i,j+1) , (i+1,j) , (i,j-1)]
                    for k in range(4):
                        (a,b) = v[k]
                        if (not ( (0 <= a <= 9) and (0 <= b <= 9) )) or (v[k] in self.poisson) :
                            v.pop(k)
                else:
                    if self.poisson[0][0] == self.poisson[1][0]:
                        v = [(i, self.poisson[0][1] - 1),(i, j+1)]
                        for k in range(2):
                            (a,b) = v[k]
                            if (not ( (0 <= a <= 9) and (0 <= b <= 9) )) or (v[k] in self.poisson) :
                                v.pop(k)
                return v
            
            self.peche = update()
            return choice(self.peche)
          
          
    def analyser(self,res,cible):
        if res == 0:
            if not self.mode_chasse :
        if res == 1 :
            self.poisson.append(cible)
            self.poisson.sort()
            self.mode_chasse = False
        if res == 2 :
            self.mode_chasse = True
            self.poisson = []
            self.peche = []
        