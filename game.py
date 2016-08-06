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


class Game(object):
    def __init__(self):
        self.interface = interface.Interface(self)
        '''Create Planets'''
        self.all_planets = [planets.Planet(self,(random.randint(20,1000),random.randint(20,1000))) for x in range(10)]
        [p.get_in_SOF() for p in self.all_planets]
        #[p.filter_planets() for p in self.all_planets]
        self.all_explorers = [explorers.Explorer(self) for x in range (2)]
        self.player = (self.all_explorers[0])
        
    def run(self):
        yoffset,xoffset = 0,0
        black_bg = pygame.Surface((config.Config.screen_w,config.Config.screen_h))
        black_bg.fill((0,0,0))
        
        while True:
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                    
            '''setting up scrolling'''      
            if pygame.mouse.get_pos()[1] < 20:
                yoffset += 1
            if pygame.mouse.get_pos()[1] > config.Config.screen_h-20:
                yoffset -= 1
            if pygame.mouse.get_pos()[0] < 20:
                xoffset += 1
            if pygame.mouse.get_pos()[0] > config.Config.screen_w-20:
                xoffset -= 1
            
            self.interface.update_bigmap()
            
            '''Calling Display functions'''
            self.interface.screen.blit(black_bg,(0,0))
            self.interface.view_solarsys(fn.sum_tulp(self.all_planets[0].pos,(xoffset,yoffset)),self.all_planets[0])
            
            pygame.display.flip()
        
        