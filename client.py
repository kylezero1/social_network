import socket
import getpass
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

print 'Socket Created'

host = '10.0.0.4'
port = 8489

try:
    s.connect((host,port))
except:
    print 'Could not connect to ' + host + ' on port ' + port
    sys.exit()

reply = s.recv(1024)
print reply

message = raw_input() #username
s.sendall(message)

reply = s.recv(1024)
print reply

password = getpass.getpass(prompt="")
s.sendall(password)

reply = s.recv(1024)
print reply

if (reply[0] == 'A' and reply[1] == 'u' and reply[2] == 't'
    and reply[3] == 'h' and reply[4] == 'e' and reply[5] == 'n'
    and reply[6] == 't' and reply[7] == 'i' and reply[8] == 'c'
    and reply[9] == 'a' and reply[10] == 't' and reply[11] == 'e' and reply[12] == 'd'):
    while 1:
        message = raw_input("\nEnter 1 to change password\nEnter 2 to logout \nEnter 3 to send a PM\nEnter 4 to see number of unread messages\nEnter 5 to read all unread\nEnter 6 to send a message to all people online\n")
        if message == "1": #change pass
            password = raw_input("What would you like to change your password to? \n")
            message = "1" + password
            s.sendall(message)
            reply = s.recv(1024)
            print reply
        elif message == "2": #logout
            s.sendall("2")
            print ("Logging out")
            s.close()
            sys.exit()
        elif message == "3": #send pm
            target = raw_input("Who would you like to send a PM to?\n")
            message = "3" + target
            s.sendall(message)
            reply = s.recv(1024)
            if (reply[0] == 'N' and reply[1] == 'o'):
                print ("No user by that name, please try again")
            elif (reply[0] == 'O' and reply[1] == 'K'):
                message = raw_input("Please enter your desired message\n")
                s.sendall(message)
                reply = s.recv(1024)
                print reply
        elif message == "4": #see number unread
            s.sendall("4")
            reply = s.recv(1024)
            print ("Number of unread messages: " + reply)
        elif message == "5": #read all unread
            s.sendall("5")
            reply = s.recv(1024)
            print reply
        elif message == "6": #broadcast
            message = raw_input("What would you like to broadcast?\n")
            s.sendall("6" + message)
            reply = s.recv(1024)
            print reply
        else:
            print "Please enter a correct option"


else:
    print "Error authenticating. Closing connection"
    s.close()
    sys.exit()