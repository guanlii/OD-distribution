# -*- coding: UTF-8 -*-

import gc

print( 'running 001/007')
gc.disable()
execfile("001_zones.py")
gc.enable()
print ('running 002/007')
gc.disable()
execfile('002_time_od.py')
gc.enable()
print( 'running 003/007')
gc.disable()
execfile("003_potentials_00.py")
gc.enable()
print ('running 004/007')
gc.disable()
execfile("004_PA_bases.py")
gc.enable()
print ('running 005/007')
execfile('005_W&C_trips_00_lite.py')

print( 'running 006/007')
execfile('006_zone_buses.py')

print( 'running 007/007')
execfile('007_Final_ODs.py')

