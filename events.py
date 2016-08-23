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
        self.event_list = [Precious_Ore_Discovered(game),Raiders(game),Old_Archives(game),Storm(game)]
        self.active_events = []
        
    def all_monthly_events(self):
        self.game.month += 1 #adds a months of gametime every 10 seconds
        self.get_random_event()
        self.planet_discovery_event(False)
        self.points_adjustement_event()
        self.network_expenses_event()
        
    def get_random_event(self):
        '''get random event'''
        if random.randint(0,5) == 0: 
            self.active_events.append(fn.choice_weighted(self.game.event_manager.event_list))
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
        self.game.player.rp -= int(cost*1.5)
        self.game.player.monthly_rp_expense = int(cost*1.5) #stores the cost value for the current game state in a variable
        #so that it can be accessed in the graph display
                
    def points_adjustement_event(self):
        self.resource_prod_event()
        self.knowledge_prod_event()
        
        
class Event(object):
    def __init__(self,game, name, weight ,text):
        self.game = game
        self.name = name
        self.weight = weight
        self.text = text
    
class Precious_Ore_Discovered(Event):
    def __init__(self,game):
        self.name = 'Precious Ore Discovered'
        self.weight = 2
        self.text ='''An ore of precious metal has been found in one of your colonies and is being traded throughout the galaxy. It will surely increase our production for a few more years.'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def execute(self):
        self.game.player.rp_bonus += 2

class Raiders(Event):
    def __init__(self,game):
        self.name = 'Raiders'
        self.weight = 1
        self.text ='''Raiders have been reported to disrupt our supply lines and are causing havoc amongst interplanetary trade. This is starting to show in our finances.'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def execute(self):
        self.game.player.rp_bonus += -2
        
class Storm(Event):
    def __init__(self,game):
        self.name = 'Storm'
        self.weight = 2
        self.text ='''An electromagnetic storm has damaged our servers costing us some precious data which we had spend years gathering !!'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def execute(self):
        self.game.player.kp_bonus += -2
        
class Old_Archives(Event):
    def __init__(self,game):
        self.name = 'Old Archives'
        self.weight = 3
        self.text ='''One of your crew librarians has managed to find some long lost archives. They must surely be of interest to us.'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def execute(self):
        self.game.player.kp_bonus += 2
        
