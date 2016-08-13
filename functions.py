# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:00:25 2016

@author: julien
"""
import pygame
import random
import numpy as np
from math import pi,radians,sin,cos

def check_collision(item,list):
    for x in list:
        if item.rect.colliderect(x.rect):
            return True
    return False

def dist(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5

def kp_formula(planet,game_time,exploration_time,bonus):
    dt = game_time - exploration_time if game_time != exploration_time else 1
    return int(abs(np.sin(dt)*planet.disc_kp*np.exp(-0.025*dt))+bonus)
    
def rp_formula(planet,game_time,exploration_time,bonus):
    dt = game_time - exploration_time if game_time != exploration_time else 1
    return int(planet.disc_rp + bonus * np.exp(-( planet.disc_rp /500)*dt)*(np.cos(2*np.pi*dt)))
    
def point_pos(pt, d, theta_rad):
    x0, y0 = pt
    #theta_rad = pi/2 - radians(theta)
    return (int(x0 + d*cos(theta_rad)), int(y0 + d*sin(theta_rad)))  
    
def travel_formula(steps):
    return steps*steps
    
def choice_weighted(list):
    weighted_choices = list#[Event('Red',8), Event('Blue', 2)]
    population = [event for event in weighted_choices for i in range(event.weight)]
    return random.choice(population)
    
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
    
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    #rect = Rect(rect)
    y = rect.top
    lineSpacing = -2
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    #blit button bg
    if bkg:
        bg = pygame.transform.smoothscale(bkg, (rect.width+5, rect.height+15))
        surface.blit(bg, sum_tulp((rect.left, y),(-5,-5)))
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
 
    return text



    
