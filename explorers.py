# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:32:09 2016

@author: julien
"""
from logbook import*

class Explorer(object):
    def __init__(self,game):
        self.game = game
        self.location = 0
        self.logbook = dict(zip((p.name for p in self.game.all_planets),(Logbook(p,True,True) for p in self.game.all_planets)))
    
