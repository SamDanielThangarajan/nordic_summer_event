#!/usr/bin/python

import json
import time
import argparse

def parseArgs():
   parser = argparse.ArgumentParser()
   parser.add_argument('-u', '--number-of-users', dest='number_users', action='store',
                            default=10, help='Total number of users for the simulation (default: 10)')
   parser.add_argument('-s', '--seed', dest='seed', action='store',
                            help='Seed for the randomizer.')
   parser.add_argument('-f', '--json-file', dest='inventory_file', action='store',
                            help='File Name for the inventory.')
   parser.add_argument('-i', '--iter-timeout', dest='iter_timeout', action='store',
                            help='Timeout for populating db.')

   return parser.parse_args()


def simulate(iteration, max_users, seed):
    print "Iteration:%d, Simulating " % iteration


if __name__ == "__main__":
   options = parseArgs()
   iteration = 0
   while True:
       iteration = iteration + 1
       simulate(iteration, options.number_users, options.seed)
       time.sleep(float(options.iter_timeout))
