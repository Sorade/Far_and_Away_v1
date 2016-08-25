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
import event_manager as em
from events import *
import interface
import planets
import explorers
import config
import logbook as lgbk
import functions as fn
import time
from worlds import *

class Game(object):
    def __init__(self):
        self.event_manager = em.Event_Manager(self)
        self.interface = interface.Interface(self)
        self.clock = pygame.time.Clock() #set timer which is used to slow game down
        self.month = 0
        self.space_travel_unit = 150
        self.planet_choices = [World_Mining,World_Habitable,World_Frozen,World_Alien]
        '''create explorers and player'''
        self.all_explorers = [explorers.Explorer(self) for x in range (2)]
        self.player = explorers.Explorer(self)

        '''Create Planets'''
        tierra = World_Habitable(self,(config.Config.screen_w/2,config.Config.screen_h/2))
        self.all_planets = pygame.sprite.Group()
        self.all_planets.add(tierra)
        
        '''assign starting planet to player only'''
        tierra.name = 'Tierra'
        self.player.logbook[tierra.name] = lgbk.Logbook(tierra,True,True)
        self.player.logbook[tierra.name].time_of_exploration = self.month
        tierra.discovered_by.append(self.player.name)
        tierra.explored_by.append(self.player.name)
        self.player.location = tierra.name
        tierra.disc_kp,tierra.disc_rp = 10,8
        tierra.radius = 600
        tierra.pop_around(max_planet = 5, max_iter = 50)
        
        '''creats events'''
        self.event_list = [Precious_Ore_Discovered(self),Raiders(self),Old_Archives(self),Storm(self),Rebellion(self),Alien_Tech(self)]

            
        '''setting up game switches'''
        self.pressed_left_clic = False 
        self.pressed_mid_clic = False
        self.pressed_right_clic = False
        self.map_active = True
#        self.planet_mode = False
        self.pause = False
        
        
#    def initial_planet(self):
#        self.all_planets.add(planets.Planet(self,(config.Config.screen_w/2,config.Config.screen_h/2)))
#        for p in self.all_planets: p.pop_around()
                
                       
    def run(self):
        '''set up'''
        black_bg = pygame.Surface((config.Config.screen_w,config.Config.screen_h))
        black_bg.fill((0,0,25))        
        pygame.time.set_timer(USEREVENT + 1, 5000) # 1 event every 10 seconds
        pygame.time.set_timer(USEREVENT + 2, 1000) # 1 event every 1 seconds
        pygame.time.set_timer(USEREVENT + 3, 75) # map offset every 100 ms
        
        while True:
            self.clock.tick(60) #needed to slow game down
            t0 = time.time()
            
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    print 'has quit' 
                elif event.type == USEREVENT + 3:
                    self.interface.get_map_offset()
                elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    if self.pause == True: self.pause = False
                    elif self.pause == False: self.pause = True
                elif event.type == pygame.KEYDOWN and event.key == K_h:
                    if self.interface.helpers == True: self.interface.helpers = False
                    elif self.interface.helpers == False: self.interface.helpers = True                        
                elif event.type == USEREVENT + 2:
                    self.interface.display_event = True
                    if self.interface.arrow_disp_time > 0: self.interface.arrow_disp_time -= 1
                elif event.type == USEREVENT + 1 and self.pause == False:
                    #Monthly Events and actions
                    self.event_manager.all_monthly_events()
                    for event in self.event_list: event.get_weight(self.player)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.pressed_left_clic = True
                elif event.type == MOUSEBUTTONUP and event.button == 1:
                    self.pressed_left_clic = True
                elif event.type == MOUSEBUTTONDOWN and event.button == 2:
                    self.pressed_mid_clic = True
                elif event.type == MOUSEBUTTONUP and event.button == 2:
                    self.pressed_mid_clic = True                    
                elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                    self.pressed_right_clic = True
                elif event.type == MOUSEBUTTONUP and event.button == 3:
                    self.pressed_right_clic = True                    

            '''Calling Display functions'''
            self.interface.screen.blit(black_bg,(0,0))
            self.interface.view_solarsys(self.player,(config.Config.screen_w/2,config.Config.screen_h/2))
            self.interface.event_popup(self.event_manager.active_events,self.player)    
            self.interface.final_overlay(self.player) #will only display messages when USEREVENT+2 has occured
            fn.display_txt(str(len(self.all_planets)),'Lucida Console',16,(200,200,0),self.interface.screen,(500,80))

            
            pygame.display.update()
            t1 = time.time()
            #print t1-t0
        
        