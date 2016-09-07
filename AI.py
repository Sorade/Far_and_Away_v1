# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 17:29:21 2016

@author: julien
"""

class AI:
    def __init__(self,game,player):
        self.game = game
        self.player = player
        self.variables = [ time_since_last_action, 
                         resource_pts, knowledge_pts, 
                         number_of_discovered_planets, 
                         number_of_explored_planets,                           
                         number_of_unexplored_planets,
                         time_in_game, current_expenses, 
                         current_resource_income, 
                         current_knowledge_income, 
                         action]
                 
    def get_variables(self):
        nb_disc, nb_exp = 0,0
        for x in range(len(self.variables)):
            '''choices'''
            if x == 0:
                var = self.player.time_since_last_action,
            elif x == 1:
                var = self.player.rp
            elif x == 2:
                var = self.player.kp
            elif x == 3:
                var = len([1 for log in self.player.logbook.itervalues() if log.is_discovered])
                nb_disc = var
            elif x == 4:
                var = len([1 for log in self.player.logbook.itervalues() if log.is_explored])
                nb_exp = var
            elif x == 5:
                var = nb_disc - nb_exp
            elif x == 6:
                var = self.game.month
            elif x == 7:
                var = self.player.yearly_rp_expense
            elif x == 8:
                var = self.player.yearly_rp_income
            elif x == 9:
                var = self.player.yearly_kp_income
            elif x ==10:
                var = self.player.action
            '''assigns variable'''
            self.variables[x] = var
            '''print to file ...'''
                 
                 
''' in explorer.py'''
def set_time_since_last_action(self):
    self.time_since_last_action = current_time - self.time_since_last_action
    
def set_action(self,action):
    actions = {'nothing' : 0, 'visit' : 1, 'explore' : 2, 'search' : 3}
    self.action = actions[action]
    
    
    

