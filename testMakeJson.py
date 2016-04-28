#!/usr/bin/python

import json
from Matcher import Entry

#class Entry:
#    def __init__(self,key,type,id,item,quantity,location):




def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

hungry = Entry("ABC", "consumer", "070123", "food", "2", "madrid-S")
thirsty = Entry("DEF", "consumer", "070456", "water", 5, "madrid-N")

rich = Entry("AAA", "provider", "070678", "food", 3, "madrid-S")
camel = Entry("BBB", "provider", "070987", "water", 3, "madrid-N")

print hungry.dict()

print hungry.json()