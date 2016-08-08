# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 12:07:13 2016

@author: Julien
"""


class Event_Manager(object):
    def __init__(self,game):
        self.game = game
    
    def planet_discovery_event(self,player_induced):
        for log in self.game.player.logbook.values():
            log.instance[0].search_in_SOF(self.game.player,False,0)
            
    def resource_prod_event(self):
        for log in self.game.player.logbook.values():
            if log.is_explored:
                self.game.player.rp += log.instance[0].disc_rp/(self.game.month-log.time_of_exploration)
                
    def knowledge_prod_event(self):
        for log in self.game.player.logbook.values():
            if log.is_explored:
                self.game.player.kp += log.instance[0].disc_kp/(self.game.month-log.time_of_exploration)
                
    def network_expenses_event(self):
        cost = 0
        for log in self.game.player.logbook.values():
            if log.is_explored:
                cost += 1
                
        self.game.player.rp -= cost
                
    def points_adjustement_event(self):
        self.resource_prod_event()
        self.knowledge_prod_event()
