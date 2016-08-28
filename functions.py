# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 10:00:25 2016

@author: julien
"""
import pygame
import random
import numpy as np
from math import pi,radians,sin,cos,acos

'''takes a list of tulpe values and plots them in a graph
of which the bottom left corner is set as o_pos and has 
a width and height defined by the dim tulpe = to (w,h)'''
def get_graph_data(list,o_pos, dim,  lab_offset):
    ox,oy = o_pos
    w,h = dim
    xls,yls = [x-1 for x,y in list], [y for x,y in list]
    dx = float(w)/(max(xls)-min(xls)) if max(xls)-min(xls) != 0 else w#float(w)/max(xls)
    dy = float(h)/(max(yls)-min(yls)) if max(yls)-min(yls) != 0 else h#float(h)/max(yls)
    data_pts = [(int(ox+(x-1)*dx),int(oy-(y-min(yls))*dy)) for x,y in list]
    #need to add a bg here
    
    #y axis labels
    ylab_pts = [(ox-lab_offset,int(oy-(y-min(yls))*dy),y) for x,y in list] # (x,y,val)
    #x axis labels
    xlab_pts = [(int(ox+(x-1)*dx),oy+lab_offset,x) for x,y in list]
    return data_pts,ylab_pts,xlab_pts

def check_collision(item,list):
    for x in list:
        if item.rect.inflate(100,100).colliderect(x.rect):
            return True
    return False

def dist(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5
    
def search_cost(planet_cat):
    cost = 0
    if planet_cat == 'Mining World' :    cost = 10
    if planet_cat == 'Habitable World' : cost = 8
    if planet_cat == 'Frozen World' :    cost = 15
    if planet_cat == 'Alien World' :     cost = 10
    if planet_cat == 'Jungle World' :    cost = 10
    return cost


def kp_formula(planet,game_time,exploration_time,explorer_kp,bonus):
    dt = game_time - exploration_time if game_time != exploration_time else 1
    return int(abs(np.sin(dt*1)*max(planet.disc_kp+bonus,0)*np.exp(-(explorer_kp/1000.)*dt))) 
    
def rp_formula(planet,game_time,exploration_time,bonus):
    dt = game_time - exploration_time if game_time != exploration_time else 1
#    return int((planet.disc_rp + bonus) * np.exp(-( planet.disc_rp/500)*dt)*(np.cos(2*np.pi*dt)))
    return int(abs(np.sin(dt)*max(planet.disc_rp+bonus,0)*np.exp(-0.025*dt)))
    
def exploration_cost_formula(nb_explored,exp_kp,disc_kp):
    return int(5+disc_kp+nb_explored*(nb_explored/(exp_kp+1)))
    
def travel_time(distance,travel_units):
    return int(distance/travel_units)
    
def point_pos(pt, d, theta_rad):
    x0, y0 = pt
    #theta_rad = pi/2 - radians(theta)
    return (int(x0 + d*cos(theta_rad)), int(y0 + d*sin(theta_rad)))
    
   
def travel_formula(travel_time):
    return int((travel_time)**2+2)

''' List -> Object
takes a list of object with a weight attribute and returns an object of this list randomly'''
def choice_weighted(list, a_class = False):
    weighted_choices = list#[Event('Red',8), Event('Blue', 2)]
    if a_class == False:
        population = [event for event in weighted_choices for i in range(event.weight)]
    else:
        population = [(angle_min,angle_max) for angle_min,angle_max,weight in weighted_choices for i in range(weight)]
    return random.choice(population)
    
#>>> weighted_choices = [('Red', 3), ('Blue', 2), ('Yellow', 1), ('Green', 4)]
#>>> population = [val for val, cnt in weighted_choices for i in range(cnt)]
#>>> random.choice(population)
#'Green'
    
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
    
def display_txt(txt,font,size,color,surface,pos,centered = False):
    txt = str(txt)
    font = pygame.font.SysFont(font, size, bold=False, italic=False)
    text = font.render(txt, True, color)
    textpos = text.get_rect()
    textpos.topleft = pos
    if centered: textpos.center = pos
    surface.blit(text, textpos)
    
def surname_gen(capitalize):
    start = ['Mo','Ma','Mu','Lo','La','Lu','Po','Pa','Pu']
    mid = ['lin','lom','sam','bam','for']
    end = ['son','va','p','ham','kol']
    
    word = ''
    for ls in [start,mid,end]:
        word += random.choice(ls)
        
    if (capitalize==True):
        word=word.capitalize()
    return word
    
    
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



    
