# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 18:37:26 2016

@author: Julien
"""

import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, x):
        self.elements.append(x)
    
    def get(self):
        return self.elements.popleft()
        
        
def breadth_first_search(explorer, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None
    visited = []
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in explorer.logbook.fetch_neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current
                visited.append(next)
    return visited  

##example_graph = SimpleGraph()
##example_graph.edges = {
##    'A': ['B'],
##    'B': ['A', 'C', 'D'],
##    'C': ['A'],
##    'D': ['E', 'A'],
##    'E': ['B']
##}
#
#class SimpleGraph:
#    def __init__(self):
#        self.edges = {} #is explorer's logbook
#    
#    def neighbors(self, id): #id is planet name to fetch in explorer's logbook
#        return self.edges[id] #get's the planets_in_SOF
#        
#    def fetch_neighbors(self,planet_name):
#        return self[planet_name].instance[0].planets_in_SOF
#
##so graph = to my explored.planets
## and entries in edges = to my planets in SOF
#
#      
##--------------------------------------------------------------------
#        
##from implementation import *
#
#def breadth_first_search_1(graph, start):
#    frontier = Queue()
#    frontier.put(start)
#    visited = {}
#    visited[start] = True
#    
#    while not frontier.empty():
#        current = frontier.get()
#        print("Visiting %r" % current)
#        for next in graph.neighbors(current):
#            if next not in visited:
#                frontier.put(next)
#                visited[next] = True
#                
#                
##-------------------------------------------------------------------
#                #My Attempt
##-------------------------------------------------------------------
#                
#def breadth_first_search_my(graph, planet_name):
#    frontier = Queue()
#    frontier.put(planet_name)
#    visited = {}
#    visited[planet_name] = True
#    
#    while not frontier.empty():
#        current = frontier.get()
#        print("Visiting %r" % current)
#        for next in graph.neighbors(current):
#            if next not in visited:
#                frontier.put(next)
#                visited[next] = True
#                

                
