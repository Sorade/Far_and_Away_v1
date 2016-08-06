# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 18:38:25 2016

@author: Julien
"""
import random
import pygame
import data
import sprite
import functions as fn

class Planet(sprite.MySprite):
    def __init__(self, game, pos):
        self.game = game
        self.name = 'X'+str(random.randint(0,1000))+str(random.randint(0,1000))+str(random.randint(0,1000))
        self.pos = pos
        self.discovered_by = []
        self.radius = random.randint(50,450) #SOF
        self.planets_in_SOF = []
        self.diameter = random.randint(5,50)
        self.disc_kp = random.randint(10,100)
        self.disc_rp = random.randint(10,100)
        self.img_ref = 'Venus'
        self.rect = data.Data.images_planets[self.img_ref].get_rect()
        
    def unveil(self,explorer,player_induced):
        explorer.logbook[self.name].is_known = True
        if player_induced == True:
            explorer.kp -= 5
        
    def explore(self, explorer):
        explorer.logbook[self.name].is_discovered = True
        explorer.logbook[self.name].discovery_time = self.game.gametime.get_tick()
        
    def get_in_SOF(self):
        for p in self.game.all_planets:
            if fn.dist(self.pos,p.pos) <= self.radius:
                self.planets_in_SOF.append(p)
                
    def filter_planets(self):
        if len(self.planets_in_SOF) == 0:
            self.game.all_planets.remove(self)
            return
        for p in self.game.all_planets:
            if self.rect.colliderect(p.rect) == True:
                self.game.all_planets.remove(self)
                break
                