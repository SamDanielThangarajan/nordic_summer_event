#!/usr/bin/python

import re
import json

providers_g = {}
consumers_g = {}

class Entry:
    def __init__(self,key,type,id,item,quantity,location):
        self.key = key
        self.type = type
        self.id = id
        self.item = item
        self.quantity = quantity
        self.location = location

    def dict(self):
        d = { "key": self.key, "type": self.type, "id": self.id, "item": self.item, "quantity": self.quantity, "location": self.location }
        return d

    def json(self):
        return json.dumps(self.dict())


def parse_json():
    global providers_g
    global consumers_g

    """ Hard code this way """
    file_name = './inventory_database'





