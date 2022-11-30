#coding:utf-8
import csv
import cPickle as pickle
import random
import math

def OD_init(id_list):
    od = {}
    for o in id_list:
        od[o] = {}
        for d in id_list:
            od[o][d] = 0
    return od
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
def OD_reader(reader_od):
    od = {}
    for line in reader_od:
        o = int(line[1])
        d = int(line[3])
        value = float(line[5])
        if not o in od.keys():
            od[o] = {}
            od[o][d] = value
        else:
            od[o][d] = value
    return od
def landuse_filter(landuse, function):
    if landuse == 'Commer':
        if function.find('C2') >= 0:
            landuse = 'office'
        elif function == 'C4':
            landuse = 'hotel'
        else:
            landuse = 'commer_les'
    if landuse == 'Admini':
        if function.find('GIC5') >= 0:
            landuse = 'school'
        elif function.find('GIC51') >= 0:
            landuse = 'compus'
        elif function.find('GIC4') >= 0:
            landuse = 'hospital'
        elif function.find('GIC2') >= 0 or function.find('GIC3') >= 0:
            landuse = 'cul_spt_les'
        else:
            landuse = 'office_gov'
    if landuse == 'Green':
        if not landuse == 'G2':
            landuse = 'green_les'
    if landuse == 'Manuf':
        if function.find('M0') >= 0:
            landuse = 'office'
    return landuse

TAZ_zones = pickle.load(open('TAZ_zones.pkl',"rb"))
time_od_cycle = {}
reader_time_od_cycle = csv.reader(open('time_od_cycle1.csv'))
time_od_walk = {}
reader_time_od_walk = csv.reader(open('time_od_walk1.csv'))

for o in TAZ_zones:
    time_od_cycle[o] = {}
    time_od_walk[o] = {}
    for d in TAZ_zones:
        time_od_cycle[o][d] = 0
        time_od_walk[o][d] = 0

for line in reader_time_od_cycle:
    o = int(line[0])
    d = int(line[1])
    if not line[2] == '':
        time = float(line[2])
    if not o == d:
        time_od_cycle[o][d] = time / 249
    else:
        time_od_cycle[o][d] = 0.2
for line in reader_time_od_walk:
    o = int(line[0])
    d = int(line[1])
    if not line[2] == '':
        time = float(line[2])
    if not o == d:
        time_od_walk[o][d] = time / 83
    else:
        time_od_walk[o][d] = 2

pickle.dump(time_od_cycle, file('time_od_cycle.pkl','wb'))
pickle.dump(time_od_walk, file('time_od_walk.pkl','wb'))
