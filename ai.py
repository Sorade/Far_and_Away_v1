# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 19:25:26 2016

@author: Julien
"""


variables = [ time_since_last_action, 
             resource_pts, knowledge_pts, 
             number_of_discovered_planets, 
             number_of_explored_planets, 
             time_in_game, current_expenses, 
             current_resource_income, 
             current_knowledge_income, 
             current_active_events]
             
class Analyser():
    def __init__(self):
        self.time_since_last = 0
    
    def get_variables(self,game,explorer):
        if pygame.mouse.getpressed() or pygame.keydown(): self.current.time - self.time_since_last
        
        
             
             
