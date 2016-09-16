# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:32:09 2016

@author: julien
"""
import random
from config import *
from logbook import*
from tools_classes import States
from ai import ai
from ship import Ship

class Explorer(object):
    def __init__(self,game,player_type = 'cpu'):
        self.game = game
        self.ai = ai(game,self)
        self.type = player_type #or 'human'
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.name = random.choice(['Drake','Logan','Fredrik','Susan','Morgane','Iloa','Markus','Karson','Clyde','Athelstan']) +' ' + fn.surname_gen(True)
        self.location = 0
        self.dest = self.location
        self.logbook = Logbook(self,game)
        self.explored_planets = []
        self.kp = 40
        self.rp = 30
        self.kp_bonus = 0
        self.rp_bonus = 0
        self.travel_bonus = 1
        self.search_bonus = 0
        self.yearly_rp_expense = 0
        self.yearly_rp_income = 0
        self.yearly_kp_income = 0
        if self.type == 'cpu':
            self.ai_income_modifier = [1+0.1*(n+1) for n,dif in enumerate(Config.ai_difficulty.iteritems()) if dif[1]][0]
        else:
            self.ai_income_modifier = 1
        self.states = States()
        self.time_since_last_action = 0
        self.time_of_last_action = 0
        self.action = 0
        self.active_events = []
        self.ship = Ship(self)
        
        
    @property
    def kp(self):
        return self._kp

    @kp.setter
    def kp(self, kp):
        kp = 0 if kp < 0 else kp
        self._kp = kp
        
    @property
    def rp(self):
        return self._rp

    @rp.setter
    def rp(self, rp):
        rp = 0 if rp < 0 else rp
        self._rp = rp
        
    def get_location(self):
        return self.logbook[self.location].instance[0]
        
    def assign_starting_planet(self,planet):
        self.logbook[planet.name] = Log(self,planet,True,True)
        self.logbook[planet.name].time_of_exploration = self.game.year
        self.explored_planets.append(planet)
        planet.discovered_by.append(self.name)
        planet.explored_by.append(self.name)
        self.location = planet.name
        planet.disc_kp,planet.disc_rp = 15,8
        planet.radius = 600        
        
    def select_displacement(self, planet):
        ''' checks whether the explorer has explored the planet or not and
            performs the corresponding displacement function (explore or visit)
            Explorer Planet -> None
            SE: -explore
                -visit
        '''
        if not self.check_exploration(planet):
            self.set_action('explore')
            planet.explore(self)
        else:
            self.set_action('visit')
            planet.visit(self)
            
    def check_discovery(self, planet):
        return self.name in planet.discovered_by

    def check_exploration(self, planet):
        return self.name in planet.explored_by
        
    def get_destinations_of_interest(self):
        if self.dest == self.location:
            pot_dests = [p.name for p in self.explorer.explored_planets if len([n for n in p.planets_in_SOF if not self.explorer.check_exploration(n) or not self.explorer.check_discovery(n)])]
            if len(pot_dests) > 0:
                self.dest = random.choice(pot_dests)
            else:
                self.dest = None
        
    def get_logbook_planets(self):
        for log in self.logbook.itervalues():
            yield log.instance[0]
            
    def set_time_since_last_action(self):
        self.time_since_last_action = self.game.year - self.time_of_last_action
        if self.action != 0:
            self.time_of_last_action = self.game.year
            
    def get_planet_ratio_at_loc(self):
        planets_in_sof =  self.logbook[self.location].instance[0].planets_in_SOF
        discovered_planets = [p for p in planets_in_sof if self.check_discovery(p)]
        explored_planets = [p for p in planets_in_sof if self.check_exploration(p)]
        ratio_exp_to_disc = float(len(explored_planets))/len(discovered_planets)
        ratio_disc_to_pop = float(len(discovered_planets))/len(planets_in_sof)
        return ratio_disc_to_pop, ratio_exp_to_disc
        
    def set_action(self,action):
        actions = {'none' : 0, 'visit' : 1, 'explore' : 2, 'search' : 3}
        self.action = actions[action]
        self.set_time_since_last_action()