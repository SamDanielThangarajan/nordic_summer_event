#!/usr/bin/python

import re
import json

providers_g = {}
consumers_g = {}

class Entry:
    def __init__(self,type,id,item,quantity,location):
        self.type = type
        self.id = id
        self.item = item
        self.quantity = quantity
        self.location = location


def parse_json():
    global providers_g
    global consumers_g

    """ Hard code this way """
    file_name = './inventory_database'





