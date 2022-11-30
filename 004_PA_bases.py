import csv
import cPickle as pickle
import random
import math

zones = pickle.load(open('zone_info.pkl',"rb"))
potential_zones = {}
PA_fators = {}
purposes = ['work', 'school', 'leisure', 'business', 'other']
PA_bases = {}
for zone in zones:
    PA_bases[zone] = {}
    for purpose in purposes:
        PA_bases[zone][purpose] ={}
        if purpose == 'work':
            PA_bases[zone][purpose]['ahead'] = zones[zone]['works']
            PA_bases[zone][purpose]['back'] = zones[zone]['pops']
        if purpose == 'school':
            PA_bases[zone][purpose]['ahead'] = zones[zone]['students']
            PA_bases[zone][purpose]['back'] = zones[zone]['pops']
        if purpose == 'leisure':
            PA_bases[zone][purpose]['ahead'] = zones[zone]['l_dens']
            PA_bases[zone][purpose]['back'] = zones[zone]['pops']
        if purpose == 'business':
            PA_bases[zone][purpose]['ahead'] = zones[zone]['b_a_dens']
            PA_bases[zone][purpose]['back'] = zones[zone]['b_p_dens']
        if purpose == 'other':
            PA_bases[zone][purpose]['ahead'] = zones[zone]['o_dens']
            PA_bases[zone][purpose]['back'] = zones[zone]['pops']
pickle.dump(PA_bases, file('PA_bases.pkl','wb'))