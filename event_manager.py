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
        
    def all_yearly_events(self,explorer):
        self.game.year += 1 #adds a years of gametime every 10 seconds
        self.get_random_event(explorer)
        #self.planet_discovery_event(explorer,False)
        self.points_adjustement_event(explorer)
        for event in self.event_list: event.get_weight(explorer)
        
    def get_random_event(self,explorer):
        '''get random event'''
        if random.randint(0,5) == 0: 
            self.active_events.append(fn.choice_weighted(self.event_list))
            self.game.map_active = False
            
        '''removes bonuses'''
        if explorer.rp_bonus >= 1:
            explorer.rp_bonus -= 1 
        elif  explorer.rp_bonus < 0:
            explorer.rp_bonus += 1
            
        if explorer.kp_bonus >= 1:
            explorer.kp_bonus -= 1 
        elif  explorer.kp_bonus < 0:
            explorer.kp_bonus += 1 
        
    
    def planet_discovery_event(self,explorer,player_induced):
        for log in explorer.logbook.values():
            log.instance[0].search_in_SOF(explorer,False)
            
    def resource_prod_event(self,explorer,year):
        income = 0
        for log in explorer.logbook.values():
            if log.is_explored:
                income += fn.rp_formula(log.instance[0],year,log.time_of_exploration,explorer.rp,explorer.rp_bonus)
        #explorer.rp += explorer.yearly_rp_income
        return income
                
    def knowledge_prod_event(self,explorer,year):
        income = 0
        for log in explorer.logbook.values():
            if log.is_explored:
                income += fn.kp_formula(log.instance[0],year,log.time_of_exploration,explorer.kp,explorer.kp_bonus)
        return income
        
    ''''Make this into a function... maybe store all event values as event manager
    variables and make a new method handling those variables'''   
    def network_expenses_event(self,explorer,year):
        cost = 0
        for log in explorer.logbook.values():
            if log.is_explored and year - log.time_of_exploration <= 100:
                cost += 1
        #explorer.rp -= int(cost)
        #explorer.yearly_rp_expense = int(cost) #stores the cost value for the current game state in a variable
        return cost                                                #so that it can be accessed in the graph display
                
    def points_adjustement_event(self,explorer):
        explorer.yearly_rp_income = self.resource_prod_event(explorer,self.game.year) #assigns yearl_income
        explorer.yearly_rp_expense = self.network_expenses_event(explorer,self.game.year) #assigns yearl_expense
        #update player's rp points
        explorer.rp += explorer.yearly_rp_income - explorer.yearly_rp_expense
        explorer.kp += self.knowledge_prod_event(explorer,self.game.year)
        
        
        
