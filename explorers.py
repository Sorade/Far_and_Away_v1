# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:32:09 2016

@author: julien
"""
import random
from logbook import*

class Explorer(object):
    def __init__(self,game):
        self.game = game
        self.name = random.choice(['Roger','Logan','Fred','Susan','Morgane','Iloa'])
        self.location = 0
        self.logbook = dict(zip((p.name for p in self.game.all_planets),(Logbook(p,False,False) for p in self.game.all_planets)))
    
