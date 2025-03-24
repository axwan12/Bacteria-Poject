from tkinter import * 
from tkinter.ttk import *
from time import sleep
from random import *
from math import *
import numpy as npa
import matplotlib.pyplot as plt

#Creates Object "bacteria" for Storing all Bacteria Related Information
class bacteria:
    #dictionary holding instance properties
    dic = {}
    death_rate = 1
    all_spawn_rate = 0.85
    plasmid_rate = 0.1
    plasmid_death_rate = 0.01
    weights = []
    #initialised code
    def __init__(self,name,spawn_rate,reproduction_rate,grid_ref,colour,plasmid):
        self.count = 0
        self.history = []
        self.name = name
        self.spawn_rate = spawn_rate
        self.reproduction_rate = reproduction_rate
        self.grid_ref = grid_ref
        self.colour = colour
        self.plasmid = plasmid

        #linking the dictionary to values
        bacteria.dic[grid_ref] = self
        bacteria.dic[name] = self
        bacteria.dic[(name, grid_ref)] = self

        #records the spawning weights associated with each bacteria in an array
        bacteria.weights.append(self.spawn_rate)

    #adds to the count of that instance when called
    def ammend_count(self):
        self.count += 1

    #removes from the count of that instance when called
    def delete(self):
        self.count -= 1
    
    #resets the count for that instance when called
    def reset(self):
        self.count = 0
    
    #appends the count to a hostorical record of the count over time
    def bacteria_history(self):
        self.history.append(self.count)

    #call to reset the counts of all instances
    @classmethod
    def reset_all_counts(cls):
        for bacteria_instance in cls.dic.values():
            bacteria_instance.reset()

    #call to create default classes
    @classmethod
    def create_defaults(cls):
        #parameters for the spawn rates from the paper (Xu et al., 2017)
        r, mf, mp, mc, mcp, cC, cP, x, s, A = 1, 0.75, 0.3, 0.3, 0.5, 0.01, 0.01, 0.01, 0.01, 0.3
        rf, rc, rp, rcp = r - mf*A, r - cC - mc*A, r - cP - x - mp*A, r - cC - cP - x - mcp*A

        n0 = cls('empty',0,0,0,'white',0)
        nf = cls('nf',0,rf,1,'red',False)
        np = cls('np',0.05,rp,2,'blue',True)
        nc = cls('nc',0.67,rc,3,'black',False)
        ncp = cls('ncp',0.23,rcp,4,'green',True)

#class grid, prepares the grid & canvas for modifying
class grid:
    def __init__(self,x,y,square_size, bacteria,name,random_colonies,colony_ref):
        self.run = True
        self.name = name
        self.window = Tk()
        self.window.title(name)
        self.canvas = Canvas(self.window, width=x*square_size, height=y*square_size, bg='white')
        self.canvas.pack(anchor=CENTER, expand=True)
        self.bacteria = bacteria
        self.square_size = square_size

        #varariables to enable random colonies
        self.random_colonies = random_colonies
        self.colony_ref = colony_ref

        #handles the windows closing
        self.window.protocol("WM_DELETE_WINDOW", self.handler)

        #creates the heatmap, which holds the positions of all bsacteria
        self.heatmap = []

        #generates the heatmap when the bacteria spawn randomly
        if random_colonies == False:
            for r in range(y):
                thisrow = []
                for c in range(x):
                    #decides wether to spawn a bacteria
                    if random() < bacteria.all_spawn_rate: 
                        #chooses the bacteria based on a weighting
                        thisrow.append(weighted_output([0,1,2,3,4],bacteria.weights))
                    else:
                        thisrow.append(0)
                self.heatmap.append(thisrow)

        #generates the heatmap when the chosen bacteria spawns in a colony in the middle
        elif random_colonies == True:
            #adjusts the weightings, removing the colony bacteria
            ref = [0,1,2,3,4]
            weight = []
            ref.pop(bacteria.dic[colony_ref].grid_ref)
            for i in range(len(ref)):
                    weight.append(bacteria.dic[ref[i]].spawn_rate)
            #generates heatmap without the colony bacteria
            for r in range(y):
                thisrow = []
                for c in range(x):
                    if random() < bacteria.all_spawn_rate: 
                        thisrow.append(weighted_output(ref,weight))
                    else:
                        thisrow.append(0)
                self.heatmap.append(thisrow)

            #inserts a block of colony bacteria in the centre of the grid
            colony_length = round(sqrt(bacteria.dic[colony_ref].spawn_rate*x*y/bacteria.all_spawn_rate))
            top_left = (round(x/2-colony_length/2),round(y/2-colony_length/2))
            for r in range(colony_length):
                 for c in range(colony_length):
                    if random() < bacteria.all_spawn_rate:
                        self.heatmap[top_left[0]+r][top_left[1]+c] = bacteria.dic[colony_ref].grid_ref
                    else:
                        self.heatmap[top_left[0]+r][top_left[1]+c] = 0
    
    #handler for window closing
    def handler(self):
        self.run = False
        self.window.destroy()

#generates array for the relative positions for cells in a radius r around (0,0)
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

#shuffles the order running of the heatmap, to ensure earlier cells dont get priority
def heatmap_order_shuffle(heatmap):
    order = [(r,c) for r in range(len(heatmap))
                     for c in range(len(heatmap[0])) if heatmap[r][c] != 0]
    shuffle(order)
    return order

#function for bacteria behaviour
def Behaviour(heatmap,extrinsic_death_rate,death_radius,death_zone,interaction_zone):
    order = heatmap_order_shuffle(heatmap)
    #hardcoded direction for spawning
    direction = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for o in range(len(order)):
        p = order[o]

        #picks a random relative position to move to
        move_direction = choice(direction)
        h = move_direction[0]
        v = move_direction[1]
        
        #variable to hold free positions for spawning
        Free = []

        #manages bacteria with plasmids
        if bacteria.dic[heatmap[p[0]][p[1]]].plasmid == True:
            for i in range(len(interaction_zone)):
                #holds the position of the interacting cell 
                position = heatmap[(p[0]+interaction_zone[i][0])%len(heatmap)][(p[1]+interaction_zone[i][1])%len(heatmap[0])]

                if position != 0 and bacteria.dic[position].plasmid == False and random() < bacteria.plasmid_rate/len(interaction_zone):
                    heatmap[(p[0]+interaction_zone[i][0])%len(heatmap)][(p[1]+interaction_zone[i][1])%len(heatmap[0])] += 1

            if random() < bacteria.plasmid_death_rate:
                heatmap[p[0]][p[1]] -= 1

        for i in range(len(direction)):
                position = heatmap[(p[0]+direction[i][0])%len(heatmap)][(p[1]+direction[i][1])%len(heatmap[0])]
                if position == 0:
                    Free.append(((p[0]+direction[i][0])%len(heatmap),(p[1]+direction[i][1])%len(heatmap[0]))) 

        if random() < bacteria.dic[heatmap[p[0]][p[1]]].reproduction_rate and len(Free) > 0:
            spawn_direction = choices(Free,k=1)[0]
            heatmap[(spawn_direction[0])%len(heatmap)][(spawn_direction[1])%len(heatmap[0])] = heatmap[p[0]][p[1]]

        #holds the count of bacteria in the death radius
        n_count = 0
        for i in range(len(death_zone)):
            if heatmap[(p[0]+death_zone[i][0])%len(heatmap)][(p[1]+death_zone[i][1])%len(heatmap[0])] > 0:
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

def colour(heatmap, canvas, r, c,grid):
    canvas.create_rectangle((grid.square_size*c,grid.square_size*r), (grid.square_size*(c+1), grid.square_size*(r+1)),
                            fill=bacteria.dic[heatmap[r][c]].colour)
def weighted_output(numbers,weights):
    random_number = choices(numbers, weights=weights, k=1)[0]
    return random_number

'''
Refrences

Xu, S., Yang, J., Yin, C., & Zhao, X. (2017). The dominance of bacterial genotypes leads to
susceptibility variations under sublethal antibiotic pressure. Future Microbiology, 13. https:
//doi.org/10.2217/fmb-2017-0070
'''