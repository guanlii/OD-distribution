#coding:utf-8
import csv
import cPickle as pickle
import random
import math

zone_info = {}
reader_zone_info = csv.reader(open('TAZ_all.csv'))

for line in reader_zone_info:
    id = int(line[0])
    x = float(line[1])
    y = float(line[2])
    zone_info[id] = {}
    zone_info[id]['x'] = x
    zone_info[id]['y'] = y

print (len(zone_info))

pickle.dump(zone_info, file('all_zones.pkl','wb'))


    
    
