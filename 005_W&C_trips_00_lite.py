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
    xi = zones[i]['x']
    yi = zones[i]['y']
    xj = zones[j]['x']
    yj = zones[j]['y']
    dist = pow(pow((xi-xj),2)+pow((yi-yj),2),0.5)
    return dist

def walk_or_cycle(P, o, d):
    i = zones[o]['zone_id']
    j = zones[d]['zone_id']
    if time_od_walk[i][j] <= 30:
        if time_od_walk[i][j] <= 5:
            walking_potential = potential_zones['walking_potential'][o][d] * 3
        elif time_od_walk[i][j] <= 10:
            walking_potential = potential_zones['walking_potential'][o][d] * 1.5
        elif time_od_walk[i][j] <= 15:
            walking_potential = potential_zones['walking_potential'][o][d] * 1
        elif time_od_walk[i][j] <= 20:
            walking_potential = potential_zones['walking_potential'][o][d] * 1
        elif time_od_walk[i][j] <= 25:
            walking_potential = potential_zones['walking_potential'][o][d] * 0.9
        else:
            walking_potential = potential_zones['walking_potential'][o][d] * 0.8
    else:
        walking_potential = potential_zones['walking_potential'][o][d] * 0.5
    cycling_potential = potential_zones['cycling_potential'][o][d]
    w_r = walking_potential / float((walking_potential + cycling_potential))
    c_r = cycling_potential / float((walking_potential + cycling_potential))
    p_w = P * w_r
    p_c = P * c_r * 0.5
    return [p_w, p_c]
def walk_or_cycle_transit(P, o, d):
    i = zones[o]['zone_id']
    j = zones[d]['zone_id']
    if time_od_walk[i][j] <= 23:
        if time_od_walk[i][j] <= 5:
            walking_potential = potential_zones['walking_potential'][o][d] * 2
        elif time_od_walk[i][j] <= 10:
            walking_potential = potential_zones['walking_potential'][o][d] * 1
        elif time_od_walk[i][j] <= 15:
            walking_potential = potential_zones['walking_potential'][o][d] * 0.8
        else:
            walking_potential = potential_zones['walking_potential'][o][d] * 0.5
    else:
        walking_potential = 0
    cycling_potential = potential_zones['cycling_potential'][o][d]
    w_r = walking_potential / float((walking_potential + cycling_potential))
    c_r = cycling_potential / float((walking_potential + cycling_potential))
    p_w = P * w_r * 1.08
    p_c = P * c_r * 0.4
    return [p_w, p_c]

def reduction_factor(o,d):
    i = zones[o]['zone_id']
    j = zones[d]['zone_id']
    if time_od_cycle[i][j] <= 5:
        rf = 1
    elif time_od_cycle[i][j] <= 10:
        rf = 0.5
    elif time_od_cycle[i][j] <= 20:
        rf = 0.2
    elif time_od_cycle[i][j] <= 30:
        rf = 0.001
    elif time_od_cycle[i][j] <= 40:
        rf = 0.0005
    elif time_od_cycle[i][j] <= 60:
        rf = 0.00001
    else:
        rf = 0
    return rf
def reduction_factor_transit(o,d):
    i = zones[o]['zone_id']
    j = zones[d]['zone_id']
    if time_od_cycle[i][j] <= 5:
        rf = 1
    elif time_od_cycle[i][j] <= 10:
        rf = 0.3
    elif time_od_cycle[i][j] <= 15:
        rf = 0.01
    elif time_od_cycle[i][j] <= 20:
        rf = 0.001
    else:
        rf = 0
    return rf

def tripping_destination(pp, zone, purpose, direction):
    ratio = 0.4
    weight_zones = {}
    total_weights = 0
    for z in zones:
        W_base = PA_bases[z][purpose][direction]
        if z in potential_zones['walking_potential'][zone]:
            weight = W_base*reduction_factor(zone, z)
        else:
            weight = W_base * 0.003
        weight_zones[z] = weight
        total_weights += weight
    for i in weight_zones:
        amount = pp * (weight_zones[i] / total_weights)
        if i in potential_zones['walking_potential'][zone]:
            ppp = walk_or_cycle(amount, zone, i)
            OD_TAZ['walking'][zones[zone]['zone_id']][zones[i]['zone_id']] += ppp[0] * ratio
            OD_TAZ['cycling'][zones[zone]['zone_id']][zones[i]['zone_id']] += ppp[1] * ratio
            TAZ_data[zones[zone]['zone_id']]['P_sum_w'] += ppp[0] * ratio
            TAZ_data[zones[zone]['zone_id']]['P_sum_c'] += ppp[1] * ratio
            TAZ_data[zones[i]['zone_id']]['A_sum_w'] += ppp[0] * ratio
            TAZ_data[zones[i]['zone_id']]['A_sum_c'] += ppp[1] * ratio
        else:
            OD_TAZ['cycling'][zones[zone]['zone_id']][zones[i]['zone_id']] += amount * ratio
            TAZ_data[zones[zone]['zone_id']]['P_sum_c'] += amount * ratio
            TAZ_data[zones[i]['zone_id']]['A_sum_c'] += amount * ratio
    return None

def activity_work(zone,off_work_p_wc):
    offwork_home_ratio = 0.6 ###todo peak hour ratio
    wc_offwork_home = int(off_work_p_wc*offwork_home_ratio)
    tripping_destination(wc_offwork_home, zone, 'work', 'back')


def activity_school(zone, off_school_p_wc):
    offschool_home_ratio = 0.8 ###todo
    wc_offschool_home = int(off_school_p_wc*offschool_home_ratio)
    tripping_destination(wc_offschool_home, zone, 'school', 'back')


def activity_leisure(zone, off_work_p_wc, off_school_p_wc, from_home_p_wc):
    offwork_leisure_ratio = 0.3
    offschool_leisure_ratio = 0.3
    fromhome_leisure_ratio = 0.5 ###todo
    wc_offwork_leisure = int(off_work_p_wc*offwork_leisure_ratio)   
    wc_offschool_leisure = int(off_school_p_wc*offschool_leisure_ratio)
    wc_fromhome_leisure = int(from_home_p_wc*fromhome_leisure_ratio)
    tripping_destination(wc_offwork_leisure, zone, 'leisure', 'ahead')
    tripping_destination(wc_offschool_leisure, zone, 'leisure', 'ahead')
    tripping_destination(wc_fromhome_leisure, zone, 'leisure', 'ahead')

def activity_business(zone, business_p_wc):
    offbusiness_ratio = 1
    wc_offbusiness = int(business_p_wc*offbusiness_ratio)
    tripping_destination(wc_offbusiness, zone, 'business', 'back')

def activity_other(zone, off_work_p_wc, off_school_p_wc, from_home_p_wc, off_other_p_wc):
    offwork_other_ratio = 0.1
    offschool_other_ratio = 0.01
    fromhome_other_ratio = 0.1
    ###
    offother_home_ratio = 1
    offother_leisure_ratio = 1
    offother_other_ratio = 1
    ###
    wc_offwork_other = int(off_work_p_wc*offwork_other_ratio)   
    wc_offschool_other = int(off_school_p_wc*offschool_other_ratio)
    wc_fromhome_other = int(from_home_p_wc*fromhome_other_ratio)
    tripping_destination(wc_offwork_other, zone, 'other', 'ahead')
    tripping_destination(wc_offschool_other, zone, 'other', 'ahead')
    tripping_destination(wc_fromhome_other, zone, 'other', 'ahead')
    wc_offother_home = int(off_other_p_wc*offother_home_ratio)
    wc_offother_leisure = int(off_other_p_wc*offother_leisure_ratio)
    wc_offother_other = int(off_other_p_wc*offother_other_ratio)     
    tripping_destination(wc_offother_home, zone, 'other', 'back')
    tripping_destination(wc_offother_leisure, zone, 'leisure', 'ahead')
    tripping_destination(wc_offother_other, zone, 'other', 'ahead')

def activity_fromtransit(zone, transit_p_wc, transit_a_wc):
    ratio_transit = 1
    weight_zones_p = {}
    total_weights_p = 0
    weight_zones_a = {}
    total_weights_a = 0
    for z in potential_zones['walking_potential'][zone]:
        pops = zones[z]['pops']
        works = zones[z]['works']
        students = zones[z]['students']
        l_dens = zones[z]['l_dens']
        b_dens = zones[z]['b_a_dens']
        W_base_p = 1*pops + 0.001*l_dens + 0.00025 * b_dens
        W_base_a = 1.5*works + 0.5*students + 0.002*l_dens + 0.0003 * b_dens
        weight_p = W_base_p * reduction_factor_transit(zone, z)
        weight_a = W_base_a * reduction_factor_transit(z, zone)
        weight_zones_p[z] = weight_p
        total_weights_p += weight_p
        weight_zones_a[z] = weight_a
        total_weights_a += weight_a
    for i in weight_zones_p:
        amount_p = transit_p_wc * (weight_zones_p[i] / total_weights_p)
        ppp_p = walk_or_cycle_transit(amount_p, zone, i)
        amount_a = transit_a_wc * (weight_zones_a[i] / total_weights_a)
        ppp_a = walk_or_cycle_transit(amount_a, i, zone)
        OD_TAZ['walking'][zones[zone]['zone_id']][zones[i]['zone_id']] += ppp_p[0] * ratio_transit
        OD_TAZ['cycling'][zones[zone]['zone_id']][zones[i]['zone_id']] += ppp_p[1] * ratio_transit
        OD_TAZ['walking'][zones[i]['zone_id']][zones[zone]['zone_id']] += ppp_a[0] * ratio_transit
        OD_TAZ['cycling'][zones[i]['zone_id']][zones[zone]['zone_id']] += ppp_a[1] * ratio_transit
        TAZ_data[zones[zone]['zone_id']]['P_sum_w'] += ppp_p[0] * ratio_transit
        TAZ_data[zones[zone]['zone_id']]['P_sum_c'] += ppp_p[1] * ratio_transit
        TAZ_data[zones[i]['zone_id']]['P_sum_w'] += ppp_a[0] * ratio_transit
        TAZ_data[zones[i]['zone_id']]['P_sum_c'] += ppp_a[1] * ratio_transit
        TAZ_data[zones[i]['zone_id']]['A_sum_w'] += ppp_p[0] * ratio_transit
        TAZ_data[zones[i]['zone_id']]['A_sum_c'] += ppp_p[1] * ratio_transit
        TAZ_data[zones[zone]['zone_id']]['A_sum_w'] += ppp_a[0] * ratio_transit
        TAZ_data[zones[zone]['zone_id']]['A_sum_c'] += ppp_a[1] * ratio_transit

    return None

def activity_random(zone):
    return None
    
OD = {}
OD_TAZ = {}
TAZ_data = {}
zones = pickle.load(open('zone_info.pkl',"rb"))
print 'zones',sys.getsizeof(zones)
TAZ_zones = pickle.load(open('TAZ_zones.pkl',"rb"))
print 'TAZ_zones',sys.getsizeof(TAZ_zones)
mainzones = {}
purposes = ['work','school','leisure','business','other']
PA_bases = pickle.load(open('PA_bases.pkl',"rb"))
print 'PA_bases',sys.getsizeof(PA_bases)
potential_zones = pickle.load(open('potential_zones.pkl',"rb"))
print 'potential_zones',sys.getsizeof(potential_zones)
###reduction_factors = pickle.load(open('reduction_factors.pkl',"rb"))
###print 'reduction_factors',sys.getsizeof(reduction_factors)
PA_types = ['home','work','school','shopping','parks&sports','other','subway', 'bus', 'train']
time_od_walk = pickle.load(open('time_od_walk.pkl',"rb"))
time_od_cycle = pickle.load(open('time_od_cycle.pkl',"rb"))

for i in TAZ_zones:
    TAZ_data[i] = {}
    TAZ_data[i]['pops'] = 0
    TAZ_data[i]['works'] = 0
    TAZ_data[i]['students'] = 0
    TAZ_data[i]['P_sum_w'] = 0
    TAZ_data[i]['P_sum_c'] = 0
    TAZ_data[i]['A_sum_w'] = 0
    TAZ_data[i]['A_sum_c'] = 0

factor_off_work = 0.6
wc_ratio_offwork = 0.3
factor_off_school = 0.9
wc_ratio_offschool = 0.9
factor_from_home = 0.3
wc_ratio_fromhome = 0.3
factor_business = 0.3
wc_ratio_bussiness = 0.1
factor_off_other = 0.1
wc_ratio_offother = 0.5

print 'OD',sys.getsizeof(OD)
print len(TAZ_zones)
OD_TAZ['walking'] = {}
OD_TAZ['cycling'] = {}
for o in TAZ_zones:
    OD_TAZ['walking'][o] = {}
    OD_TAZ['cycling'][o] = {}
    for d in TAZ_zones:
        OD_TAZ['walking'][o][d] = 0
        OD_TAZ['cycling'][o][d] = 0
print 'OD_TAZ',sys.getsizeof(OD_TAZ)
for i in zones:
    print i
    if zones[i]['zone_id'] < 2000:
        TAZ_data[zones[i]['zone_id']]['pops'] += zones[i]['pops']
        TAZ_data[zones[i]['zone_id']]['works'] += zones[i]['works']
        TAZ_data[zones[i]['zone_id']]['students'] += zones[i]['students']
        off_work_p_wc = zones[i]['works']*factor_off_work*wc_ratio_offwork
        off_school_p_wc = zones[i]['students']*factor_off_school*wc_ratio_offschool
        from_home_p_wc = zones[i]['pops']*factor_from_home * wc_ratio_fromhome
        business_p_wc = zones[i]['business_p']*factor_business*wc_ratio_bussiness
        off_other_p_wc = zones[i]['other_p']*factor_off_other*wc_ratio_offother
        activity_work(i, off_work_p_wc)
        activity_school(i, off_school_p_wc)
        activity_leisure(i, off_work_p_wc, off_school_p_wc, from_home_p_wc)
        activity_business(i, business_p_wc)
        activity_other(i, off_work_p_wc, off_school_p_wc, from_home_p_wc, off_other_p_wc)
    #elif 2000< zones[i]['zone_id'] < 7000:#

    else:
        transit_p_wc = zones[i]['transit_p']*0.65
        transit_a_wc = zones[i]['transit_a']*0.65
        activity_fromtransit(i, transit_p_wc, transit_a_wc)

pickle.dump(OD_TAZ, file('OD_W&C_TAZ.pkl','wb'))
pickle.dump(TAZ_data, file('TAZ_data.pkl','wb'))
Write_OD_to_csv('OD_W&C_TAZ_walking.csv', OD_TAZ['walking'])
Write_OD_to_csv('OD_W&C_TAZ_cycling.csv', OD_TAZ['cycling'])

writer = csv.writer(file('TAZ_data.csv', 'wb'))
TAZs = TAZ_data.keys()
TAZs.sort()
titleline = TAZ_data[TAZs[0]].keys()
firstline = ['id'] + titleline
writer.writerow(firstline)
for taz in TAZs:
    item = [taz]
    for t in titleline:
        item.append(TAZ_data[taz][t])
    writer.writerow(item)
