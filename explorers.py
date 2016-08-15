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
        self.monthly_rp_expense = 1
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

