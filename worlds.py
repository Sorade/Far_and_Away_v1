# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 21:54:13 2016

@author: julien
"""
import random
from planets import Planet
import functions as fn

class World_Mining(Planet):
    def __init__(self, game, pos):
        self.img_ref = 'Venus'
        super(type(self), self).__init__(game,pos, self.img_ref)
        self.name = '{}-{}'.format(fn.name_gen(True),str(random.randint(0,100)))
        self.chance_of_discovery = random.randint(0,10)
        self.disc_kp = random.randint(0,3)
        self.disc_rp = random.randint(10,15)
        self.type = 'Mining World'
        
class World_Habitable(Planet):
    def __init__(self, game, pos):
        self.img_ref = 'Earth'
        super(type(self), self).__init__(game,pos, self.img_ref)
        self.name = '{}-{}'.format(fn.name_gen(True),str(random.randint(0,100)))
        self.chance_of_discovery = random.randint(0,15)
        self.disc_kp = random.randint(5,10)
        self.disc_rp = random.randint(10,10)
        self.type = 'Habitable World'
        
class World_Frozen(Planet):
    def __init__(self, game, pos):
        self.img_ref = 'Frozen'
        super(type(self), self).__init__(game,pos, self.img_ref)
        self.name = '{}-{}'.format(fn.name_gen(True),str(random.randint(0,100)))
        self.chance_of_discovery = random.randint(0,15)
        self.disc_kp = random.randint(0,2)
        self.disc_rp = random.randint(0,2)
        self.type = 'Frozen World'
        
        

