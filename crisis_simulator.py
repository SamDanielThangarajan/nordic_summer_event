#!/usr/bin/python

import json
import time
import names
import random
import argparse

import Matcher

provider_role = 'provider'
consumer_role = 'consumer'
item_list = [ 'food', 'shelter', 'water', 'clothing', 'medical', 'manual labor', 'transport']
location  = [ "Adambakkam", "Adyar", "Alandur", "Alwarpet", "Alwarthirunagar",
              "Ambattur", "Aminjikarai", "Anakaputhur", "Anna Nagar", "Annanur", "Arumbakkam",
              "Ashok Nagar", "Avadi", "Ayanavaram", "Besant Nagar", "Basin Bridge", "Chepauk",
              "Chetput", "Chintadripet", "Chitlapakkam", "Choolai", "Choolaimedu", "Chrompet",
              "Egmore", "Ekkaduthangal", "Ennore", "Foreshore Estate", "Fort St. George",
              "George Town", "Gopalapuram", "Government Estate", "Guindy", "IIT Madras",
              "Injambakkam", "ICF", "Iyyapanthangal", "Jafferkhanpet", "Karapakkam",
              "Kattivakkam", "Kazhipattur", "K.K. Nagar", "Keelkattalai", "Kelambakkam",
              "Kilpauk", "Kodambakkam", "Kodungaiyur", "Kolathur", "Korattur", "Korukkupet",
              "Kottivakkam", "Kotturpuram", "Kottur", "Kovalam", "Kovilambakkam", "Koyambedu",
              "Kundrathur", "Madhavaram", "Madhavaram Milk Colony", "Madipakkam",
              "Madambakkam", "Maduravoyal", "Manali", "Manali New Town", "Manapakkam",
              "Mandaveli", "Mangadu", "Mannadi", "Mathur", "Medavakkam", "Meenambakkam", 
              "MGR Nagar", "Minjur", "Mogappair", "MKB Nagar", "Mount Road", "Moolakadai",
              "Moulivakkam", "Mugalivakkam", "Mudichur", "Mylapore", "Nandanam",
              "Nanganallur", "Navalur", "Neelankarai", "Nemilichery", "Nesapakkam",
              "Nolambur", "Noombal", "Nungambakkam", "Otteri", "Padi", "Pakkam", "Palavakkam",
              "Pallavaram", "Pallikaranai", "Pammal", "Park Town", "Parry's Corner",
              "Pattabiram", "Pattaravakkam", "Pazhavanthangal", "Peerkankaranai", "Perambur",
              "Peravallur", "Perumbakkam", "Perungalathur", "Perungudi", "Pozhichalur",
              "Poonamallee", "Porur", "Pudupet", "Purasaiwalkam", "Puthagaram", "Puzhal",
              "Puzhuthivakkam", "Raj Bhavan", "Ramavaram", "Red Hills", "Royapettah",
              "Royapuram", "Saidapet", "Saligramam", "Santhome", "Sembakkam", "Selaiyur",
              "Shenoy Nagar", "Sholavaram", "Sholinganallur", "Sithalapakkam", "Sowcarpet",
              "St.Thomas Mount", "Tambaram", "Teynampet", "Tharamani", "T. Nagar",
              "Thirumangalam", "Thirumullaivoyal", "Thiruneermalai", "Thiruninravur",
              "Thiruvanmiyur", "Tiruverkadu", "Thiruvotriyur", "Tirusulam", "Tiruvallikeni",
              "Tondiarpet", "United India Colony", "Vandalur", "Vadapalani", "Valasaravakkam",
              "Vallalar Nagar", "Vanagaram", "Velachery", "Villivakkam", "Virugambakkam",
              "Vyasarpadi", "Washermanpet", "West Mambalam" ]

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


def generate_subscriber_subscribers( number_users ):
    total_subscribers = random.randint(1, number_users)
    print "Provisioning %d users in the system ..." % options.number_users

    subscribers = []
    for i in range(1, total_subscribers):
        subscribers.append(
                    {'name': names.get_full_name(), 
                     'phone': generate_phone_number(),
                     'offered_services': generate_offer()
                    })

    return subscribers


def generate_phone_number():
    cc  = "+91"
    ndc = random.randint(7000,9000)
    sn  = random.randint(0,999999)
    return "%s%d%06d" % (cc, ndc, sn)


def generate_offer():
    sample_size = random.randint(1, len(item_list))
    return random.sample(item_list, sample_size)


def generate_initial_inventory(subscribers):
    inventory = {'entries': []}

    for subscriber in subscribers:
        is_subscriber_in_need  = random.random() < 0.70
        is_subscriber_offering = random.random() < 0.50

        subscriber_current_location = random.choice(location)

        if is_subscriber_offering:
            for item in subscriber['offered_services']:
                entry = Matcher.Entry("identifier",
                                      provider_role,
                                      subscriber['phone'],
                                      item,
                                      random.randint(1,10),
                                      subscriber_current_location)
                inventory['entries'].append( entry.dict() )

        if is_subscriber_in_need:
            entry = Matcher.Entry("identifier",
                                  consumer_role,
                                  subscriber['phone'],
                                  random.choice(item_list),
                                  random.randint(1,10),
                                  subscriber_current_location)
            inventory['entries'].append( entry.dict() )
    return inventory


def simulate(iteration, subscribers, inventory):
    print "Iteration:%d, Simulating" % iteration


if __name__ == "__main__":
    # Parse input arguments
    options = parseArgs()

    # Set the seed to the one passed as an argument
    random.seed( options.seed )

    # Subscriber profile databse
    subscribers = generate_subscriber_subscribers( options.number_users )

    # The initialize the inventory
    inventory = generate_initial_inventory(subscribers)

    iteration = 0
    while True:
        iteration = iteration + 1

        with open(options.inventory_file, 'w') as output_file:
            json.dump(inventory, output_file, indent=4, sort_keys=True)

            simulate(iteration, subscribers, inventory)

        time.sleep(float(options.iter_timeout))
