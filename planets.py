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
from tools_classes import Quad

class Planet(sprite.MySprite):
    def __init__(self, game, pos, img_ref):
        super(Planet, self).__init__()
        self.game = game
        self.name = '{}-{}'.format(fn.name_gen(True),str(random.randint(0,100)))
        self.pos = pos
        self.discovered_by = []
        self.explored_by = []
        self.planets_in_SOF = []
        self.chance_of_discovery = random.randint(0,15)
        self.diameter = random.randint(5,50)
        self.img_ref = img_ref
        self.is_virgin =  True
        self.has_popped = False
        
        
        self.rect = data.Data.images_planets[self.img_ref].get_rect()
        self.rect.center = pos
        
    def add_to_logbook(self,explorer):
        explorer.logbook[self.name] = lgbk.Logbook(self,False,False)
        
    def pop_around(self, max_planet = 2, max_iter = 3):
        if not self.has_popped:
            ox,oy = self.pos
            self.get_in_SOF()
            Quad.get_content(self.pos,[p.pos for p in self.game.all_planets])
            Quad.get_weights()
            iteration = 1
            num_planet = 1
            self.has_popped = True
            while num_planet <= max_planet and iteration <= max_iter :#len(self.planets_in_SOF) <= 4 and max_iter <= 100:
                #remove the radius of the planet so that planets do not overlap
                #will only work if the radius of all planets are the same
                pop_dist = random.randint(max(self.rect.w+30,self.radius/2),self.radius-self.rect.w)
                angle_min,angle_max = fn.choice_weighted(Quad.angle_list, True)
                pop_angle = random.uniform(angle_min,angle_max)
                new_p_pos = fn.point_pos(self.pos,pop_dist,pop_angle)#(int(np.cos(pop_angle)*pop_dist),int(np.sin(pop_angle)*pop_dist))
                new_p = fn.choice_weighted(self.game.planet_choices)(self.game,new_p_pos) 
                if fn.check_collision(new_p,self.planets_in_SOF) == False:
                    self.planets_in_SOF.append(new_p) 
                    self.game.all_planets.add(new_p)
                    new_p.add_to_logbook(self.game.player)
                    Quad.update_weights(self.pos,new_p_pos)
                    num_planet += 1
                iteration += 1
            
        
    def unveil(self,explorer,player_induced):
        if player_induced == True:
            explorer.kp -= fn.search_cost(self.cat)
            if not explorer.check_discovery(self) and self.chance_of_discovery + explorer.search_bonus >= random.randint(0,100):
                explorer.logbook[self.name].is_discovered = True
                self.discovered_by.append(explorer.name)
                self.game.interface.add_message('Discovered {}'.format(self.name),1)
                if random.randint(0,100) <= 25: self.pop_around(max_planet=self.pop_factor,max_iter=self.pop_factor*2)
                arrow_stats = self.game.interface.arrow_param(self)
                if arrow_stats: self.game.interface.add_arrow(arrow_stats,2)
                
        elif not explorer.check_discovery(self) and self.chance_of_discovery >= random.randint(0,100):
            explorer.logbook[self.name].is_discovered = True
            self.discovered_by.append(explorer.name)
            self.game.interface.add_message('Auto-Discovered {}'.format(self.name),1)
            if random.randint(0,100) <= 25: self.pop_around(max_planet=self.pop_factor,max_iter=self.pop_factor*2)
            arrow_stats = self.game.interface.arrow_param(self)
            if arrow_stats: self.game.interface.add_arrow(arrow_stats,2)
            
        
    def explore(self, explorer):
        if explorer.logbook[self.name].is_explored == False:
            test = self.visit(explorer, True)
            if test == True:
                '''remove the visit message so that the exploration message
                occurs first. If the test is true then the message will be re-added
                at the end of the message list (after exploration msg)'''
                #to do only for first explorer to explore
                if self.is_virgin:
                    explorer.kp += self.disc_kp
                    #works out cost/gain from exploration
                    explorer.rp += self.disc_rp - fn.exploration_cost_formula(len([log for log in self.game.player.logbook.itervalues() if log.is_explored]),explorer.kp,self.disc_kp)
                    explorer.logbook[self.name].time_of_exploration = self.game.year
                    self.pop_around(max_planet=self.pop_factor,max_iter=self.pop_factor*2)
                    self.is_virgin = False

                #to do at every exploration or re-explroation
                visit_msg = self.game.interface.messages[-1]
                self.game.interface.messages.remove(visit_msg)                
                explorer.logbook[self.name].is_explored = True
                self.explored_by.append(explorer.name)
                self.game.interface.add_message('Player explored {}'.format(self.name),1)
                self.game.interface.add_message(visit_msg,1)
        
    def visit(self, explorer, explo = False):
        if explorer.location != self.name:
#            travel_time = fn.travel_time(fn.dist(self.game.player.logbook[self.game.player.location].instance[0].pos,self.pos)/self.game.space_travel_unit)
#            travel_cost = fn.travel_formula(travel_time)
            #generate travel time and cost for the planet
            explorer.logbook[explorer.location].get_travel_info(self,explorer.travel_bonus)
            travel_cost = explorer.logbook[explorer.location].travel_cost
            if explo: travel_cost += fn.exploration_cost_formula(len([log for log in explorer.logbook.itervalues() if log.is_explored]),explorer.kp,self.disc_kp)
            if explorer.rp >= travel_cost:
                #removes cost of travel
                explorer.rp -= explorer.logbook[explorer.location].travel_cost
                explorer.location = self.name
                for x in range(explorer.logbook[explorer.location].travel_time):
                    self.game.event_manager.all_yearly_events(explorer)
                self.game.interface.add_message('Player is at {}'.format(self.name),1)
                return True
        else:
            return False
            
    def search_in_SOF(self,explorer,player_induced):
        if explorer.logbook[self.name].is_explored:
            if player_induced:
                self.game.event_manager.all_yearly_events(explorer)
                self.game.interface.add_message('Searching around {} ...'.format(self.name),1)
                loc_bonus = 20
                if explorer.location == self.name: explorer.search_bonus += loc_bonus # adds a loc bonus
                
                for planet in self.planets_in_SOF:
                    if explorer.kp >= fn.search_cost(planet.cat) and not explorer.check_discovery(planet):
                        planet.unveil(explorer,player_induced)
                        
                self.game.interface.add_message('... search completed'.format(self.name),1)
                if explorer.location == self.name: explorer.search_bonus -= loc_bonus #remove the loc bonus
            else:
                for planet in self.planets_in_SOF:
                    if not explorer.check_discovery(planet):
                        planet.unveil(explorer,player_induced)


    def get_in_SOF(self):
        self.planets_in_SOF = []
        for p in self.game.all_planets:
            if fn.dist(self.pos,p.pos) <= self.radius:
                self.planets_in_SOF.append(p)
                
                