# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 21:54:13 2016

@author: julien
"""
import random
from planets import Planet
import functions as fn

class World_Mining(Planet):
    img_ref = 'Venus'
    cat = 'Mining World'
    weight = 7
    def __init__(self, game, pos):
        super(type(self), self).__init__(game,pos, type(self).img_ref)
        self.radius = random.randint(250,350) #SOF
        self.chance_of_discovery = random.randint(0,10)
        self.disc_kp = random.randint(0,3)
        self.disc_rp = random.randint(10,15)
        
class World_Habitable(Planet):
    img_ref = 'Habitable_world'
    cat = 'Habitable World'
    weight = 3
    def __init__(self, game, pos):
        super(type(self), self).__init__(game,pos, type(self).img_ref)
        self.radius = random.randint(250,500) #SOF
        self.chance_of_discovery = random.randint(0,15)
        self.disc_kp = random.randint(5,10)
        self.disc_rp = random.randint(10,10)
        
class World_Frozen(Planet):
    img_ref = 'Frozen'
    cat = 'Frozen World'
    weight = 12
    def __init__(self, game, pos):
        super(type(self), self).__init__(game,pos, type(self).img_ref)
        self.radius = random.randint(500,700) #SOF
        self.chance_of_discovery = random.randint(0,15)
        self.disc_kp = random.randint(0,2)
        self.disc_rp = random.randint(0,2)
        
class World_Alien(Planet):
    img_ref = 'Alien_hive'
    cat = 'Alien World'
    weight = 2
    def __init__(self, game, pos):
        super(type(self), self).__init__(game,pos, type(self).img_ref)
        self.radius = random.randint(250,600) #SOF
        self.chance_of_discovery = random.randint(0,25)
        self.disc_kp = random.randint(20,30)
        self.disc_rp = random.randint(5,10)
        
class World_Jungle(Planet):
    img_ref = 'Jungle'
    cat = 'Jungle World'
    weight = 3
    def __init__(self, game, pos):
        super(type(self), self).__init__(game,pos, type(self).img_ref)
        self.radius = random.randint(350,550) #SOF
        self.chance_of_discovery = random.randint(0,10)
        self.disc_kp = random.randint(10,20)
        self.disc_rp = random.randint(1,10)
        
        

