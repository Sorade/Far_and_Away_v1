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
import events
import interface
import planets
import explorers
import config
import functions as fn
import time

class Game(object):
    def __init__(self):
        self.event_manager = events.Event_Manager(self)
        self.interface = interface.Interface(self)
        self.clock = pygame.time.Clock() #set timer which is used to slow game down
        self.month = 0

        '''Create Planets'''
        self.all_planets = pygame.sprite.Group()
        self.dx, self.dy = self.generate_planets()
        [p.get_in_SOF() for p in self.all_planets]
        '''create explorers and player'''
        self.all_explorers = [explorers.Explorer(self) for x in range (2)]
        self.player = explorers.Explorer(self)
        
        '''assign starting planet to player only'''
        delay, x = 20, 0
        temp_name = 0
        for p in self.all_planets:
            if x >= delay and len(p.planets_in_SOF) >= 4:
                self.player.location = temp_name
                p.chance_of_discovery = 100
                p.disc_kp,p.disc_rp = 10,10
                p.unveil(self.player,False,0)
                steps = fn.steps(self.player.logbook[temp_name].instance[0].pos,p.pos,self.dx,self.dy)
                self.player.rp += steps*steps+1
                p.explore(self.player)
                p.disc_kp,p.disc_rp = 8,8 #starting values
                break
            temp_name = p.name
            x += 1
        
        '''setting up game switches'''
        self.pressed_left_clic = False 
        self.pressed_mid_clic = False
        self.pressed_right_clic = False
        self.map_active = True
#        self.planet_mode = False
        self.pause = False
        
        
    def generate_planets(self):
        offset = 50
        w = config.Config.screen_w-offset
        h = config.Config.screen_h-offset
        
        row_nb,col_nb = 5,10
        for row in range(offset/2, int(h - offset), h/row_nb):
            for col in range(offset/2, int(w + offset*1.5), w/col_nb):
                self.all_planets.add(planets.Planet(self,(col,row)))
                
        return w/col_nb, h/row_nb
                
                       
    def run(self):
        '''set up'''
        black_bg = pygame.Surface((config.Config.screen_w,config.Config.screen_h))
        black_bg.fill((0,0,25))        
        pygame.time.set_timer(USEREVENT + 1, 5000) # 1 event every 10 seconds
        pygame.time.set_timer(USEREVENT + 2, 1000) # 1 event every 1 seconds
        
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
                elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    if self.pause == True: self.pause = False
                    elif self.pause == False: self.pause = True
                elif event.type == pygame.KEYDOWN and event.key == K_h:
                    if self.interface.helpers == True: self.interface.helpers = False
                    elif self.interface.helpers == False: self.interface.helpers = True                        
                elif event.type == USEREVENT + 2:
                    self.interface.display_event = True
                elif event.type == USEREVENT + 1 and self.pause == False:
                    self.month += 1 #adds a months of gametime every 10 seconds
                    self.event_manager.get_random_event()
                    self.event_manager.planet_discovery_event(False)
                    self.event_manager.points_adjustement_event()
                    self.event_manager.network_expenses_event()
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
            self.interface.view_solarsys((config.Config.screen_w/2,config.Config.screen_h/2))
            self.interface.event_popup()    
            self.interface.final_overlay() #will only display messages when USEREVENT+2 has occured
            
            
            pygame.display.update()
            t1 = time.time()
            #print t1-t0
        
        