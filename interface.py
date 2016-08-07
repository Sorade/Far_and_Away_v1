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
        
        self.selected = None
        
    def centered_offset(self,offset):
        x,y = offset[0],offset[1]
        return (self.screen.get_rect().centerx-x,self.screen.get_rect().centery-y)
        
    def view_solarsys(self,offset,planet):
        planets_to_blit = []
        for p in self.game.all_planets:
            if self.game.player.logbook[p.name].is_discovered == True:
                [pygame.draw.line(self.screen, (0,255,0), p.pos, p2.pos, 5) for p2 in p.planets_in_SOF if self.game.player.logbook[p2.name].is_explored and self.game.player.logbook[p.name].is_explored]
                planets_to_blit.append(p)
                
        for p in planets_to_blit:
            if p.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.game.map_mode = False
                self.game.planet_mode = True
                self.selected = p
                return
            if self.game.player.logbook[p.name].is_discovered == True:
                fn.blitc(self.screen, Data.images_planets[p.img_ref], p.pos)
                
              
            
    def view_planet(self,planet):
        self.screen.blit(self.menu_bg,(0,0))
        '''make buttons'''
        go_to_button = Button('Travel to',planet,50,Config.screen_h-50)
        search_button = Button('Search SOF',planet,150,Config.screen_h-50)
        view_solarsys_but = Button('View Solar System',planet,350,Config.screen_h-50)
        
        buttons = []
        buttons.extend([go_to_button,view_solarsys_but,search_button])
        
        ''' blit all the planet's stats to the screen'''
        if self.game.player.name in planet.explored_by:
            info_ls = [planet.name,planet.pos,planet.discovered_by,planet.explored_by,planet.disc_kp,planet.disc_rp]
        else:
            info_ls = [planet.name,planet.pos,self.game.player.name,'not explored', planet.disc_kp,planet.disc_rp]
        x,y = 50,50
        
        cats = {0: 'Planet Id: ', 1:'Planet Location:  ', 2:'Discovered by: ', 3:'Explored by: ', 4:'KP: ', 5:'RP '}
        
        count = 0
        for stat in info_ls:
            if type(stat) is list:
                to_blit = ', '.join(stat)
            else:
                to_blit = stat
            to_blit = cats[count]+ str(to_blit)
            fn.display_txt(to_blit,'impact',16,(0,255,0),self.screen,(x,y))
            y += 20
            count += 1
            
        '''blit the player's points'''
        fn.display_txt('Your KP: {}'.format(self.game.player.kp),'impact',16,(0,255,0),self.screen,(Config.screen_w/2,50))
        fn.display_txt('Your RP: {}'.format(self.game.player.rp),'impact',16,(0,255,0),self.screen,(Config.screen_w/2,75))                    

                        
        for but in buttons:
            but.check_select()
            but.display(self.screen)
        
        if go_to_button.selected == True:
            if self.game.player.logbook[planet.name].is_explored == False:
                planet.explore(self.game.player)
            else:
                planet.visit(self.game.player)
                
        elif search_button.selected == True and self.game.pressed_left_clic == True:
            planet.search_in_SOF(self.game.player,True)
            self.game.pressed_left_clic = False
                
        elif view_solarsys_but.selected == True:
            self.game.planet_mode = False
            self.game.map_mode = True
        
               
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

                