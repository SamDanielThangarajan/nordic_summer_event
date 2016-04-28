# Socket server in python using select function
 
import socket, select
import re

########################################################
### Class Subscriber
###

class Subscriber:
    def __init__(self, number, name, age, loc, skills):
        self.number = number
        self.name = name
        self.age = age
        self.loc = loc
        self.skills = skills

    def print_it(self):
        print ''
        print 'name> ' + self.name
        print 'no> ' + self.number
        print 'age> ' + self.age
        print 'loc> ' + self.loc
        print 'skills> ' + self.skills
        print ''

########################################################
### Subscriber DB Functions
###

subs_db = {}

def populate_subscriber_db():
    global subs_db
    with open('subscriber_profiles') as file_db:
        for line in file_db.readlines():
            """ A_Sam|29|0725838333|ZoneA|engineer_softwaredeveloper_firstaid """
            match = re.match('([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)\|([^\|]+)',line)
            if match:
                subscriber = Subscriber(match.group(3),match.group(1),match.group(2),match.group(4),match.group(5))
                subs_db[subscriber.number] = subscriber


def print_subscriber_db():
    for k,v in subs_db.items():
        v.print_it()


########################################################
### Business Logic
###

def process_data(data):
    if data.startswith('S_'):
        """ Format:
        S_Contact_Item_quantity
        """
        """ S_number_item_qty """

        match = re.match('S_([^_]+)_([^_]+)_([^_]+)',data)

        if match:
            sub = subs_db[match.group(1)]

            with open('inventory.txt', 'a') as the_file:
                input1 = 'Supply_' + sub.number + '_' + sub.loc + '_' + match.group(2) + '_' + match.group(3)
                the_file.write(input1)
    elif data.startswith('D_'):
        """ Format:
        D_Contact_Item_Quantity
        """
        match = re.match('D_([^_]+)_([^_]+)_([^_]+)',data)

        if match:
            sub = subs_db[match.group(1)]
            with open('inventory.txt', 'a') as the_file:
                input1 = 'Demand_' + sub.number + '_' + sub.loc + '_' + match.group(2) + '_' + match.group(3)
                the_file.write(input1)



########################################################
### Server Socket functionality
###

  
if __name__ == "__main__":
    
    populate_subscriber_db()
    print_subscriber_db()


    CONNECTION_LIST = []    # list of socket clients
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
         
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
             
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                 
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    # echo back the client message
                    if data:
                        process_data(data)
                        sock.send('OK ... ' + data)
                 
                # client disconnected, so remove from socket list
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
         
    server_socket.close()
