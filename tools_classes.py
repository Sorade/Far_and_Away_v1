# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 22:10:01 2016

@author: julien
"""
from math import pi
from data import Data

class Blinker:
    def __init__(self, img_ref, speed = 5):
        self.alpha = speed
        self.speed = speed
        self.img_ref = img_ref
        
    def blink(self):
        image = Data.images_planets[self.img_ref].convert_alpha()
        image.set_alpha(self.alpha)
        if -self.speed <= self.alpha < (250 - self.speed):
            self.speed *= 1
        else:
            self.speed *= -1
        self.alpha += self.speed
        return image

'''a class which enables to return weighted quadrants based on the
inverse amount of occurences in the given quadrant.
eg. if occurences are TP,TR,BR,BL = 1,1,0,2
the return weight would be 1,1,2,0
the angle list returns the angles determining the quadrant with the weighted value
[(angle_min,angle_max,weight),...]'''

class Quad(object):
    ref_x,ref_y = (0,0)
    conts = [0,0,0,0]
    weights = [0,0,0,0]
    angle_list = [0,0,0,0]
    
    '''Tulp,List -> None
takes a reference point and updates the class conts attribute to
represent in which quadrant the points in the list lie with respect
to the reference points'''
    
    @staticmethod    
    def get_content(ref_pt,pts_list):
        Quad.conts = [0,0,0,0]
        Quad.ref_x,Quad.ref_y = ref_pt
        for x,y in pts_list:
            if x < Quad.ref_x and y <= Quad.ref_y:
                Quad.conts[0] += 1 #TL
            elif x >= Quad.ref_x and y < Quad.ref_y:
                Quad.conts[3] += 1 #TR
            elif x > Quad.ref_x and y >= Quad.ref_y:
                Quad.conts[2] += 1 #BL
            else:
                Quad.conts[1] += 1 #BR
                
    @staticmethod            
    def get_weights():
        cont_max = max(Quad.conts)
        counter = 0
        for cont in Quad.conts:
            Quad.weights[counter] = cont_max - cont
            counter += 1
        #checks for none 0 max weight value
        if max(Quad.weights) == 0:
            for x in range(len(Quad.weights)):
                Quad.weights[x] = 1
                
        #builds an assigned list
        counter = 0
        for w in Quad.weights:
            Quad.angle_list[counter] = [counter*pi/2+0.7,(counter+1)*pi/2-0.7,w]
            counter += 1
            
    @staticmethod    
    def update_weights(ref_pt,pt):
        Quad.conts = [0,0,0,0]
        Quad.ref_x,Quad.ref_y = ref_pt
        x,y = pt
        if sum([Quad.angle_list[n][2] for n in range(4)]) > 1:
            if x < Quad.ref_x and y <= Quad.ref_y:
                Quad.angle_list[0][2] -= 1 #TL
            elif x >= Quad.ref_x and y < Quad.ref_y:
                Quad.angle_list[3][2] -= 1 #TR
            elif x > Quad.ref_x and y >= Quad.ref_y:
                Quad.angle_list[2][2] -= 1 #BL
            else:
                Quad.angle_list[1][2] -= 1 #BR
                
class States:
    def __init__(self):
        self.contaminated  = False
        self.has_new_weapons = False
        self.has_hyperdrive = False
        self.has_radar = False
          
