# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:00:25 2016

@author: julien
"""
import pygame

def dist(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5
    
def sum_tulp(t1,t2):
    return (t1[0]+t2[0],t1[1]+t2[1])
    
def blitc(dest,surface,blitpos): #blitpos is the center of the image
    rect = surface.get_rect()
    corrected_blitpos = (blitpos[0]-rect.w/2,blitpos[1]-rect.h/2)
#    dx,dy = blitpos[0]-rect.centerx,blitpos[1]-rect.centery
#    corrected_blitpos = sum_tulp(rect.topleft, (dx,dy))
    
    dest.blit(surface, corrected_blitpos)
    
def display_txt(txt,font,size,color,surface,pos):
    txt = str(txt)
    font = pygame.font.SysFont(font, size, bold=False, italic=False)
    text = font.render(txt, True, color)
    textpos = text.get_rect()
    textpos.topleft = pos
    surface.blit(text, textpos)  
