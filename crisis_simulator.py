#!/usr/bin/python

import json
import argparse

def parseArgs():
   parser = argparse.ArgumentParser()
   parser.add_argument('-u', '--number-of-users', dest='number_users', action='store',
                            default=10, help='Total number of users for the simulation (default: 10)')
   parser.add_argument('-s', '--seed', dest='seed', action='store',
                            help='Seed for the randomizer.')
   parser.add_argument('-f', '--json-file', dest='inventory_file', action='store',
                            help='File Name for the inventory.')
   parser.add_argument('-i', '--iter-timeout', dest='inventory_file', action='store',
                            help='File Name for the inventory.')

   return parser.parse_args()



if __name__ == "__main__":
   options = parseArgs()

   print options
