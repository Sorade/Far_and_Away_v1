# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 19:25:26 2016

@author: Julien
"""

class ai:
    def __init__(self,game,player):
        self.game = game
        self.player = player
        self.variables = [ 'time_since_last_action', 
                         'resource_pts', 'knowledge_pts', 
                         'number_of_discovered_planets', 
                         'number_of_explored_planets',                           
                         'number_of_unexplored_planets',
                         'time_in_game',
                         'current_expenses', 
                         'current_resource_income', 
                         'current_knowledge_income', 
                         'action']
                 
    def get_variables(self):
        nb_disc, nb_exp = 0,0
        for x in range(len(self.variables)):
            '''choices'''
            if x == 0:
                var = self.player.time_since_last_action
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
                var = self.game.year
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
            
    def print_to_file(self):
        pass#print self.variables
        
    def train(self):
        self.get_variables()
        self.print_to_file()

#
#
#variables = [ time_since_last_action, 
#             resource_pts, knowledge_pts, 
#             number_of_discovered_planets, 
#             number_of_explored_planets, 
#             time_in_game, current_expenses, 
#             current_resource_income, 
#             current_knowledge_income, 
#             current_active_events]
#             
#class Analyser():
#    def __init__(self):
#        self.time_since_last = 0
#    
#    def get_variables(self,game,explorer):
#        if pygame.mouse.getpressed() or pygame.keydown(): self.current.time - self.time_since_last
        
        
             
             
