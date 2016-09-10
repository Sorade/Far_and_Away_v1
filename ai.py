# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 19:25:26 2016

@author: Julien
"""
import pygame
from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt
import random

class ai:
    def __init__(self,game,explorer):
        self.game = game
        self.explorer = explorer
        self.algo = None
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
                var = self.explorer.time_since_last_action
            elif x == 1:
                var = self.explorer.rp
            elif x == 2:
                var = self.explorer.kp
            elif x == 3:
                var = len([1 for log in self.explorer.logbook.itervalues() if log.is_discovered])
                nb_disc = var
            elif x == 4:
                var = len([1 for log in self.explorer.logbook.itervalues() if log.is_explored])
                nb_exp = var
            elif x == 5:
                var = nb_disc - nb_exp
            elif x == 6:
                var = self.game.year
            elif x == 7:
                var = self.explorer.yearly_rp_expense
            elif x == 8:
                var = self.explorer.yearly_rp_income
            elif x == 9:
                var = self.explorer.yearly_kp_income
            elif x ==10:
                var = self.explorer.action
            '''assigns variable'''
            self.variables[x] = var
            
    def print_to_file(self):
        f = open('./ai_training_data/test.csv', 'a')
        string = ''
        for val in self.variables:
            string = string + str(val) + ',' 
        string += '\n'
        f.write(string)
        f.close()
        
    def train(self):
        self.get_variables()
        self.print_to_file()
        
    def play(self):
        '''get action'''
        self.get_variables() #monitors state of game
        action = self.get_action_from_rand_forest() #get's action from state of game
        '''perform action'''
        if action == 1: #visit
            random.choice(self.explorer.explored_planets).visit(self.explorer)
        elif action == 2: #explore
            unexplored_planets = [log.instance[0] for log in self.explorer.logbook.itervalues() if log.is_discovered and not log.is_explored]
            random.choice(unexplored_planets).explore(self.explorer)
        elif action == 3: #search
            self.explorer.logbook[self.explorer.location].instance[0].search_in_SOF(self.explorer, True)
            

    def rand_forest(self):
        #create the training & test sets, skipping the header row with [1:]
        dataset = genfromtxt(open('./ai_training_data/test.csv','r'), delimiter=',', dtype='f8')[1:]    
        target = [x[0] for x in dataset]
        train = [x[1:] for x in dataset]
        
        #create and train the random forest
        #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
        self.algo = RandomForestClassifier(n_estimators=100)
        self.algo.fit(train, target)
    
    def get_action_from_rand_forest(self):
        test = self.variables[1:]
        return self.algo.predict(test)
        #savetxt('Data/submission2.csv', rf.predict(test), delimiter=',', fmt='%f')
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
        
        
             
             
