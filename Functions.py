from tkinter import * 
from tkinter.ttk import *
from time import sleep
from random import *
from math import *
import numpy as npa
import matplotlib.pyplot as plt

N = 0
r = 0

#Creates Object "bacteria" for Storing all Bacteria Related Information
class bacteria:
    dic = {}
    death_rate = 0.1
    
    def __init__(self,name,spawn_rate,reproduction_rate,grid_ref,colour):
        self.count = 0
        self.history = []
        self.name = name
        self.spawn_rate = spawn_rate
        self.reproduction_rate = reproduction_rate
        self.grid_ref = grid_ref
        self.colour = colour
        bacteria.dic[grid_ref] = self
        bacteria.dic[name] = self
        bacteria.dic[(name, grid_ref)] = self

    def ammend_count(self):
        global N
        self.count += 1
        N += 1

    def delete(self):
        global N
        self.count -= 1
        N -= 1

    def reset(self):
        self.count = 0

    def accumalate(self):
        global r
        r += self.spawn_rate
    
    def bacteria_history(self):
        self.history.append(self.count)

    def spawn(self):
        print('test')

    @classmethod
    def reset_all_counts(cls):
        for bacteria_instance in cls.dic.values():
            bacteria_instance.reset()

    @classmethod
    def accumalate_all_spawn(cls):
        for bacteria_instance in cls.dic.values():
            bacteria_instance.accumalate()
        print(r)


    @classmethod
    def create_defaults(cls):
        cls('empty',0,0,0,'white')
        cls('nf',0.05,0,1,'red')
        cls('np',0.01,0,2,'blue')
        cls('nc',0.01,0,3,'black')
        cls('ncp',0.01,0,4,'green')

class grid:
    def __init__(self,x,y,square_size, bacteria,name):
        self.run = True
        self.name = name
        self.window = Tk()
        self.window.attributes('-fullscreen', False)
        self.window.title(name)
        self.canvas = Canvas(self.window, width=x*square_size, height=y*square_size, bg='white')
        self.canvas.pack(anchor=CENTER, expand=True)
        self.bacteria = bacteria

        self.window.protocol("WM_DELETE_WINDOW", self.handler)

        self.heatmap = []
        for r in range(y):
            thisrow = []
            for c in range(x):
                if random() < self.bacteria.dic['nf'].spawn_rate:
                    thisrow.append(1)
                else:
                    thisrow.append(0)
            self.heatmap.append(thisrow)

    def handler(self):
        self.run = False
        self.window.destroy()

def death_radius_area(r):   
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

def move_random(heatmap,extrinsic_death_rate,death_radius):
    order = heatmap_order_shuffle(heatmap)
    n = death_radius_area(death_radius)
    for o in range(len(order)):
        direction = 2*pi*random()
        h = round(cos(direction)) 
        v = round(sin(direction))
        p = order[o]

        n_count = 0
        
        for i in range(len(n)):
            if heatmap[(p[0]+n[i][0])%len(heatmap)][(p[1]+n[i][1])%len(heatmap[0])] > 0:
                n_count +=1
        N = n_count/((death_radius*2+1)**2-1)

        if random() < N*bacteria.death_rate:
            heatmap[p[0]][p[1]] = 0
        
        elif heatmap[(p[0]+h)%len(heatmap)][(p[1]+v)%len(heatmap[0])] == 0:
            heatmap[(p[0]+h)%len(heatmap)][(p[1]+v)%len(heatmap[0])] = heatmap[p[0]][p[1]]
            heatmap[p[0]][p[1]] = 0
        
        else:
            heatmap[p[0]][p[1]] = heatmap[p[0]][p[1]]
                
    return heatmap

def colour(heatmap, canvas, r, c):
    canvas.create_rectangle((10*c,10*r), (10*(c+1), 10*(r+1)),
                            fill=bacteria.dic[heatmap[r][c]].colour)
