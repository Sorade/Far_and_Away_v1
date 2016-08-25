# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:32:09 2016

@author: julien
"""
import random
from logbook import*

class Explorer(object):
    def __init__(self,game):
        self.game = game
        self.name = random.choice(['Roger','Logan','Fred','Susan','Morgane','Iloa'])
        self.location = 0
        self.logbook = {}
        self.kp = 10
        self.rp = 10
        self.kp_bonus = 0
        self.rp_bonus = 0
        self.travel_bonus = 1
        self.search_bonus = 40
        self.monthly_rp_expense = 0
        self.monthly_rp_income = 0
        
        
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
            planet.explore(self)
        else:
            planet.visit(self)
            
    def check_discovery(self, planet):
        return self.name in planet.discovered_by

    def check_exploration(self, planet):
        return self.name in planet.explored_by
        
    def get_logbook_planets(self):
        for log in self.logbook.itervalues():
            yield log.instance[0] 
