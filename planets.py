# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 18:38:25 2016

@author: Julien
"""
import random

class Planet(object):
    def __init__(self, game, pos):
        self.game = game
        self.name = 'X'+random.randint(0,1000)+random.randint(0,1000)+random.randint(0,1000)
        self.pos = pos
        self.discovered_by = []
        self.radius_of_influence = random.randint(5,50)
        self.disc_kp = random.randint(10,100)
        self.disc_rp = random.randint(10,100)
        
    def unveil(self,explorer,player_induced):
        explorer.logbook[self.name].is_known = True
        if player_induced == True:
            explorer.kp -= 5
        
    def explore(self, explorer):
        explorer.logbook[self.name].is_discovered = True
        explorer.logbook[self.name].discovery_time = self.game.gametime.get_tick()
                