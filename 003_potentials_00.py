import csv
import cPickle as pickle
import random
import math
import sys as sys

def distance(i,j):
    xi = zones[i]['x']
    yi = zones[i]['y']
    xj = zones[j]['x']
    yj = zones[j]['y']
    dist = pow(pow((xi-xj),2)+pow((yi-yj),2),0.5)
    return dist

potential_zones = {}
reduction_factors = {}
zones = pickle.load(open('zone_info.pkl',"rb"))
time_od = {}
purposes = ['work','school','leisure','business','other']
potential_zones['walking_potential'] = {}
potential_zones['cycling_potential'] = {}
potential_zones['reduction_factor'] = {}

time_od_walk = pickle.load(open('time_od_walk.pkl',"rb"))
time_od_cycle = pickle.load(open('time_od_cycle.pkl',"rb"))
connector_addit = 5
for i in zones:
    potential_zones['walking_potential'][i] = {}
    potential_zones['cycling_potential'][i] = {}
    potential_zones['reduction_factor'][i] = {}
    o = zones[i]['zone_id']
    for j in zones:
        d = zones[j]['zone_id']
        if i == j:
            walking_potential = 0.99
            cycling_potential = 0.01
        elif time_od_walk[o][d] <= 5 + connector_addit:
            walking_potential = 0.9
            cycling_potential = 0.1
        elif time_od_walk[o][d] <= 10 + connector_addit:
            walking_potential = 0.9
            cycling_potential = 0.1
        elif time_od_walk[o][d] <= 15 + connector_addit:
            walking_potential = 0.9
            cycling_potential = 0.1
        elif time_od_walk[o][d] <= 20 + connector_addit:
            walking_potential = 0.7
            cycling_potential = 0.2
        elif time_od_walk[o][d] <= 30 + connector_addit:
            walking_potential = 0.7
            cycling_potential = 0.3
        elif time_od_walk[o][d] <= 40 + connector_addit:
            walking_potential = 0.5
            cycling_potential = 0.7
        elif time_od_walk[o][d] <= 60 + connector_addit:
            walking_potential = 0.2
            cycling_potential = 0.7
        else:
            walking_potential = None
            cycling_potential = None
        if not walking_potential == None:
            potential_zones['walking_potential'][i][j] = walking_potential
            potential_zones['cycling_potential'][i][j] = cycling_potential

pickle.dump(potential_zones, file('potential_zones.pkl','wb'))