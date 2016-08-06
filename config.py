# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 18:56:10 2016

@author: Julien
"""
import pygame

class Config(object):
    fullscreen = False
    screen_h = 500
    screen_w = 800
    
    if fullscreen == True:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.SRCALPHA, 32)

    