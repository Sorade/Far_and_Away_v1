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
    backgrounds = {'event' : pygame.image.load('data\\event_popup.png').convert_alpha(),
                    'graph': img_import('graph_bg_green.png',(500,350)), 
                    'game_over': pygame.image.load('data\\game_over_bg.jpg').convert_alpha()}
                    
    misc = {'arrow' : img_import('arrow.png',(100,50)),
            'instructions': pygame.image.load('data\\instructions.png').convert_alpha()}
    
    images_planets = {'Venus' : image_venus,
                      'Earth' : img_import('earth.png',(50,50)),
                        'Habitable_world' : img_import('habitable_world.png',(50,50)),
                        'Frozen' : img_import('frozen.png',(50,50)),
                        'Alien_hive' : img_import('alien_hive.png',(50,50)),
                        'Jungle' : img_import('jungle_world.png',(50,50)) }
    
    event_images = {'Precious Ore Discovered': img_import('mining_event.png',(550,310)),
                    'Raiders': img_import('raider_event.png',(550,310)),
                    'Storm': img_import('storm_event.png',(550,310)),
                    'Old Archives': img_import('old_archives_event.png',(550,310)),
                    'Rebellion': img_import('rebellion.png',(550,310)),
                    'Alien Tech': img_import('alien_tech.png',(550,310)),
                    'Astronomer': img_import('astronomer.png',(550,310)),
                    'Contamination': img_import('contamination.jpg',(550,310)),
                    'Cure': img_import('cure.jpg',(550,310))}
                    
    '''music & sounds'''
    musics = {'theme' : 'data\\musictheme.ogg'}
    
    
    