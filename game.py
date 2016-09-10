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
pygame.mixer.init()
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
import data

class Game(object):
    def __init__(self):
        self.event_manager = em.Event_Manager(self)
        self.interface = interface.Interface(self)
        self.clock = pygame.time.Clock() #set timer which is used to slow game down
        self.year = 0
        self.space_travel_unit = 150
        self.planet_choices = [World_Mining, 
                               World_Habitable, 
                               World_Frozen, 
                               World_Alien, 
                               World_Jungle]
        '''create explorers and player'''
        self.all_explorers = [explorers.Explorer(self) for x in range (2)]
        self.player = explorers.Explorer(self)

        '''Create Planets'''
        tierra = World_Habitable(self,(config.Config.screen_w/2,config.Config.screen_h/2))
        self.all_planets = pygame.sprite.Group()
        self.all_planets.add(tierra)
        
        '''assign starting planet to player only'''
        tierra.name = 'Tierra'
        tierra.img_ref = 'Earth'
        self.player.logbook[tierra.name] = lgbk.Log(self.player,tierra,True,True)
        self.player.logbook[tierra.name].time_of_exploration = self.year
        tierra.discovered_by.append(self.player.name)
        tierra.explored_by.append(self.player.name)
        self.player.location = tierra.name
        tierra.disc_kp,tierra.disc_rp = 15,8
        tierra.radius = 600
        for x in range(2): tierra.pop_around(max_planet = 3, max_iter = 10000)
        
        #increases the chance of discovery of starting planets
        for planet in self.all_planets:
            planet.chance_of_discovery = 101
            
        #makes initial discovery for player
        self.event_manager.planet_discovery_event(self.player,False)
        
        '''creats events'''
        self.event_manager.event_list = [Precious_Ore_Discovered(self), 
                                         Raiders(self),
                                         Old_Archives(self), 
                                         Storm(self),
                                         Rebellion(self),
                                         Alien_Tech(self),
                                         Alien_Weapons(self),
                                         Astronomer(self),
                                         Contamination(self),
                                         Cure(self)]            
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
        black_bg.fill((0,0,3))
        delta_time = 1000
        current_time_setting = 5000
        pygame.time.set_timer(USEREVENT + 1, current_time_setting) # 1 event every 10 seconds
        pygame.time.set_timer(USEREVENT + 2, 1000) # 1 event every 1 seconds
        pygame.time.set_timer(USEREVENT + 3, 75) # map offset every 100 ms
        
        pygame.mixer.music.load(data.Data.musics['theme'])
        pygame.mixer.music.play(-1,0.0)
        
        while True:
            self.clock.tick(60) #needed to slow game down
            #t0 = time.time()
            
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
                elif event.type == USEREVENT + 2:
                    self.interface.display_event = True
                    if self.interface.arrow_disp_time > 0: self.interface.arrow_disp_time -= 1
                elif event.type == USEREVENT + 1 and self.pause == False:
                    #yearly Events and actions
                    self.event_manager.all_yearly_events(self.player)                      
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        if self.pause == True: self.pause = False
                        elif self.pause == False: self.pause = True
                    elif event.key == K_h:
                        if self.interface.helpers == True: self.interface.helpers = False
                        elif self.interface.helpers == False: self.interface.helpers = True
                    elif event.key == K_h:
                        if self.interface.helpers == True: self.interface.helpers = False
                        elif self.interface.helpers == False: self.interface.helpers = True  
                    elif event.key == K_MINUS or event.key == K_KP_MINUS:
                        print current_time_setting
                        if current_time_setting <= 60000:
                            current_time_setting += delta_time
                        else:
                            current_time_setting = 60000
                        pygame.time.set_timer(USEREVENT + 1, current_time_setting)
                    elif event.key == K_PLUS or event.key == K_KP_PLUS:
                        if current_time_setting >= 1000:
                            current_time_setting -= delta_time
                        else:
                            current_time_setting = 1000
                        pygame.time.set_timer(USEREVENT + 1, current_time_setting)

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 3:
                        self.pressed_right_clic = True
                    elif event.button == 1:
                        self.pressed_left_clic = True
                    elif event.button == 2:
                        self.pressed_mid_clic = True
                    elif event.button == 4:
                        self.interface.delta += 1
                    elif event.button == 5:
                        self.interface.delta -= 1
                        
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 2:
                        self.pressed_mid_clic = True                    
                    elif event.button == 3:
                        self.pressed_right_clic = True 
                    elif event.button == 1:
                        self.pressed_left_clic = True
                    
            '''Calling Display functions'''
            self.interface.screen.blit(black_bg,(0,0))
            self.player.set_action('none')
            self.interface.view_solarsys(self.player,(config.Config.screen_w/2,config.Config.screen_h/2))
            self.interface.event_popup(self.event_manager.active_events,self.player)    
            self.interface.final_overlay(self.player) #will only display messages when USEREVENT+2 has occured
            fn.display_txt(str(len(self.all_planets)),'Lucida Console',16,(200,200,0),self.interface.screen,(20,20))
            fn.display_txt('score: '+str(self.get_score()),'Lucida Console',16,(200,200,0),self.interface.screen,(20,40))
            fn.display_txt('Current Position: '+str(fn.sum_tulp(pygame.mouse.get_pos(),(-self.interface.map_offset_x,-self.interface.map_offset_y))),'Lucida Console',16,(200,200,0),self.interface.screen,(20,config.Config.screen_h-20))

            self.player.ai.train()
            pygame.display.update()
            
            '''Checks if game ends'''
            if self.player.rp  == 0: self.game_over_screen()
            
    def get_score(self):
        total_explored_planets = sum([1 for planet in self.all_planets if self.player.check_exploration(planet)])
        return total_explored_planets + self.year
        
    def game_over_screen(self):
        while True:
            self.clock.tick(60) #needed to slow game down
            for event in pygame.event.get(): #setting up quit
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    print 'has quit'
                elif event.type == pygame.KEYDOWN and (event.key == K_ESCAPE or event.key == K_RETURN):
                    pygame.quit()
                    sys.exit()
                    print 'has quit' 
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
            self.interface.screen.blit(pygame.transform.smoothscale(data.Data.backgrounds['game_over'],(config.Config.screen_w,config.Config.screen_h)),(0,0))
            fn.display_txt('score: '+str(self.get_score()),'Lucida Console',50,(200,200,0),self.interface.screen,(config.Config.screen_w/2,config.Config.screen_h/4),True)
            
            pygame.display.update()
            
    def start_menu(self):
        '''set up'''
        pygame.time.set_timer(USEREVENT + 1, 1000) # 1 event every 1 second
        show_press_to_start = True
        
        while True:
            self.clock.tick(60) #needed to slow game down
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
                elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                    self.instruction_menu()                    
                elif event.type == USEREVENT + 1:
                    show_press_to_start = False if show_press_to_start else True
                    

            '''Calling Display functions'''
            self.interface.screen.blit(pygame.transform.smoothscale(data.Data.backgrounds['game_over'],(config.Config.screen_w,config.Config.screen_h)),(0,0))
            fn.display_txt('FAR AND AWAY','Lucida Console',80,(200,200,0),self.interface.screen,(config.Config.screen_w/2,config.Config.screen_h/5),True)

            if show_press_to_start:
                fn.display_txt('PRESS ENTER TO START GAME','Lucida Console',50,(200,200,0),self.interface.screen,(config.Config.screen_w/2,config.Config.screen_h/2),True)
    
            pygame.display.update()
            
    def instruction_menu(self):
        '''set up'''
        pygame.time.set_timer(USEREVENT + 1, 1000) # 1 event every 1 second
        show_press_to_start = True
        black_bg = pygame.Surface((config.Config.screen_w,config.Config.screen_h))
        black_bg.fill((0,0,0))
        black_bg.set_alpha(100)        
        
        
        while True:
            self.clock.tick(60) #needed to slow game down
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
                elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                    self.planets_info()                    
                elif event.type == USEREVENT + 1:
                    show_press_to_start = False if show_press_to_start else True
                    

            '''Calling Display functions'''
            self.interface.screen.blit(pygame.transform.smoothscale(data.Data.backgrounds['game_over'],(config.Config.screen_w,config.Config.screen_h)),(0,0))
            self.interface.screen.blit(black_bg,(0,0))
            self.interface.screen.blit(pygame.transform.smoothscale(data.Data.misc['instructions'],(config.Config.screen_w,config.Config.screen_h)),(0,0))

            if show_press_to_start:
                fn.display_txt('PRESS ENTER TO START GAME','Lucida Console',20,(200,200,0),self.interface.screen,(config.Config.screen_w/2,config.Config.screen_h-25),True)
    
            pygame.display.update()
            
    def planets_info(self):
        '''set up'''
        pygame.time.set_timer(USEREVENT + 1, 1000) # 1 event every 1 second
        show_press_to_start = True
        black_bg = pygame.Surface((config.Config.screen_w,config.Config.screen_h))
        black_bg.fill((0,0,0))
        black_bg.set_alpha(100)        
        
        
        while True:
            self.clock.tick(60) #needed to slow game down
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
                elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
                    self.run()                    
                elif event.type == USEREVENT + 1:
                    show_press_to_start = False if show_press_to_start else True
                    

            '''Calling Display functions'''
            self.interface.screen.blit(pygame.transform.smoothscale(data.Data.backgrounds['game_over'],(config.Config.screen_w,config.Config.screen_h)),(0,0))
            self.interface.screen.blit(black_bg,(0,0))
            self.interface.screen.blit(pygame.transform.smoothscale(data.Data.misc['planets_info'],(config.Config.screen_w,config.Config.screen_h)),(0,0))

            if show_press_to_start:
                fn.display_txt('PRESS ENTER TO START GAME','Lucida Console',20,(200,200,0),self.interface.screen,(config.Config.screen_w/2,config.Config.screen_h-25),True)
    
            pygame.display.update()        
        