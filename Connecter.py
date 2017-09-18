#!/usr/bin/python

import re
import json
import time

providers_g = {}
consumers_g = {}

#####################################################
### Entry
###
class Entry:
    def __init__(self,key,type,id,item,quantity,location):
        self.key = key
        self.type = type
        self.id = id
        self.item = item
        self.quantity = quantity
        self.location = location

    def dict(self):
        d = { "key": self.key, 
              "type": self.type, 
              "id": self.id, 
              "item": self.item, 
              "quantity": self.quantity, 
              "location": self.location }
        return d

    def json(self):
        return json.dumps(self.dict())

def test_populate_consumers(id,item,quantity,location):
    global consumers_g
    entry = Entry('','consumer',id,item,quantity,location)
    if item+'-'+location in consumers_g:
        consumers_g[item+'-'+location].append(entry)
    else:
        consumers_g[item+'-'+location] = [entry]

def test_populate_producers(id,item,quantity,location):
    global providers_g
    entry = Entry('','producer',id,item,quantity,location)
    if item+'-'+location in providers_g:
        providers_g[item+'-'+location].append(entry)
    else:
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




def main():


    global providers_g
    global consumers_g

    providers_g = {}
    consumers_g = {}

    jdata = open('./inventory.txt')
    data = json.load(jdata)

    entries = data['entries']

    for entry in entries:
        if entry['type'] == 'provider':
            test_populate_producers(entry['id'],entry['item'],entry['quantity'],entry['location'])
        else:
            test_populate_consumers(entry['id'],entry['item'],entry['quantity'],entry['location'])


    
    """
    test_populate_consumers('A','food',5,'zonea')
    test_populate_consumers('B','cloths',5,'zonea')
    test_populate_consumers('C','food',5,'zonea')

    test_populate_producers('P1','food',5,'zonea')
    test_populate_producers('P2','food',5,'zonea')
    test_populate_producers('P2','cloths',5,'zonea')

    """
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
        print 'Pool : ' + grp_name
        print ''
        pool = pools[grp_name]
        consumers = pool.d_groups
        providers = pool.s_groups

        for consumer in consumers:
            provid_list = []
            for producer in providers:
                provid_list.append(producer.id)
            print consumer.id + '--->' + str(provid_list)

        print ''
        print '----------------------------------------'

if __name__ == "__main__":
    while True:
        main()
        print 'end'
        time.sleep(2)



