# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 21:42:15 2016

@author: Julien
"""

import pygame
from sprite import MySprite
from data import Data
import functions as fn


class Ship(MySprite):
    def __init__(self, explorer):
        super(Ship, self).__init__()
        self.img_ref_void = 'ship_void'
        self.img_ref_full = 'ship'
        self.orientation = 0
        self.explorer = explorer
        
    def point_to_mouse(self,pos):
        self.orientation = fn.angle_clockwise(pos,(pos[0],pos[1]-10), pygame.mouse.get_pos())
        
    def blit(self,dest_surf,pos):
        self.point_to_mouse(pos)
        if self.explorer.type == 'human':
            image = pygame.transform.rotate(Data.misc[self.img_ref_void], self.orientation)
            image_color = pygame.transform.rotate(Data.misc[self.img_ref_full], self.orientation)
        else:
            image = Data.misc[self.img_ref_void]
            image_color = Data.misc[self.img_ref_full]
            
        fn.color_surface(image_color,self.explorer.color)
        fn.blitc(dest_surf,image_color,pos)
        fn.blitc(dest_surf,image,pos)
