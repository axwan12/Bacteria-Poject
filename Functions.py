from tkinter import * 
from tkinter.ttk import *
from time import sleep
from random import *
from math import *
import numpy as npa
import matplotlib.pyplot as plt

#Creates Object "bacteria" for Storing all Bacteria Related Information
class bacteria:
    dictionary = {}

    def __init__(self,spawn_rate,reproduction_rate,grid_ref,colour):
        self.count = 0
        self.spawn_rate = spawn_rate
        self.reproduction_rate = reproduction_rate
        self.grid_ref = grid_ref
        self.colour = colour
        bacteria.dictionary[grid_ref] = self

    def ammend_count(self):
        self.count += 1
    def delete(self):
        self.count -=1
    def reset(self):
        self.count = 0

    @classmethod
    def reset_all_counts(cls):
        for bacteria_instance in cls.dictionary.values():
            bacteria_instance.reset()

    @classmethod
    def create_defaults(cls):
        cls(0,0,0,'white')

class grid:
    def __init__(self,size):
        self.heatmap = []
        for r in range(size[1]):
            thisrow = []
            for c in range(size[0]):
                if random() < 0.5:
                    thisrow.append(1)
                else:
                    thisrow.append(0)
            self.heatmap.append(thisrow)

def death_radius(r):   
    if r > 0:
        radius = []
        for i in range(-r,r+1):
            for j in range(-r,r+1):
                if j !=0 or i!=0:
                     radius.append((i,j))
        return radius
    
    else:
        print("Error: Radius Must be Positive and Greater Than Zero, a Radius of One Will be Used :)")
        return [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def heatmap_order_shuffle(heatmap):
    order = [(r,c) for r in range(len(heatmap))
                     for c in range(len(heatmap[0])) if heatmap[r][c] != 0]
    shuffle(order)
    return order

def move_random(heatmap,extrinsic_death_rate,order):
    n = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for o in range(len(order)):
        direction = 2*pi*random()
        h = round(cos(direction)) 
        v = round(sin(direction))
        p = order[o]
        
        for i in range(len(n)):
            if heatmap[(p[0]+n[i][0])%len(heatmap)][(p[1]+n[i][1])%len(heatmap[0])] != 0:
                die = True
            else:
                die = False
                break
        if die == False and heatmap[(p[0]+h)%len(heatmap)][(p[1]+v)%len(heatmap[0])] == 0:
            heatmap[(p[0]+h)%len(heatmap)][(p[1]+v)%len(heatmap[0])] = heatmap[p[0]][p[1]]
            heatmap[p[0]][p[1]] = 0
        
        elif die == True and random() < extrinsic_death_rate:
            heatmap[p[0]][p[1]] = 0
        else:
            heatmap[p[0]][p[1]] = heatmap[p[0]][p[1]]
                
    return heatmap

