#!/usr/bin/python

import json
import time
import names
import random
import argparse

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
    return [ random.sample(item_list, sample_size) ]


def generate_initial_inventory(subscribers):
    inventory = {'entries': []}

    for subscriber in subscribers:
        is_subscriber_in_need  = random.random() > 0.6
        is_subscriber_offering = random.random() > 0.6

        if is_subscriber_offering:
            for offer in subscriber['offered_services']:
                inventory['entries'].append({'type': provider_role,
                                             'id': subscriber['phone'],
                                             'item': offer,
                                             'quantity': random.randint(1,10),
                                             'location': random.choice(location)
                                             })

        if is_subscriber_in_need:
            inventory['entries'].append({'type': consumer_role,
                                         'id': subscriber['phone'],
                                         'item': random.choice(item_list),
                                         'quantity': random.randint(1,10),
                                         'location': random.choice(location) })
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
            json.dump(inventory, output_file)

            simulate(iteration, subscribers, inventory)

        time.sleep(float(options.iter_timeout))
