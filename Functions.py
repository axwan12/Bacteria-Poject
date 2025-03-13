from tkinter import * 
from tkinter.ttk import *
from time import sleep
from random import *
from math import *
import numpy as npa
import matplotlib.pyplot as plt

N = 0
z = 0
weights = []

#Creates Object "bacteria" for Storing all Bacteria Related Information
class bacteria:
    dic = {}
    death_rate = 0.1
    all_spawn_rate = 0.1
    plasmid_rate = 0.02
    plasmid_death_rate = 0.01
    def __init__(self,name,spawn_rate,reproduction_rate,grid_ref,colour,plasmid):
        self.count = 0
        self.history = []
        self.name = name
        self.spawn_rate = spawn_rate
        self.reproduction_rate = reproduction_rate
        self.grid_ref = grid_ref
        self.colour = colour
        self.plasmid = plasmid
        bacteria.dic[grid_ref] = self
        bacteria.dic[name] = self
        bacteria.dic[(name, grid_ref)] = self
        global weights
        weights.append(self.spawn_rate)

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
        global z
        z += self.spawn_rate
    
    def bacteria_history(self):
        self.history.append(self.count)

    @classmethod
    def reset_all_counts(cls):
        for bacteria_instance in cls.dic.values():
            bacteria_instance.reset()

    @classmethod
    def create_defaults(cls):
        f = 0.2
        r, mf, mp, mc, mcp, cC, cP, x, s, A = 1, 0.75, 0.3, 0.3, 0.5, 0.01, 0.01, 0.01, 0.01, 0
        rf, rc, rp, rcp = f*(r - mf*A), f*(r - cC - mc*A), f*(r - cP - x - mp*A), f*(r - cC - cP - x - mcp*A)

        cls('empty',0,0,0,'white',0)
        cls('nf',0.67,rf,1,'red',False)
        cls('np',0.1,rp,2,'blue',True)
        cls('nc',0.23,rc,3,'black',False)
        cls('ncp',0.1,rcp,4,'green',True)

class grid:
    def __init__(self,x,y,square_size, bacteria,name):
        self.run = True
        self.name = name
        self.window = Tk()
        self.window.title(name)
        self.canvas = Canvas(self.window, width=x*square_size, height=y*square_size, bg='white')
        self.canvas.pack(anchor=CENTER, expand=True)
        self.bacteria = bacteria

        self.window.protocol("WM_DELETE_WINDOW", self.handler)

        self.heatmap = []

        global weights
        for r in range(y):
            thisrow = []
            for c in range(x):
                if random() < bacteria.all_spawn_rate: 
                    thisrow.append(weighted_output([0,1,2,3,4],
                                                weights))
                else:
                    thisrow.append(0)
            self.heatmap.append(thisrow)

    def handler(self):
        self.run = False
        self.window.destroy()

def AOE(r):   
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

def Behaviour(heatmap,extrinsic_death_rate,death_radius,interaction_area):
    order = heatmap_order_shuffle(heatmap)
    n = AOE(death_radius)
    m = AOE(interaction_area)
    for o in range(len(order)):
        direction = 2*pi*random()
        h = round(cos(direction)) 
        v = round(sin(direction))
        p = order[o]

        spawn_direction = 2*pi*random()
        sh = round(cos(direction)) 
        sv = round(sin(direction))

        n_count = 0
        if bacteria.dic[heatmap[p[0]][p[1]]].plasmid == True:
            for i in range(len(m)):
                position = heatmap[(p[0]+m[i][0])%len(heatmap)][(p[1]+m[i][1])%len(heatmap[0])]
                if position != 0 and bacteria.dic[position].plasmid == False and random() < bacteria.plasmid_rate:
                    heatmap[(p[0]+m[i][0])%len(heatmap)][(p[1]+m[i][1])%len(heatmap[0])] += 1
            if random() < bacteria.plasmid_death_rate:
                heatmap[p[0]][p[1]] -= 1
        
        if random() < bacteria.dic[heatmap[p[0]][p[1]]].reproduction_rate and heatmap[(p[0]+sh)%len(heatmap)][(p[1]+sv)%len(heatmap[0])] == 0:
            heatmap[(p[0]+sh)%len(heatmap)][(p[1]+sv)%len(heatmap[0])] = bacteria.dic[heatmap[p[0]][p[1]]].grid_ref
            
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
def weighted_output(numbers,weights):
    random_number = choices(numbers, weights=weights, k=1)[0]
    return random_number