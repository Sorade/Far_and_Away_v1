# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:06:08 2016

@author: julien
"""

class Interface(object):
    def __init__(self,game):
        self.game = game
        self.screen = 'pygame screen'
        
    def view_solarsys(self,offset):
        for p in self.game.all_planets:
            self.screen.blit(p.image,(0,0))
            
    def view_planet(self,planet):
        '''make go_to_button'''
        
        ''' blit all the planet's stats to the screen'''
        self.screen.blit(planet.stats,(0,0))
        
        if go_to_button.selected == True:
            if self.game.player.logbook[planet.name].is_discovered == False:
                planet.explore(self.game.player)
            else:
                planet.visit(self.game.player)
                