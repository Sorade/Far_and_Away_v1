# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 18:42:16 2016

@author: Julien
"""
import pygame

class Data(object):
    '''image imports'''
    image_venus = pygame.image.load('data\\Venus.png').convert_alpha()
    image_venus = pygame.transform.smoothscale(image_venus,(50,50))
    
    '''image dictionaries'''
    images_planets = {'Venus' : image_venus}
    
    '''planet names'''
    planet_names = ['Stella','Orma','Rupa','Gamma','Ortia','Zima','Fita','Bella','Ursa']