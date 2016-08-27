# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:06:08 2016

@author: julien
"""
import pygame
import matplotlib as plt
import functions as fn
from config import*
from data import*


class Interface(object):
    def __init__(self,game):
        self.game = game
        '''setting screen up'''
        self.screen = Config.screen
        self.selected = None
        '''message manager'''
        self.messages = [] # contains angles at which to blit  and the blitpos as a tulp
        self.message_disp_time = 0
        self.display_event = False
        '''planet discovery arrow'''
        self.arrows = []
        self.arrow_disp_time = 0
        '''variables'''
        self.hovered = None
        self.helpers = False
        self.map_offset_x = 0
        self.map_offset_y = 0
        
    def get_map_offset(self):
        mx,my = pygame.mouse.get_pos()
        delta = 10
        if mx <= 10:
            self.map_offset_x += delta
        elif mx >= Config.screen_w-10:
            self.map_offset_x -= delta
            
        if my <= 10:
            self.map_offset_y += delta
        elif my >= Config.screen_h-10:
            self.map_offset_y -= delta   

    def centered_offset(self,offset):
        x,y = offset[0],offset[1]
        return (self.screen.get_rect().centerx-x,self.screen.get_rect().centery-y)
        
    def final_overlay(self,explorer):
        self.message_display()
        '''blit pause status'''
        if self.game.pause: fn.display_txt('Game Paused','Impact',16,(0,255,0),self.screen,(int(Config.screen_w*0.75),15))
        '''blit time in months'''
        fn.display_txt('Current Month: {}'.format(self.game.month),'Lucida Console',16,(0,255,0),self.screen,(Config.screen_w/2,15))
        '''blit the player's points'''
        fn.display_txt('Your KP: {}'.format(explorer.kp),'Lucida Console',16,(0,255,0),self.screen,(Config.screen_w-350,Config.screen_h-30))
        fn.display_txt('Your RP: {}'.format(explorer.rp),'Lucida Console',16,(0,255,0),self.screen,(Config.screen_w-150,Config.screen_h-30))                    
        '''display arrows'''
        self.show_arrows()
        
    def view_solarsys(self,explorer,offset):
        ''' 
            !!! draw line between discovered planets
            !!! blit discovered planets
            !!! blit red halo to unexplored
            !!! blit green halo to player's location
            '''
        planets_to_blit = []
        for p in explorer.get_logbook_planets():
            if explorer.check_discovery(p):
                if explorer.check_exploration(p):
                    [pygame.draw.line(self.screen, (0,250,0), fn.sum_tulp(p.pos,(self.map_offset_x,self.map_offset_y)), fn.sum_tulp(p2.pos,(self.map_offset_x,self.map_offset_y)), 5) for p2 in p.planets_in_SOF if explorer.check_exploration(p2)]
                planets_to_blit.append(p)
                self.check_hovered(p)
        
        #need another loop to ensure planets are blitted in front of all the lines        
        for p in planets_to_blit:
            if explorer.check_discovery(p):
                if not explorer.check_exploration(p):
                    pygame.draw.circle(self.screen, (255,0,0), fn.sum_tulp(p.pos,(self.map_offset_x,self.map_offset_y)), int(p.rect.w*0.6), 0)
                if explorer.location == p.name:
                    pygame.draw.circle(self.screen, (0,255,0), fn.sum_tulp(p.pos,(self.map_offset_x,self.map_offset_y)), int(p.rect.w*0.75), 0)
                fn.blitc(self.screen, Data.images_planets[p.img_ref], fn.sum_tulp(p.pos,(self.map_offset_x,self.map_offset_y)))
                                
            '''Mouse interaction'''
            self.solar_sys_mouse_interaction(explorer,p)
            
        '''blitting planet info'''
        self.view_planet(explorer)
    
    def solar_sys_mouse_interaction(self,explorer,planet):
        ''' None -> None
            Handles mouse interaction when in solar system view
            SE: -player exploration
                -player visit
                -search is SOF'''
                
        #offsets the rectangle of the planet by the map offset        
        offset_rect = pygame.Rect(fn.sum_tulp(planet.rect.topleft,(self.map_offset_x,self.map_offset_y)),(planet.rect.w,planet.rect.h))
        
        #checks for mouse colision with the planet and if the map is active
        if offset_rect.collidepoint(pygame.mouse.get_pos()) and self.game.map_active:
            if pygame.mouse.get_pressed()[0] and self.game.pressed_left_clic:
                #choses between visit and exploration
                explorer.select_displacement(planet)
                    
            elif pygame.mouse.get_pressed()[2] and self.game.pressed_right_clic:
                planet.search_in_SOF(explorer, True)
                self.game.pressed_right_clic = False
                
    def check_hovered(self, planet):
        offset_rect = pygame.Rect(fn.sum_tulp(planet.rect.topleft,(self.map_offset_x,self.map_offset_y)),(planet.rect.w,planet.rect.h))
        if offset_rect.collidepoint(pygame.mouse.get_pos()) : self.hovered = planet
     
            
    def view_planet(self,explorer):
        ''' if the planet is hovered upon by the mouse, information on it is
            blitted to the screen'''
        if self.hovered is not None:
            planet = self.hovered
            
            m_x,m_y = pygame.mouse.get_pos()
            offset_w,offset_h = 300,220
            
            if m_x <= Config.screen_w-offset_w and m_y <= Config.screen_h-offset_h:
                blitpos = (m_x,m_y)
            elif m_x > Config.screen_w-offset_w and m_y > Config.screen_h-offset_h:
                blitpos = (m_x-offset_w,m_y-offset_h)
            elif m_x > Config.screen_w-offset_w:
                blitpos = (m_x-offset_w,m_y)
            elif m_y > Config.screen_h-offset_h:
                blitpos = (m_x,m_y-offset_h)
                
            '''blits bg '''
            tooltip_bg = pygame.Surface((offset_w,offset_h))
            tooltip_bg.set_alpha(125)
            self.screen.blit(tooltip_bg,blitpos)
            
            ''' blit all the planet's stats to the screen'''
            #update's travel information for the planet
            explorer.logbook[planet.name].get_travel_info(explorer.logbook[explorer.location].instance[0],explorer.travel_bonus)
            if explorer.name in planet.explored_by:
                info_ls = [
                planet.name,
                planet.pos,
                planet.discovered_by,
                planet.explored_by,
                '{} (+{}/month)'.format(planet.disc_kp,fn.kp_formula(planet,self.game.month+1,explorer.logbook[planet.name].time_of_exploration,explorer.kp,explorer.kp_bonus)),
                '{} (+{}/month)'.format(planet.disc_rp,fn.rp_formula(planet,self.game.month+1,explorer.logbook[planet.name].time_of_exploration,explorer.rp_bonus)),
                explorer.logbook[planet.name].travel_cost,
                explorer.logbook[planet.name].travel_time]
            else:
                info_ls = [planet.name,planet.pos,explorer.name,'not explored', planet.disc_kp,planet.disc_rp,
                           fn.exploration_cost_formula(len([log for log in explorer.logbook.itervalues() if log.is_explored]),explorer.kp,planet.disc_kp) + explorer.logbook[planet.name].travel_cost,
                            explorer.logbook[planet.name].travel_time]
            x,y = blitpos[0],blitpos[1]
            
            cats = {0: 'Planet Id: ', 1:'Planet Location:  ', 2:'Discovered by: ', 3:'Explored by: ', 4:'KP: ', 5:'RP ', 6:'Travel cost: ', 7:'Travel time: '}
            
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
                
            self.hovered = None

                
    def add_message(self,msg,disp_time):
        self.messages.append(msg)
        self.message_disp_time += disp_time #adds x seconds to the message timer
        
    def arrow_param(self,planet):
        offset_x = planet.rect.centerx+self.map_offset_x
        offset_y = planet.rect.centery+self.map_offset_y
        
        d = 60        
        
        if offset_x > Config.screen_w:
            if offset_y > Config.screen_h:
                return (-135,(Config.screen_w-d,Config.screen_h-d))
            elif offset_y < 0:
                return (-45,(Config.screen_w-d,d))
            return (-90,(Config.screen_w-d,Config.screen_h/2))
        elif offset_x < 0:
            if offset_y > Config.screen_h:
                return (135,(d,Config.screen_h-d))
            elif offset_y < 0:
                return (45,(d,d))
            return (90,(d,Config.screen_h/2))
        elif offset_y > Config.screen_h:
            return (180, (Config.screen_w/2,Config.screen_h-d))
        elif offset_y < 0 :
            return (0, (Config.screen_w/2,d))
            
        else:
            return False
            
    def add_arrow(self,(angle,pos),disp_time):
        self.arrows.append((angle,pos))
        self.arrow_disp_time += disp_time
        
    def show_arrows(self):
        if self.arrow_disp_time > 0:
            for angle,pos in self.arrows:
                img = pygame.transform.rotate(Data.misc['arrow'],angle)
                fn.blitc(self.screen,img,pos)
                
        if self.arrow_disp_time <= 0:
            self.arrows = []
        
    def message_display(self):
        if self.display_event == True: #displays on call to USEREVENT+2 in game.py
            '''removes 1 second from the display timer'''
            self.message_disp_time -= 1
            if self.message_disp_time < 0: self.message_disp_time = 0
        self.display_event = False #disable the display until the next call to USEREVENT+2 in game.py

        if len(self.messages) >= 15: self.messages.pop(0) #ensure message list isn't too long

        if self.message_disp_time > 0 and self.helpers:
            '''displays messages'''
            x = 0
            for msg in self.messages:
                fn.display_txt(msg,'Lucida Console',16,(0,255,0),self.screen,(int(Config.screen_w*0.75),50+x))
                x += 25
        elif self.message_disp_time <= 0:
            self.messages = [] #if the message timer reaches 0 the messages are deleted
            
        if self.helpers: self.graph_display()
            
            
    def graph_display(self):
        rp_pts = []
        kp_pts = []
        for month in range(1,11):
            next_month_rp = 0
            next_month_kp = 0
            for log in (log for log in self.game.player.logbook.itervalues() if log.is_explored):
                next_month_kp += fn.kp_formula(log.instance[0],self.game.month+month,log.time_of_exploration,self.game.player.kp,self.game.player.kp_bonus)
                next_month_rp += fn.rp_formula(log.instance[0],self.game.month+month,log.time_of_exploration,self.game.player.rp_bonus)
            next_month_rp -= self.game.player.monthly_rp_expense
            rp_pts.append((month,next_month_rp))
            kp_pts.append((month,next_month_kp))
        '''transfer data into graph compatible data'''
        data_kp,ylab_kp,xlab_kp = fn.get_graph_data(kp_pts,(100,300),(400,250),30)
        data_rp,ylab_rp,xlab_rp = fn.get_graph_data(rp_pts,(100,300),(400,250),15)
        '''blit graph'''
        self.screen.blit(Data.backgrounds['graph'],(45,25))
        pygame.draw.lines(self.screen, (0,0,255), False, data_kp, 2)
        pygame.draw.lines(self.screen, (255,0,0), False, data_rp, 2)
        [fn.display_txt(val,'Lucida Console',16,(0,0,255),self.screen,(x,y)) for x,y,val in ylab_kp]
        [fn.display_txt(val,'Lucida Console',16,(255,0,0),self.screen,(x,y)) for x,y,val in ylab_rp]
        [fn.display_txt(val,'Lucida Console',16,(0,255,0),self.screen,(x,y)) for x,y,val in xlab_rp]
        
    def event_popup(self,event_list,explorer):
        '''get event from event manager and assign it locally'''
        events = event_list
        for event in events:
            self.game.pause = True
            event.update()
            '''blits popup bg '''
            tooltip_bg = Data.backgrounds['event']
            tooltip_bg.set_alpha(50)
            tooltip_rect = tooltip_bg.get_rect()
            fn.blitc(self.screen,tooltip_bg,(Config.screen_w/2,Config.screen_h/2))
            '''blit event's img'''
            fn.blitc(self.screen,Data.event_images[event.name],(Config.screen_w/2,Config.screen_h/2-115)) #-50 to adjust image to pupup bg
            '''blit event's text'''
            text_zone = pygame.Rect((Config.screen_w/2-300,Config.screen_h/2+50),(tooltip_rect.w-50,300))
            fn.drawText(self.screen,event.text,(0,255,0),text_zone, pygame.font.SysFont('Lucida Console', 15))
            '''button actions'''
            okay_but = Button('Approve',event,Config.screen_w/2+15,Config.screen_h/2+210)
            okay_but.check_select()
            okay_but.display(self.screen)
            
            if okay_but.selected and self.game.pressed_left_clic:
                self.game.pause = False
                event.execute()
                self.game.event_manager.active_events.remove(event)
                self.game.map_active = True
                self.game.pressed_left_clic = False
            break #only does the function for one event at a time

            
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

                