# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:50:54 2016

@author: julien
"""
'''import built in modules'''
import pygame
from pygame.locals import*
import random
import sys

'''Game Init'''
pygame.init()
clock = pygame.time.Clock() #set timer which is used to slow game down

'''import game modules'''
import interface
import planets
import explorers
import config
import functions as fn
import time

class Game(object):
    def __init__(self):
        self.interface = interface.Interface(self)
        self.clock = pygame.time.Clock() #set timer which is used to slow game down
        self.month = 0

        '''Create Planets'''
        self.all_planets = pygame.sprite.Group()
        self.generate_planets()
        [p.get_in_SOF() for p in self.all_planets]
        '''create explorers and player'''
        self.all_explorers = [explorers.Explorer(self) for x in range (2)]
        self.player = explorers.Explorer(self)
        
        '''assign starting planet to player only'''
        delay, x = 20, 0
        for p in self.all_planets:
            if x == delay:
                p.chance_of_discovery = 100
                p.unveil(self.player,False)
                p.explore(self.player)
                break  
            x += 1
        
        '''setting up game switches'''
        self.pressed_left_clic = False  
        self.map_mode = True
        self.planet_mode = False
        
        
    def generate_planets(self):
        offset = 50
        w = config.Config.screen_w-offset
        h = config.Config.screen_h-offset
        
        row_nb,col_nb = 5,10
        for row in range(offset/2, int(h + offset*1.5), h/row_nb):
            for col in range(offset/2, int(w + offset*1.5), w/col_nb):
                self.all_planets.add(planets.Planet(self,(col,row)))
                
                       
    def planet_discovery_event(self,player_induced):
        for log in self.player.logbook.values():
            log.instance[0].search_in_SOF(self.player,False)
            
    def resource_prod_event(self):
        for log in self.player.logbook.values():
            if log.is_explored :
                self.player.rp += 5
                
    def knowledge_prod_event(self):
        for log in self.player.logbook.values():
            if log.is_explored :
                self.player.kp += 5
                
    def points_prod_event(self):
        self.resource_prod_event()
        self.knowledge_prod_event()
                
    def run(self):
        '''set up'''
        black_bg = pygame.Surface((config.Config.screen_w,config.Config.screen_h))
        black_bg.fill((0,0,0))
        pygame.time.set_timer(USEREVENT + 1, 5000) # 1 event every 10 seconds
        
        while True:
            self.clock.tick(60) #needed to slow game down
            t0 = time.time()
                        
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                elif event.type == USEREVENT + 1:
                    self.month += 1 #adds a months of gametime every 10 seconds
                    self.planet_discovery_event(False)
                    self.points_prod_event()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.pressed_left_clic = True
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.pressed_left_clic = True
                    
            if self.map_mode == True:
                '''Calling Display functions'''
                self.interface.screen.blit(black_bg,(0,0))
                planet = [ v for v in self.player.logbook.values()][0].instance[0]
                self.interface.view_solarsys((config.Config.screen_w/2,config.Config.screen_h/2),planet)
                
            if self.planet_mode == True:
                self.interface.view_planet(self.interface.selected)            
                    

            
            pygame.display.update()
            t1 = time.time()
            #print t1-t0
        
        