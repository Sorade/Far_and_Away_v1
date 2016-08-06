# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:50:54 2016

@author: julien
"""
import pygame
from pygame.locals import*
import random
import planets
import explorers
import interface

class Game(object):
    def __init__(self):
        '''Create Planets'''
        self.all_planets = [planets.Planet(self,(random.randint(20,10000),random.randint(20,10000))) for x in range(200)]
        self.all_explorers = [explorers.Explorer(self) for x in range (2)]
        self.player = (self.all_explorers[0])
        self.interface = Interface(self)
        
    def run(self):
        
        