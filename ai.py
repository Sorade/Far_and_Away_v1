# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 19:25:26 2016

@author: Julien
"""
import pygame
from sklearn.ensemble import RandomForestClassifier
from numpy import genfromtxt, savetxt
import random
import pathfinding as pth

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
                         'ratio_disc_to_pop', 
                         'ratio_exp_to_disc',
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
            elif x ==12:
                var = self.explorer.action
            elif x == 10:
                ratios = self.explorer.get_planet_ratio_at_loc() #returns a tuple
                var = ratios[0]
                self.variables[x+1] = ratios[1]
            '''assigns variable'''
            self.variables[x] = var
            
#    def print_to_file(self):
#        f = open('./ai_training_data/test.csv', 'a')
#        string = ''
#        for val in self.variables:
#            string = string + str(val) + ',' 
#        string = string[:-1]    
#        string += '\n'
#        f.write(string)
#        f.close()
        
#    def train(self):
#        self.get_variables()
#        self.print_to_file()
        
    def get_planet_with_unexplored(self, init = True):
        if init:
            neighbors = self.explorer.logbook[self.explorer.location].instance[0].planets_in_SOF
        else:
            neighbors = init.planets_in_SOF
        
            
        for p in neighbors:
            if self.explorer.check_discovery(p): #makes sure the returned planet will be reachable
                for pp in p.planets_in_SOF:
                    if self.explorer.check_exploration(pp):
                        return pp.name
        return False
        
    def get_planet_with_undiscovered(self, init = True):
        if init:
            neighbors = self.explorer.logbook[self.explorer.location].instance[0].planets_in_SOF
        else:
            neighbors = init.planets_in_SOF
        
            
        for p in neighbors:
            if self.explorer.check_discovery(p): #makes sure the returned planet will be reachable
                for pp in p.planets_in_SOF:
                    if self.explorer.check_discovery(pp):
                        return pp.name
        return False


                
        
    def play_procedural(self):
        
        old_SOF = list(self.explorer.logbook[self.explorer.location].instance[0].planets_in_SOF) #get the ps in SOF of explorer's loc
        self.explorer.logbook[self.explorer.location].instance[0].get_in_SOF() #scans for nearby planets
        self.get_variables() #monitors state of game
        self.explorer.logbook[self.explorer.location].instance[0].planets_in_SOF = old_SOF #resets SOF in case human player uses planet
        
        if self.variables[10] != 1: #checks if all planets in sof have been discovered
            self.perform_action(3)
        if self.variables[11] != 1: #checks if all planets in sof are explored
            self.perform_action(2) #forces exploration at start of play
        else:
            self.perform_action(1)
                

            
    def perform_action(self,action):
        '''perform action'''
#        if action == 1: #visit
#            pot_dests = [p for p in self.explorer.explored_planets if self.explorer.logbook[self.explorer.location].get_travel_info(p, self.explorer.travel_bonus) is None and self.explorer.logbook[self.explorer.location].travel_time <= 3]
#            pot_dests.remove(self.explorer.logbook[self.explorer.location].instance[0])
#            if len(pot_dests) > 0:
#                self.explorer.set_action('visit')
#                random.choice(pot_dests).visit(self.explorer)
#            else:
#                action = 2 #if only 1 planet is explored, then explores
        #____________________________________________________________________________________
        
        if action == 1: #visit
            self.explorer.get_destinations_of_interest()
            #pot_dests.remove(self.explorer.logbook[self.explorer.location].instance[0])
            if self.explorer.dest is not None:
                dest = pth.breadth_first_search(self.explorer,self.explorer.location,self.explorer.dest)
                if len(dest) > 0:
                    self.explorer.logbook[dest[0]].instance[0].visit(self.explorer)
                else:
                    pot_dests = [p for p in self.explorer.explored_planets if self.explorer.logbook[self.explorer.location].get_travel_info(p, self.explorer.travel_bonus) is None and self.explorer.logbook[self.explorer.location].travel_time <= 3]
                    pot_dests.remove(self.explorer.logbook[self.explorer.location].instance[0])
                    print 'passed'
                    if len(pot_dests) > 0:
                        random.choice(pot_dests).visit(self.explorer)
                self.explorer.set_action('visit')
            else:
                action = 2 #if only 1 planet is explored, then explores
         #_________________________________________________________________________________________       
                
        if action == 2: #explore
            unexplored_planets = [log.instance[0] for log in self.explorer.logbook.itervalues() if log.is_discovered and not log.is_explored and self.explorer.logbook[self.explorer.location].get_travel_info(log.instance[0], self.explorer.travel_bonus) is None and self.explorer.logbook[self.explorer.location].travel_time <= 4]
            if len(unexplored_planets) > 0:
                self.explorer.set_action('explore')
                random.choice(unexplored_planets).explore(self.explorer)
            else:
                action = 3 #to do a search instead
        if action == 3: #search
            self.explorer.set_action('search')
            self.explorer.logbook[self.explorer.location].instance[0].search_in_SOF(self.explorer, True)
            
#    def play(self):
##        '''free search around discovered planets'''
##        for p in self.explorer.explored_planets:
##            p.search_in_SOF(self.explorer, False)
#
#        '''get action'''
#        self.get_variables() #monitors state of game
#        print self.variables
#        action = self.get_action_from_rand_forest()[0] #get's action from state of game
#        
#        if self.game.year <= 5: action = 2 #forces exploration at start of play
#        if action != 0: print action
#            
#        self.perform_action(action)            

#    def set_algo(self):
#        #create the training & test sets, skipping the header row with [1:]
#        dataset = genfromtxt(open('./ai_training_data/test.csv','r'), delimiter=',', dtype='f8')[1:]
#        target = [x[-1:] for x in dataset]
#        train = [x[:-1] for x in dataset]
#        
#        #create and train the random forest
#        #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
#        self.algo = RandomForestClassifier(n_estimators=100)
#        self.algo.fit(train, target)
#    
#    def get_action_from_rand_forest(self):
#        test = self.variables[:-1]
#        return self.algo.predict(test)
#        #savetxt('Data/submission2.csv', rf.predict(test), delimiter=',', fmt='%f')
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
        
        
             
             
