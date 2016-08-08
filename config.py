# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 18:56:10 2016

@author: Julien
"""
import pygame

class Config(object):
    fullscreen = False
    screen_h = 700
    screen_w = 1200
    map_size = 'Huge'
    
    if fullscreen == True:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screenRES = pygame.display.Info()
        screen_w = screenRES.current_w
        screen_h = screenRES.current_h
    else:
        screen = pygame.display.set_mode((screen_w, screen_h), pygame.SRCALPHA, 32)

    