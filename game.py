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
        '''Create Planets'''
        self.all_planets = pygame.sprite.Group()
        #[self.all_planets.add(planets.Planet(self,(random.randint(50,4950),random.randint(50,4950)))) for x in range(400)]
        self.generate_planets()
        [p.get_in_SOF() for p in self.all_planets]
        [p.filter_planets() for p in self.all_planets]
        [p.get_in_SOF() for p in self.all_planets]
        self.all_explorers = [explorers.Explorer(self) for x in range (2)]
        self.player = explorers.Explorer(self)
        
        '''setting up game switches'''
        self.map_mode = False
        self.planet_mode = False
        
    def generate_planets(self):
        offset = 50
        w = config.Config.screen_w-offset
        h = config.Config.screen_h-offset
        
        row_nb,col_nb = 5,10
        
        for row in range(offset,h,h/row_nb):
            for col in range(offset,w,w/col_nb):
                self.all_planets.add(planets.Planet(self,(col,row)))

       
    def run(self):
        '''set up'''
        clock = pygame.time.Clock() #set timer which is used to slow game down
        black_bg = pygame.Surface((config.Config.screen_w,config.Config.screen_h))
        black_bg.fill((0,0,0))
        
        while True:
            clock.tick(60) #needed to slow game down
            t0 = time.time()
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'

            self.interface.update_bigmap()
            
            '''Calling Display functions'''
            self.interface.screen.blit(black_bg,(0,0))
            planet = [ v for v in self.player.logbook.values()][0].instance[0]
            self.interface.view_solarsys((config.Config.screen_w/2,config.Config.screen_h/2),planet)
               
            
            pygame.display.update()
            t1 = time.time()
            print t1-t0
        
        