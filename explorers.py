# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:32:09 2016

@author: julien
"""
import random
from logbook import*
from tools_classes import States
from ai import ai

class Explorer(object):
    def __init__(self,game):
        self.game = game
        self.ai = ai(game,self)
        self.name = random.choice(['Roger','Logan','Fred','Susan','Morgane','Iloa']) +' ' + fn.surname_gen(True)
        self.location = 0
        self.logbook = {}
        self.explored_planets = []
        self.kp = 10
        self.rp = 10
        self.kp_bonus = 0
        self.rp_bonus = 0
        self.travel_bonus = 1
        self.search_bonus = 0
        self.yearly_rp_expense = 0
        self.yearly_rp_income = 0
        self.yearly_kp_income = 0
        self.states = States()
        self.time_since_last_action = 0
        self.time_of_last_action = 0
        self.action = 0
        
        
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