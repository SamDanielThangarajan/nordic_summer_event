#!/usr/bin/python

import json
import time
import names
import random
import argparse

def parseArgs():
   parser = argparse.ArgumentParser()
   parser.add_argument('-u', '--number-of-users', dest='number_users', action='store',
                            default=100, help='Total number of users for the simulation (default: 10)')
   parser.add_argument('-s', '--seed', dest='seed', action='store',
                            help='Seed for the randomizer.')
   parser.add_argument('-f', '--json-file', dest='inventory_file', action='store',
                            required=True, help='File Name for the inventory.')
   parser.add_argument('-i', '--iter-timeout', dest='iter_timeout',
                            action='store', type=float, default=1.0,
                            help='Timeout for populating db.')

   return parser.parse_args()


def simulate(iteration, max_users, inventory):
    print "Iteration:%d, Simulating %d" % (iteration, random.randint(1,100))

def generate_phone_number():
    cc  = "+91"
    ndc = random.randint(7000,9000)
    sn  = random.randint(0,999999)
    return "%s%d%06d" % (cc, ndc, sn)

def generate_offer():
    return [ random.sample(['food', 'shelter', 'water', 'clothing', 'medical'], 2) ]

def generate_subscriber_profile_database( number_users ):
    total_subscribers = random.randint(1, number_users)
    print "Provisioning %d users in the system ..." % options.number_users

    subscribers = []
    for i in range(1, total_subscribers):
        subscribers.append( 
                    {'name': names.get_full_name(), 
                     'phone': generate_phone_number(),
                     'offered_services': generate_offer()
                    }
                )
    print "Generated %s" % subscribers


if __name__ == "__main__":
    # Parse input arguments
    options = parseArgs()

    # Set the seed to the one passed as an argument
    random.seed( options.seed )

    # Subscriber profile databse
    profile_database = generate_subscriber_profile_database( options.number_users )

    # The inital inventory is empty
    inventory = {'entries': []}

    with open(options.inventory_file, 'w') as output_file:

        json.dump(inventory, output_file)

        iteration = 0
        while True:
            iteration = iteration + 1

            simulate(iteration, options.number_users, inventory)

            time.sleep(float(options.iter_timeout))
