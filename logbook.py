# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:45:26 2016

@author: julien
"""
import functions as fn

#class Logbook(object):
#    def __init__(self, body, is_discovered, is_explored):
#        self.instance = [body]
#        self.is_discovered = is_discovered
#        self.is_explored = is_explored
#        self.time_of_exploration = None
#        self.travel_time = 0
#        self.travel_cost = 0
#        
#    def get_travel_info(self,planet,travel_bonus):
#        self.travel_time = fn.travel_time(fn.dist(self.instance[0].pos,planet.pos),self.instance[0].game.space_travel_unit)/travel_bonus
#        self.travel_cost = fn.travel_formula(self.travel_time)

class Logbook(dict):
    def __init__(self,explorer,game):
        self.explorer = explorer
        self.game = game
        
    def fetch_neighbors(self,planet_name):
        if planet_name not in self.iterkeys():
            for planet in self.game.all_planets:
                if planet.name == planet_name:
                    planet.add_to_logbook(self.explorer)
                    
        return [p.name for p in self[planet_name].instance[0].planets_in_SOF]
        
class Log(object):
    def __init__(self, explorer, body, is_discovered, is_explored):
        self.explorer = explorer
        self.instance = [body]
        self.is_discovered = is_discovered
        self.is_explored = is_explored
        self.time_of_exploration = None
        self.first_exploration = True
        self.travel_time = 0
        self.travel_cost = 0
        
    @property
    def is_explored(self):
        return self._is_explored

    @is_explored.setter
    def is_explored(self, is_explored):
        if is_explored:
            self.explorer.explored_planets.append(self.instance[0])
        else:
            try:
                self.explorer.explored_planets.remove(self.instance[0])
            except:
                pass
        self._is_explored = is_explored
        
        
    def get_travel_info(self,planet,travel_bonus):
        self.travel_time = fn.travel_time(fn.dist(self.instance[0].pos,planet.pos),self.instance[0].game.space_travel_unit)/travel_bonus
        self.travel_cost = fn.travel_formula(self.travel_time)

        
       