# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:06:08 2016

@author: julien
"""
import pygame
import functions as fn
from config import*
from data import*

class Interface(object):
    def __init__(self,game):
        self.game = game
        '''setting screen up'''
        self.screen = Config.screen
        self.menu_bg = pygame.Surface((Config.screen_w,Config.screen_h))
        self.menu_bg.set_alpha(150)
        self.selected = None
        '''message manager'''
        self.messages = []
        self.message_disp_time = 0
        self.display_event = False
        
    def centered_offset(self,offset):
        x,y = offset[0],offset[1]
        return (self.screen.get_rect().centerx-x,self.screen.get_rect().centery-y)
        
    def final_overlay(self):
        self.message_display()
        '''blit pause status'''
        if self.game.pause: fn.display_txt('Game Paused','Impact',16,(0,255,0),self.screen,(int(Config.screen_w*0.75),15))
        '''blit time in months'''
        fn.display_txt('Current Month: {}'.format(self.game.month),'Lucida Console',16,(0,255,0),self.screen,(Config.screen_w/2,15))
        '''blit the player's points'''
        fn.display_txt('Your KP: {}'.format(self.game.player.kp),'Lucida Console',16,(0,255,0),self.screen,(Config.screen_w/2,50))
        fn.display_txt('Your RP: {}'.format(self.game.player.rp),'Lucida Console',16,(0,255,0),self.screen,(Config.screen_w/2,75))                    

        
    def view_solarsys(self,offset,planet):
        planets_to_blit = []
        for p in self.game.all_planets:
            if self.game.player.logbook[p.name].is_discovered == True:
                [pygame.draw.line(self.screen, (0,250,0), p.pos, p2.pos, 5) for p2 in p.planets_in_SOF if self.game.player.logbook[p2.name].is_explored and self.game.player.logbook[p.name].is_explored]
                planets_to_blit.append(p)
                
        for p in planets_to_blit:
            if p.rect.collidepoint(pygame.mouse.get_pos()):# and pygame.mouse.get_pressed()[0]:
                self.view_planet()
            if self.game.player.logbook[p.name].is_discovered == True:
                if self.game.player.logbook[p.name].is_explored == False:
                    pygame.draw.circle(self.screen, (255,0,0), p.pos, int(p.rect.w*0.6), 0)
                if self.game.player.location == p.name:
                    pygame.draw.circle(self.screen, (0,255,0), p.pos, int(p.rect.w*0.75), 0)
                fn.blitc(self.screen, Data.images_planets[p.img_ref], p.pos)
                
            '''Mouse interaction'''
            if p.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[2]:
                    if self.game.player.logbook[p.name].is_explored == False:
                        p.explore(self.game.player)
                    else:
                        p.visit(self.game.player)
                elif pygame.mouse.get_pressed()[1] and self.game.pressed_mid_clic == True:
                    p.search_in_SOF(self.game.player,True,30)
                    self.game.pressed_mid_clic = False
              
            
    def view_planet(self):
        planet_list = [planet for planet in (log.instance[0] for log in self.game.player.logbook.values()) if planet.rect.collidepoint(pygame.mouse.get_pos())]
        if len(planet_list) > 0: 
            planet = planet_list[0]

            '''make buttons'''
            go_to_button = Button('Travel to',planet,50,Config.screen_h-50)
            search_button = Button('Search SOF',planet,150,Config.screen_h-50)
            
            buttons = []
            buttons.extend([go_to_button,search_button])
            
            ''' blit all the planet's stats to the screen'''
            if self.game.player.name in planet.explored_by:
                info_ls = [
                planet.name,
                planet.pos,
                planet.discovered_by,
                planet.explored_by,
                '{} (+{}/month)'.format(planet.disc_kp,fn.kp_formula(planet,self.game.month,self.game.player.logbook[planet.name].time_of_exploration)),
                '{} (+{}/month)'.format(planet.disc_rp,fn.rp_formula(planet,self.game.month,self.game.player.logbook[planet.name].time_of_exploration)),
                fn.travel_formula(fn.steps(self.game.player.logbook[self.game.player.location].instance[0].pos,planet.pos,self.game.dx,self.game.dy))]
            else:
                info_ls = [planet.name,planet.pos,self.game.player.name,'not explored', planet.disc_kp,planet.disc_rp,10+fn.travel_formula(fn.steps(self.game.player.logbook[self.game.player.location].instance[0].pos,planet.pos,self.game.dx,self.game.dy))]
            x,y = pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]
            
            cats = {0: 'Planet Id: ', 1:'Planet Location:  ', 2:'Discovered by: ', 3:'Explored by: ', 4:'KP: ', 5:'RP ', 6:'Travel cost: '}
            
            count = 0
            for stat in info_ls:
                if type(stat) is list:
                    to_blit = ', '.join(stat)
                else:
                    to_blit = stat                
                to_blit = cats[count]+ str(to_blit)
                fn.display_txt(to_blit,'Lucida Console',16,(0,255,0),self.screen,(x,y))
                y += 20
                count += 1
                
            for but in buttons:
                but.check_select()
                but.display(self.screen)
            
            if go_to_button.selected == True:
                if self.game.player.logbook[planet.name].is_explored == False:
                    planet.explore(self.game.player)
                else:
                    planet.visit(self.game.player)
                    
            elif search_button.selected == True and self.game.pressed_left_clic == True:
                planet.search_in_SOF(self.game.player,True,30)
                self.game.pressed_left_clic = False
                    
    def add_message(self,msg,disp_time):
        self.messages.append(msg)
        self.message_disp_time += disp_time #adds x seconds to the message timer
        
    def message_display(self):
        if self.display_event == True:
            '''removes 1 second from the display timer'''
            self.message_disp_time -= 1
            if self.message_disp_time < 0: self.message_disp_time = 0

        if len(self.messages) >= 15: self.messages.pop(0) #ensure message list isn't too long

        if self.message_disp_time > 0:
            '''displays messages'''
            x = 0
            for msg in self.messages:
                fn.display_txt(msg,'Lucida Console',16,(0,255,0),self.screen,(Config.screen_w/2,Config.screen_h/3+x))
                x += 25
        else:
            self.messages = [] #if the message timer reaches 0 the messages are deleted
        self.display_event = False #disable the display until the next call to USEREVENT+2 in game.py
            

        
        
               
class Button(pygame.sprite.Sprite):
    def __init__(self, text, binded, x,y):
        super(Button, self).__init__()
        self.text = text
        self.image = pygame.Surface((100,50))
        self.image.fill((100,100,100))
        self.text_pos = ((x+75/2),(y+75/2))
        self.rect2 = 0
        self.txt_color = (0,0,0)
        self.binded = binded
        
       
        self.smallText = pygame.font.Font("freesansbold.ttf",12)
        self.textSurf = self.smallText.render(self.text, True, self.txt_color)
        self.rect2 = self.textSurf.get_rect()
        self.rect2.center = self.text_pos
        self.image = pygame.transform.scale(self.image, (int(self.rect2.width*1.5),int(self.rect2.height*3)))
        self.rect = pygame.Rect(x,y,self.image.get_rect().width,self.image.get_rect().height)
        
        self.selected = False
        self.m_released = True
        
    def check_select(self):
        m_pos = pygame.mouse.get_pos()
        over_but = self.rect.collidepoint(m_pos) 
        
        if pygame.mouse.get_pressed()[0] ==1 and over_but == 1 and self.selected == False and self.m_released == True:
            self.selected = True
            self.txt_color = (0,200,0)
            self.m_released = False
            
        elif pygame.mouse.get_pressed()[0] == 1 and over_but == 1 and self.selected == True and self.m_released == True:
            self.selected = False
            self.txt_color = (0,0,0)
            self.m_released = False
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.m_released = True
            
            
            
    def display(self,dest_surf):
        #self.surface = pygame.draw.rect(var.screen, self.color , self.rect)
        dest_surf.blit(self.image,self.rect)
        dest_surf.blit(self.textSurf, pygame.Rect(self.rect[0]+(self.rect.centerx-self.rect[0])*0.4,self.rect[1]+self.rect[3]/4,self.rect[2],self.rect[3])) #Rect(self.rect[0]+self.rect[2]/8,self.rect[1]+20,self.rect[2],self.rect[3])

                