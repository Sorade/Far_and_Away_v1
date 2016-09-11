# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 19:04:07 2016

@author: Julien
"""
import random

class Event(object):
    def __init__(self,game, name, weight ,text):
        self.game = game
        self.name = name
        self.weight = weight
        self.text = text
        
    def get_weight(self,explorer):
        pass
        
    def update(self,explorer):
        pass
    
class Precious_Ore_Discovered(Event):
    def __init__(self,game):
        self.name = 'Precious Ore Discovered'
        self.weight = 0
        self.planet_pointer = None
        self.text ='''An ore of precious metal has been found in one of your colonies and is being traded throughout the galaxy. It will surely increase our production for a few more years.'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        total_explored_mining_worlds = len([p for p in self.game.all_planets if explorer.check_exploration(p) and p.cat == 'Mining World'])
        self.weight =  total_explored_mining_worlds*20/(self.game.year+1)
#        print 'mining',self.weight
        
    def execute(self,explorer):
        explorer.rp_bonus += 2
        self.planet_pointer[0].disc_rp += 10
        self.planet_pointer = None
        
    def update(self,explorer):
        if self.planet_pointer is None:
            ls = [p for p in self.game.all_planets if explorer.check_exploration(p)]
            self.planet_pointer = [random.choice(ls)]
            self.text ='''An ore of precious metal has been found in {} and is being traded throughout the galaxy. It will surely increase our production for a few more years.'''.format(self.planet_pointer[0].name)


class Raiders(Event):
    def __init__(self,game):
        self.name = 'Raiders'
        self.weight = 0
        self.text ='''Raiders have been reported to disrupt our supply lines and are causing havoc amongst interplanetary trade. This is starting to show in our finances.'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        total_unexplored_planets = len([p for p in self.game.all_planets if not explorer.check_exploration(p) and  explorer.check_discovery(p) and p.cat == 'Frozen World'])
        total_explored_planets = len([p for p in self.game.all_planets if explorer.check_exploration(p) and  explorer.check_discovery(p) and p.cat == 'Frozen World'])        #self.weight = total_unexplored_planets*10/(self.game.year+1) if total_unexplored_planets > 5 else 0
        if total_unexplored_planets > 10 and float(total_explored_planets)/total_unexplored_planets <= 0.999:
            self.weight = 3 if not explorer.states.has_new_weapons else 1
        else:
            self.weight = 0
#        print 'raider',self.weight, float(total_explored_planets)/(total_unexplored_planets+0.01)
        
    def execute(self,explorer):
        explorer.rp_bonus += -2
        
class Storm(Event):
    def __init__(self,game):
        self.name = 'Storm'
        self.weight = 1
        self.text ='''An electromagnetic storm has damaged our servers costing us some precious data which we had spend years gathering !!'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def execute(self,explorer):
        explorer.kp_bonus += -2
        
class Old_Archives(Event):
    def __init__(self,game):
        self.name = 'Old Archives'
        self.weight = 2
        self.text ='''One of your crew librarians has managed to find some long lost archives. They must surely be of interest to us.'''
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        total_explored_habitable_alien = len([p for p in self.game.all_planets if explorer.check_exploration(p) and (p.cat == 'Habitable World' or p.cat == 'Alien World')])
        self.weight = total_explored_habitable_alien*25/(self.game.year+1)
#        print 'archive',self.weight
        
    def execute(self,explorer):
        explorer.kp_bonus += 2
        
class Rebellion(Event):
    def __init__(self,game):
        self.name = 'Rebellion'
        self.weight = 0
        self.planet_pointer = None
        self.text = 'to be defined at exec'
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        total_explored_planets = len([p for p in self.game.all_planets if explorer.check_exploration(p) and p.name != explorer.location])
        self.weight = total_explored_planets*6/(self.game.year+1) if total_explored_planets > 5 else 0
#        print 'rebel',self.weight

    def execute(self,explorer):
        explorer.logbook[self.planet_pointer[0].name].is_explored = False
        self.planet_pointer[0].explored_by.remove(explorer.name)
        self.planet_pointer = None
        
    def update(self,explorer):
        if self.planet_pointer is None:
            list_of_potential_rebelious_planets = [p for p in self.game.all_planets if
                                        explorer.check_exploration(p)
                                        and p.name != explorer.location
                                        and (p.cat == 'Habitable World'
                                        or p.cat == 'Alien World' 
                                        or p.cat == 'Mining World')]
            if len(list_of_potential_rebelious_planets) > 0: self.planet_pointer = [random.choice(list_of_potential_rebelious_planets)]
            self.text ='''The governement of {} has rebelled against your authority. Refusing to pay you the taxes you are owed to carry your duty.'''.format(self.planet_pointer[0].name)

class Alien_Tech(Event):
    def __init__(self,game):
        self.name = 'Alien Tech'
        self.weight = 0
        self.text ='New Alien hyperdrive technology is available, making our travels faster !'
        self.newly_explored = 0
        self.already_explored = 0
        super(Alien_Tech, self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        total_explored_alien = len([p for p in self.game.all_planets if explorer.check_exploration(p) and p.cat == 'Alien World'])
        self.newly_explored = total_explored_alien - self.already_explored
        self.already_explored = total_explored_alien
        self.weight = total_explored_alien*4 if self.newly_explored > 0 else 0
#        print 'AlienTech',self.weight
        
    def execute(self,explorer):
        explorer.travel_bonus += 1
        explorer.states.has_hyperdrive = True
        
class Alien_Weapons(Alien_Tech):
    def __init__(self,game):
        super(type(self), self).__init__(game)
        self.name = 'Xenos Weaponary'
        self.weight = 0
        self.text ='A successful trade deal with an alien colony has allowed to equip our fleet with new, more powerfull weapons. Surely, this will give raiders something to think about !'
        
    def get_weight(self,explorer):
        if not explorer.states.has_new_weapons:
            super(type(self), self).get_weight(explorer)
        else:
            self.weight = 0
        
    def execute(self,explorer):
        explorer.states.has_new_weapons = True
        
        
class Astronomer(Event):
    def __init__(self,game):
        self.name = 'Astronomer'
        self.weight = 0
        self.already_occured = False
        self.text ='An astronomer has joined your high-command concil, enhancing your research efforts for new worlds.'
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        total_explored = len([p for p in self.game.all_planets if explorer.check_exploration(p)])
        self.weight = 2 if self.game.year > 50 and not self.already_occured and total_explored > 25 else 0
#        print 'Astro',self.weight
        
    def execute(self,explorer):
        explorer.search_bonus += 10
        self.already_occured = True

class Contamination(Event):
    def __init__(self,game):
        self.name = 'Contamination'
        self.weight = 0
        self.text ='Following our exploration of a Jungle World, a new deadly virus was discovered amongst crew members of the ship. This will slow us down while we work on a cure !'
        self.newly_explored = 0
        self.already_explored = 0
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        total_explored_jungle = len([p for p in self.game.all_planets if explorer.check_exploration(p) and p.cat == 'Jungle World'])
        self.newly_explored = total_explored_jungle - self.already_explored
        self.already_explored = total_explored_jungle
        if self.newly_explored > 0 and explorer.travel_bonus > 1:
            if self.weight == 0:
                self.weight = total_explored_jungle*3
            elif self.weight > 3:
                self.weight = 3
            else:
                self.weight -= 1
        else:
            self.weight = 0
#        print 'Contamination',self.weight
        
    def execute(self,explorer):
        if explorer.travel_bonus > 1: explorer.travel_bonus -= 1
        explorer.states.contaminated = True
        
class Cure(Event):
    def __init__(self,game):
        self.name = 'Cure'
        self.weight = 0
        self.text ='Commander, a cure has finally been found to cure one of the virus present in the fleet. We can now focus on our task once again !'
        super(type(self), self).__init__(game,self.name,self.weight,self.text)
        
    def get_weight(self,explorer):
        if explorer.states.contaminated:
            self.weight = explorer.kp/100
#        print 'Cure',self.weight
        
    def execute(self,explorer):
        explorer.travel_bonus += 1
        explorer.states.contaminated = False
        
class Radar(Alien_Tech):
    def __init__(self,game):
        super(type(self), self).__init__(game)
        self.name = 'Radar'
        self.weight = 0
        self.text ='Our understanding of Xenos technology has enabled us to develop beam casting radars which make us more likely to discover new planets.'
        
    def get_weight(self,explorer):
        if not explorer.states.has_radar and explorer.states.has_hyperdrive and explorer.states.has_new_weapons:
            super(type(self), self).get_weight(explorer)
            if self.weight > 0: self.weight = 2
#        print 'Radar',self.weight
        
    def execute(self,explorer):
        explorer.travel_bonus += 1
        explorer.states.has_radar = True

