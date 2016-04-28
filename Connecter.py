#!/usr/bin/python

import re
import json

providers_g = {}
consumers_g = {}

#####################################################
### Entry
###
class Entry:
    def __init__(self,type,id,item,quantity,location):
        self.type = type
        self.id = id
        self.item = item
        self.quantity = quantity
        self.location = location

def test_populate_consumers(id,item,quantity,location):
    global consumers_g
    entry = Entry('consumer',id,item,quantity,location)
    if item+'-'+location in consumers_g:
        print 'Appending a new entry'
        consumers_g[item+'-'+location].append(entry)
    else:
        print 'creating a new entry'
        consumers_g[item+'-'+location] = [entry]

def test_populate_producers(id,item,quantity,location):
    global providers_g
    entry = Entry('producer',id,item,quantity,location)
    if item+'-'+location in providers_g:
        print 'Appending a new entry'
        providers_g[item+'-'+location].append(entry)
    else:
        print 'creating a new entry'
        providers_g[item+'-'+location] = [entry]

#####################################################
### Group
###

class Group:
    def __init__(self, entries):
        self.entries = entries

        
#####################################################
### Pool
###
class Pool:
    def __init__(self, demand_group, supply_group):
        self.d_groups = demand_group
        self.s_groups = supply_group



if __name__ == "__main__":
    test_populate_consumers('A','food',5,'zonea')
    test_populate_consumers('B','cloths',5,'zonea')
    test_populate_consumers('C','food',5,'zonea')

    test_populate_producers('P1','food',5,'zonea')
    test_populate_producers('P2','food',5,'zonea')
    test_populate_producers('P2','cloths',5,'zonea')


    """
    Pool - Food-zonea
      - Group-Demand { A,C }
      - Group Supply {P1, P2}
      - Group Transport (X)
    """

    pools = {}
    

    for grp_name in providers_g.keys():
        if grp_name in consumers_g:
            pools[grp_name] = Pool(consumers_g[grp_name],providers_g[grp_name])

    for grp_name in pools.keys():
        print grp_name
        print ''
        pool = pools[grp_name]
        consumers = pool.d_groups
        providers = pool.s_groups

        for consumer in consumers:
            provid_list = []
            for producer in providers:
                provid_list.append(producer.id)
            print consumer.id + '--->' + str(provid_list)





