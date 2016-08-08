# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 11:45:26 2016

@author: julien
"""

class Logbook(object):
    def __init__(self, body, is_discovered, is_explored):
        self.instance = [body]
        self.is_discovered = is_discovered
        self.is_explored = is_explored
        self.time_of_exploration = None
        