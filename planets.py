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
        super(Planet, self).__init__()
        self.game = game
        self.name = '{}-X{}-{}'.format(random.choice(data.Data.planet_names),str(random.randint(0,100)),str(random.randint(0,100)))
        self.pos = pos
        self.discovered_by = []
        self.explored_by = []
        self.radius = random.randint(0,300) #SOF
        self.planets_in_SOF = []
        self.chance_of_discovery = random.randint(0,10)
        self.diameter = random.randint(5,50)
        self.disc_kp = random.randint(0,20)
        self.disc_rp = random.randint(0,20)
        self.img_ref = 'Venus'
        
        self.rect = data.Data.images_planets[self.img_ref].get_rect()
        self.rect.center = pos
        
    def unveil(self,explorer,player_induced,bonus):
        if player_induced == True  and explorer.kp >= 5:
            explorer.kp -= 5
            if explorer.logbook[self.name].is_discovered == False and self.chance_of_discovery+bonus >= random.randint(0,100):
                explorer.logbook[self.name].is_discovered = True
                self.discovered_by.append(explorer.name)
                
        elif explorer.logbook[self.name].is_discovered == False and self.chance_of_discovery >= random.randint(0,100):
            explorer.logbook[self.name].is_discovered = True
            self.discovered_by.append(explorer.name)

        
    def explore(self, explorer):
        if explorer.logbook[self.name].is_explored == False:
            test = self.visit(explorer)
            if test == True:
                explorer.logbook[self.name].is_explored = True
                explorer.logbook[self.name].time_of_exploration = self.game.month
                explorer.kp += self.disc_kp
                explorer.rp += self.disc_rp -10
                self.explored_by.append(explorer.name)
                print 'Player explored {}'.format(self.name)
        
    def visit(self, explorer):
        if explorer.location != self.name:
            steps = fn.steps(explorer.logbook[explorer.location].instance[0].pos,self.pos,self.game.dx,self.game.dy)
            if explorer.rp >= steps*steps:
                explorer.rp -= steps*steps
                explorer.location = self.name
                print 'Player is at {}'.format(self.name)
                return True
        else:
            return False
            
    def search_in_SOF(self,explorer,player_induced,bonus):
        if explorer.logbook[self.name].is_explored:
            for planet in self.planets_in_SOF:
                if explorer.kp == 0:
                    break
                planet.unveil(explorer,player_induced,bonus)

    def get_in_SOF(self):
        self.planets_in_SOF = []
        for p in self.game.all_planets:
            if fn.dist(self.pos,p.pos) <= self.radius:
                self.planets_in_SOF.append(p)
                
    def filter_planets(self):
        if len(self.planets_in_SOF) == 0:
            self.game.all_planets.remove(self)
            return
        group_without_self = self.game.all_planets
        group_without_self.remove(self)
        collisions = pygame.sprite.spritecollideany(self, group_without_self)
        group_without_self.add(self)
        if collisions != None:
            self.game.all_planets.remove(collisions)
            
            
#        for p in self.game.all_planets:
#            if self.rect.colliderect(p.rect) == True:
#                self.game.all_planets.remove(p)
                
                