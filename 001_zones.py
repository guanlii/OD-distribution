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


zone_info = {}
reader_zone_info = csv.reader(open('zone_info0918.csv'))
landuses = []
TAZ_zones = []
LU_Convert = {}
LU_Convert[unicode('工业用地','utf-8')] = 'Manuf'
LU_Convert[unicode('公用设施用地','utf-8')] = 'Utili'
LU_Convert[unicode('公共管理与服务设施用地','utf-8')] = 'Admini'
LU_Convert[unicode('农林和其它用地','utf-8')] = 'Farm'
LU_Convert[unicode('水域','utf-8')] = 'Waters'
LU_Convert[unicode('绿地与广场用地','utf-8')] = 'Green'
LU_Convert[unicode('居住用地','utf-8')] = 'Resid'
LU_Convert[unicode('交通设施用地','utf-8')] = 'Trans'
LU_Convert[unicode('商业服务业用地','utf-8')] = 'Commer'
LU_Convert[unicode('物流仓储用地','utf-8')] = 'Logi'
LU_Convert[unicode('发展备用地','utf-8')] = 'Reserv'
LU_Convert[unicode('白色用地','utf-8')] = 'Empty'
LU_Convert[unicode('对外交通用地','utf-8')] = 'OutTrans'

reader_zone_info00 = csv.reader(open('TAZ_all.csv'))
for line in reader_zone_info00:
    taz_id = int(line[0])
    TAZ_zones.append(taz_id)

total_school = 0
total_students = 190000
for line in reader_zone_info:
    land_id = int(float(line[2]))
    zone_id = int(float(line[18]))
    building_area = float(line[8])
    area = float(line[12])
    pops = int(float(line[10]))
    works = int(float(line[11]))
    remark = line[19]
    function = line[9]
    if line[3].decode('gbk') in LU_Convert.keys():
        landuse = LU_Convert[line[3].decode('gbk')]
    else:
        landuse = remark
    landuse = landuse_filter(landuse, function)

    if landuse == 'commer_les':
        l_dens = building_area * 1.0
    elif landuse == 'cul_spt_les':
        if building_area > 100:
            l_dens = building_area * 0.9
        else:
            l_dens = area * 0.5
    if landuse == 'campus':
        l_dens = building_area * 0.1
    elif landuse == 'green_les' or 'Farm':
        l_dens = area * 0.4
    elif landuse == 'Waters':
        l_dens = area * 0.2
    else:
        l_dens = 0
    if landuse == 'office':
        b_a_dens = building_area*0.1
        b_p_dens = building_area*0.1
    elif landuse == 'office_gov':
        b_a_dens = building_area * 0.05
        b_p_dens = building_area * 0.05
    elif landuse == 'Manuf':
        b_a_dens = building_area * 0.003
        b_p_dens = building_area * 0.003
    elif landuse == 'campus':
        b_a_dens = building_area * 0.002
        b_p_dens = building_area * 0.002
    else:
        b_a_dens = 0
        b_p_dens = 0
    if landuse == 'commer_les':
        o_dens = building_area * 0.02
    elif landuse == 'office_gov':
        o_dens = building_area * 0.03
    elif landuse == 'Resid':
        o_dens = building_area * 0.01
    elif landuse == 'office':
        o_dens = building_area * 0.011
    elif landuse == 'Manuf':
        o_dens = building_area * 0.002
    elif landuse == 'campus':
        o_dens = building_area * 0.001
    else:
        o_dens = 0
    print (landuse, building_area, o_dens, b_a_dens)
    if landuse == 'school':
        total_school += building_area
    x = float(line[13])
    y = float(line[14])
    transit_a = float(line[20])
    transit_p = float(line[21])
    zone_info[land_id] = {}
    zone_info[land_id]['building_area'] = building_area
    zone_info[land_id]['area'] = area
    zone_info[land_id]['pops'] = pops
    zone_info[land_id]['works'] = works
    zone_info[land_id]['landuse'] = landuse
    zone_info[land_id]['x'] = x
    zone_info[land_id]['y'] = y
    zone_info[land_id]['zone_id'] = zone_id
    zone_info[land_id]['remarks'] = remark
    zone_info[land_id]['l_dens'] = l_dens
    zone_info[land_id]['b_a_dens'] = b_a_dens
    zone_info[land_id]['b_p_dens'] = b_p_dens
    zone_info[land_id]['business_p'] = b_p_dens * 1####todo
    zone_info[land_id]['o_dens'] = o_dens
    zone_info[land_id]['other_p'] = o_dens * 1####todo
    zone_info[land_id]['transit_a'] = transit_a
    zone_info[land_id]['transit_p'] = transit_p
for zone in zone_info:
    if zone_info[zone]['landuse'] == 'school':
        zone_info[zone]['students'] = float(zone_info[zone]['pops'])
    else:
        zone_info[zone]['students'] = 0
pickle.dump(zone_info, file('zone_info.pkl','wb'))
pickle.dump(TAZ_zones, file('TAZ_zones.pkl','wb'))
