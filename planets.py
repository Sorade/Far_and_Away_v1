# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 18:38:25 2016

@author: Julien
"""
import random
import numpy as np
import pygame
import data
import sprite
import logbook as lgbk
import functions as fn

class Planet(sprite.MySprite):
    def __init__(self, game, pos):
        super(Planet, self).__init__()
        self.game = game
        self.name = '{}-{}'.format(fn.name_gen(True),str(random.randint(0,100)))
        self.pos = pos
        self.discovered_by = []
        self.explored_by = []
        self.radius = random.randint(250,500) #SOF
        self.planets_in_SOF = []
        self.chance_of_discovery = random.randint(0,15)
        self.diameter = random.randint(5,50)
        self.disc_kp = random.randint(0,12)
        self.disc_rp = random.randint(0,12)
        self.img_ref = 'Venus'
        
        self.rect = data.Data.images_planets[self.img_ref].get_rect()
        self.rect.center = pos
        
    def add_to_logbook(self,explorer):
        explorer.logbook[self.name] = lgbk.Logbook(self,False,False)
        
    def pop_around(self):
        ox,oy = self.pos
        self.get_in_SOF()
        while len(self.planets_in_SOF) <= 4:
            pop_dist = random.randint(max(self.rect.w+30,self.radius/2),self.radius)
            pop_angle = random.randint(0,int(np.pi))
            new_p_pos = fn.point_pos(self.pos,pop_dist,pop_angle)#(int(np.cos(pop_angle)*pop_dist),int(np.sin(pop_angle)*pop_dist))
            new_p = Planet(self.game,new_p_pos) 
            if fn.check_collision(new_p,self.planets_in_SOF) == False:
                self.planets_in_SOF.append(new_p) 
                self.game.all_planets.add(new_p)
                new_p.add_to_logbook(self.game.player)
            
        
    def unveil(self,explorer,player_induced,bonus):
        if player_induced == True  and explorer.kp >= 5:
            explorer.kp -= 5
            if explorer.logbook[self.name].is_discovered == False and self.chance_of_discovery+bonus >= random.randint(0,100):
                explorer.logbook[self.name].is_discovered = True
                self.discovered_by.append(explorer.name)
                self.pop_around()
                self.game.interface.add_message('Discovered {}'.format(self.name),1)
                
        elif explorer.logbook[self.name].is_discovered == False and self.chance_of_discovery >= random.randint(0,100):
            explorer.logbook[self.name].is_discovered = True
            self.discovered_by.append(explorer.name)
            self.pop_around()
            self.game.interface.add_message('Auto-Discovered {}'.format(self.name),1)
            arrow_stats = self.game.interface.arrow_param(self)
            if arrow_stats: self.game.interface.add_arrow(arrow_stats,2)
            
        
    def explore(self, explorer):
        if explorer.logbook[self.name].is_explored == False:
            test = self.visit(explorer, True)
            if test == True:
                '''remove the visit message so that the exploration message
                occurs first. If the test is true then the message will be re-added
                at the end of the message list (after exploration msg)'''
                visit_msg = self.game.interface.messages[-1]
                self.game.interface.messages.remove(visit_msg)                
                explorer.logbook[self.name].is_explored = True
                explorer.logbook[self.name].time_of_exploration = self.game.month
                explorer.kp += self.disc_kp
                explorer.rp += self.disc_rp -10 #-10 is the exploration malus
                self.explored_by.append(explorer.name)
                self.game.interface.add_message('Player explored {}'.format(self.name),1)
                self.game.interface.add_message(visit_msg,1)
        
    def visit(self, explorer, explo = False):
        if explorer.location != self.name:
            travel_cost = fn.travel_formula(fn.dist(self.game.player.logbook[self.game.player.location].instance[0].pos,self.pos)/self.game.space_travel_unit)
            if explo: travel_cost += 10
            if explorer.rp >= travel_cost:
                explorer.rp -= travel_cost
                explorer.location = self.name
                self.game.interface.add_message('Player is at {}'.format(self.name),1)
                return True
        else:
            return False
            
    def search_in_SOF(self,explorer,player_induced,bonus):
        if explorer.logbook[self.name].is_explored:
            launch = True if explorer.kp >= 5 else False
            if player_induced and launch: self.game.interface.add_message('Searching around {} ...'.format(self.name),1)
            for planet in self.planets_in_SOF:
                if launch == False:
                    break
                planet.unveil(explorer,player_induced,bonus)
            if player_induced and launch: self.game.interface.add_message('... search completed'.format(self.name),1)
            

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
                
                