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

for i in zones:
    potential_zones['walking_potential'][i] = {}
    potential_zones['cycling_potential'][i] = {}
    potential_zones['reduction_factor'][i] = {}
    reduction_factors[i] = {}
    for j in zones:
        if i == j:
            walking_potential = 0.99
            cycling_potential = 0.01
        elif distance(i,j) <= 300:
            walking_potential = 0.9
            cycling_potential = 0.1
        elif distance(i,j) <= 500:
            walking_potential = 0.8
            cycling_potential = 0.2
        elif distance(i,j) <= 800:
            walking_potential = 0.8
            cycling_potential = 0.2
        elif distance(i,j) <= 1000:
            walking_potential = 0.7
            cycling_potential = 0.4
        elif distance(i,j) <= 1500:
            walking_potential = 0.6
            cycling_potential = 0.5
        elif distance(i,j) <= 2000:
            walking_potential = 0.5
            cycling_potential = 0.7
        elif distance(i, j) <= 5000:
            walking_potential = 0.2
            cycling_potential = 0.9
        else:
            walking_potential = None
            cycling_potential = None
        if not walking_potential == None:
            potential_zones['walking_potential'][i][j] = walking_potential
            potential_zones['cycling_potential'][i][j] = cycling_potential
            if distance(i,j) <= 500:
                reduction_factor = 1
            elif distance(i, j) <= 1000:
                reduction_factor = 0.9
            elif distance(i, j) <= 2000:
                reduction_factor = 0.5
            elif distance(i, j) <= 2000:
                reduction_factor = 0.3
            elif distance(i, j) <= 3000:
                reduction_factor = 0.07
            elif distance(i, j) <= 5000:
                reduction_factor = 0.01
            potential_zones['reduction_factor'][i][j] = reduction_factor
print( sys.getsizeof(potential_zones))
pickle.dump(potential_zones, file('potential_zones.pkl','wb'))
pickle.dump(reduction_factors, file('reduction_factors.pkl','wb'))
