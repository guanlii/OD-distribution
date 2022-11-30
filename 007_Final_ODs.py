import csv
import cPickle as pickle
import random
import math
import gc
import sys as sys

def weighted_choice_sub(weights):
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
def WCS_for_lists(wlist):
   choices = []
   weights = []
   for cc in wlist:
        if type(cc) is not list:
            print 'ERROR!'
            break
        choices.append(cc[0])
        weights.append(cc[1])
   choice = choices[weighted_choice_sub(weights)]
   return choice
def Write_OD_to_csv(filename, OD):
    writer = csv.writer(file(filename, 'wb'))
    ids = OD.keys()
    ids.sort()
    firstline = ['O/D']
    for i in ids:
        firstline.append(i)
    writer.writerow(firstline)
    for o in ids:
        item = [o]
        for d in ids:
            item.append(OD[o][d])
        writer.writerow(item)
def distance(i,j):
    xi = all_zones[i]['x']
    yi = all_zones[i]['y']
    xj = all_zones[j]['x']
    yj = all_zones[j]['y']
    dist = pow(pow((xi-xj),2)+pow((yi-yj),2),0.5)
    return dist

def walk_or_cycle(P, o, d):
    if i < 3000:
        zone = i
        b_zone = j
    else:
        zone = j
        b_zone = i
    if distance(b_zone, zone) <= 1200:
        walking_potential = 0.9
        cycling_potential = 0.2
    else:
        walking_potential = 0.8
        cycling_potential = 0.25
    w_r = walking_potential / float((walking_potential + cycling_potential))
    c_r = cycling_potential / float((walking_potential + cycling_potential))
    p_w = P * w_r
    p_c = P * c_r
    return [p_w, p_c]
    
OD = {}
OD_Buses = {}
TAZ_data = {}
zones = pickle.load(open('zone_info.pkl',"rb"))
TAZ_data = pickle.load(open('TAZ_data.pkl',"rb"))
OD_TAZ = pickle.load(open('OD_W&C_TAZ.pkl',"rb"))
all_zones = pickle.load(open('all_zones.pkl',"rb"))
total_zone = all_zones.keys()
OD_all = {}
bus_zones = []
OD_all['walking'] = {}
OD_all['cycling'] = {}
print (len(total_zone))

OD_original = {}
OD_original['walking'] = {}
OD_original['cycling'] = {}

for o in total_zone:
    OD_all['walking'][o] = {}
    OD_all['cycling'][o] = {}
    if o >= 7000:
        bus_zones.append(o)
    for d in total_zone:
        if o < 7000 and d < 7000:
            OD_all['walking'][o][d] = OD_TAZ['walking'][o][d]
            OD_all['cycling'][o][d] = OD_TAZ['cycling'][o][d]
        else:
            OD_all['walking'][o][d] = 0
            OD_all['cycling'][o][d] = 0
print (bus_zones)
bus_zone_rate = {}
for i in TAZ_data:
    bus_zone_rate[i] = {}
    bus_zone_rate[i]['total_R'] = 0

for i in TAZ_data:
    if i < 2000:
        for j in bus_zones:
            D = distance(i,j)
            if D <= 3200:
                if D <= 700:
                    rate = 2
                elif D <= 1000:
                    rate = 1.2
                elif D <= 1400:
                    rate = 0.8
                else:
                    rate = 0.4
                bus_zone_rate[i][j] = rate
                bus_zone_rate[i]['total_R'] += rate
    else:
        for j in bus_zones:
            D = distance(i, j)
            if D <= 1400:
                if D <= 700:
                    rate = 2
                elif D <= 1000:
                    rate = 1.5
                else:
                    rate = 1
                bus_zone_rate[i][j] = rate
                bus_zone_rate[i]['total_R'] += rate

for i in bus_zone_rate:
    if i < 2000:
        P_base = 0.15 * (TAZ_data[i]['P_sum_w'] + TAZ_data[i]['P_sum_c'])
        A_base = 0.15 * (TAZ_data[i]['A_sum_w'] + TAZ_data[i]['A_sum_c'])
    else:
        P_base = 0.05 * (TAZ_data[i]['P_sum_w'] + TAZ_data[i]['P_sum_c'])
        A_base = 0.05 * (TAZ_data[i]['A_sum_w'] + TAZ_data[i]['A_sum_c'])
    bus_keys = bus_zone_rate[i].keys()
    bus_keys.remove('total_R')
    total_R = bus_zone_rate[i]['total_R']
    for j in bus_keys:
        amount_p = P_base * (bus_zone_rate[i][j] / total_R)
        ppp_p = walk_or_cycle(amount_p, i, j)
        amount_a = A_base * (bus_zone_rate[i][j] / total_R)
        ppp_a = walk_or_cycle(amount_a, j, i)
        OD_all['walking'][i][j] += ppp_p[0]
        OD_all['cycling'][i][j] += ppp_p[1]
        OD_all['walking'][j][i] += ppp_a[0]
        OD_all['cycling'][j][i] += ppp_a[1]

Write_OD_to_csv('00_OD_W&C_all_walking.csv', OD_all['walking'])
Write_OD_to_csv('00_OD_W&C_all_cycling.csv', OD_all['cycling'])


OD_original = {}
OD_original['walking'] = {}
OD_original['cycling'] = {}
OD_metro = {}
OD_metro['walking'] = {}
OD_metro['cycling'] = {}
OD_buses = {}
OD_buses['walking'] = {}
OD_buses['cycling'] = {}

for o in total_zone:
    OD_original['walking'][o] = {}
    OD_original['cycling'][o] = {}
    OD_metro['walking'][o] = {}
    OD_metro['cycling'][o] = {}
    OD_buses['walking'][o] = {}
    OD_buses['cycling'][o] = {}
    for d in total_zone:
        if o < 2000 and d < 2000:
            OD_original['walking'][o][d] = OD_all['walking'][o][d]
            OD_original['cycling'][o][d] = OD_all['cycling'][o][d]
            OD_metro['walking'][o][d] = 0
            OD_metro['cycling'][o][d] = 0
            OD_buses['walking'][o][d] = 0
            OD_buses['cycling'][o][d] = 0
        elif (o < 2000 and 2000 <= d < 7000) or (d < 2000 and 2000 <= o < 7000) or (2000 <= o < 7000 and  2000 <= d < 7000):
            OD_original['walking'][o][d] = 0
            OD_original['cycling'][o][d] = 0
            OD_metro['walking'][o][d] = OD_all['walking'][o][d]
            OD_metro['cycling'][o][d] = OD_all['cycling'][o][d]
            OD_buses['walking'][o][d] = 0
            OD_buses['cycling'][o][d] = 0
        else:
            OD_original['walking'][o][d] = 0
            OD_original['cycling'][o][d] = 0
            OD_metro['walking'][o][d] = 0
            OD_metro['cycling'][o][d] = 0
            OD_buses['walking'][o][d] = OD_all['walking'][o][d]
            OD_buses['cycling'][o][d] = OD_all['cycling'][o][d]

Write_OD_to_csv('01_OD_original_walking.csv', OD_original['walking'])
Write_OD_to_csv('01_OD_original_cycling.csv', OD_original['cycling'])
Write_OD_to_csv('02_OD_metro_walking.csv', OD_metro['walking'])
Write_OD_to_csv('02_OD_metro_cycling.csv', OD_metro['cycling'])
Write_OD_to_csv('03_OD_buses_walking.csv', OD_buses['walking'])
Write_OD_to_csv('03_OD_buses_cycling.csv', OD_buses['cycling'])
