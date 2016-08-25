# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 12:07:13 2016

@author: Julien
"""
import functions as fn
import random

class Event_Manager(object):
    def __init__(self,game):
        self.game = game
        self.active_events = []
        self.event_list = None
        
    def all_monthly_events(self,explorer):
        self.game.month += 1 #adds a months of gametime every 10 seconds
        self.get_random_event()
        self.planet_discovery_event(False)
        self.points_adjustement_event()
        self.network_expenses_event()
        for event in self.event_list: event.get_weight(explorer)
        
    def get_random_event(self):
        '''get random event'''
        if random.randint(0,5) == 0: 
            self.active_events.append(fn.choice_weighted(self.event_list))
            self.game.map_active = False
            
        '''removes bonuses'''
        if self.game.player.rp_bonus >= 1: self.game.player.rp_bonus -= 1
        if self.game.player.kp_bonus >= 1: self.game.player.kp_bonus -= 1 
        
    
    def planet_discovery_event(self,player_induced):
        for log in self.game.player.logbook.values():
            log.instance[0].search_in_SOF(self.game.player,False,0)
            
    def resource_prod_event(self):
        for log in self.game.player.logbook.values():
            if log.is_explored:
                self.game.player.rp += fn.rp_formula(log.instance[0],self.game.month,log.time_of_exploration,self.game.player.rp_bonus)
                
    def knowledge_prod_event(self):
        for log in self.game.player.logbook.values():
            if log.is_explored:
                self.game.player.kp += fn.kp_formula(log.instance[0],self.game.month,log.time_of_exploration,self.game.player.kp_bonus)
                
    ''''Make this into a function... maybe store all event values as event manager
    variables and make a new method handling those variables'''   
    def network_expenses_event(self):
        cost = 0
        for log in self.game.player.logbook.values():
            if log.is_explored:
                cost += 1
        self.game.player.rp -= int(cost*1.2)
        self.game.player.monthly_rp_expense = int(cost*1.2) #stores the cost value for the current game state in a variable
        #so that it can be accessed in the graph display
                
    def points_adjustement_event(self):
        self.resource_prod_event()
        self.knowledge_prod_event()
        
        
        
