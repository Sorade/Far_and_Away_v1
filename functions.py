# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:00:25 2016

@author: julien
"""
import pygame
import random

def dist(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5

def kp_formula(planet,game_time,exploration_time):
    denom = game_time-exploration_time if game_time-exploration_time != 0 else 1
    return planet.disc_kp/denom
    
def rp_formula(planet,game_time,exploration_time):
    denom = game_time-exploration_time if game_time-exploration_time != 0 else 1
    return planet.disc_rp/denom
    
def travel_formula(steps):
    return steps*steps
    
    
def steps(point1, point2, dx, dy):
    x1,y1 = point1[0],point1[1]
    x2,y2 = point2[0],point2[1]
    return abs(x1-x2)/dx+abs(y1-y2)/dy
    
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
    
def name_gen(capitalize):

    bits=[]
    vowels="aeiou"
    letters="abcdefghijklmnopqrstuvwxyz"
    for ch in letters:
        for v in vowels:
            bits.append(ch+v)
    bits.remove("fu")
    bits.remove("hi")
    bits.remove("cu")
    bits.remove("co")
    bits.remove("mo")
    word=""
    rnd=len(bits)-1
    numOfBits=random.randint(2,3)
    for i in range(0,numOfBits):
        word=word+bits[random.randint(1,rnd)]
    word=word+letters[random.randrange(0,25)]
    if (capitalize==True):
        word=word.capitalize()
    return word


    
