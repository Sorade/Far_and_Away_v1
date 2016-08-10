# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 18:42:16 2016

@author: Julien
"""
import pygame

def img_import(str,dim):
    img = pygame.image.load('data\\{}'.format(str)).convert_alpha()
    return pygame.transform.smoothscale(img,dim)


class Data(object):
    '''image imports'''
    image_venus = pygame.image.load('data\\Venus.png').convert_alpha()
    image_venus = pygame.transform.smoothscale(image_venus,(50,50))
    
    
    '''image dictionaries'''
    backgrounds = {'event' : pygame.image.load('data\\event_popup.png').convert_alpha()}    
    
    images_planets = {'Venus' : image_venus}
    
    event_images = {'Precious Ore Discovered': img_import('mining_event.png',(550,310))}
    
    '''planet names'''
    planet_names = ['Stella','Orma','Rupa','Gamma','Ortia','Zima','Fita','Bella','Ursa']
    
    