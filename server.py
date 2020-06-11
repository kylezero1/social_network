import socket
import sys
from thread import *

HOST = ''
PORT = 8489

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST,PORT))
except socket.error, msg:
    print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10) # 10 connections
print 'Socket now listening'

CLIENTS = {}

user1 = {
    "username" : "kyle",
    "password" : "tran",
    "numberUnread" : 0, #use this to show all unread messages
    "online" : False
}
user2 = {
    "username" : "mininet",
    "password" : "password",
    "numberUnread" : 0,
    "online" : False
}
user3 = {
    "username" : "admin",
    "password" : "password",
    "numberUnread" : 0,
    "online" : False
}

def clientthread(conn):
    conn.send('Welcome to the server. Please login.\nUsername:')
    #conn.send('Username:')

    username = conn.recv(1024)
    currentUser = 0

    if not username:
        print "No username given"
        conn.close()
    
    conn.send("Username: " + username + "\nPassword:\n")

    #conn.send('Password:')

    password = conn.recv(1024)

    if not password:
        print "No password given"
        conn.close()

    if username == user1["username"]:
        if password == user1["password"]:
            conn.send('Authenticated. Welcome ' + username)
            currentUser = 1
            user1["online"] = True
        else:
            conn.send('Incorrect password')
            conn.close()
    if username == user2["username"]:
        if password == user2["password"]:
            conn.send('Authenticated. Welcome ' + username)
            currentUser = 2
            user2["online"] = True
        else:
            conn.send('Incorrect password')
            conn.close()
    if username == user3["username"]:
        if password == user3["password"]:
            conn.send('Authenticated. Welcome ' + username)
            currentUser = 3
            user3["online"] = True
        else:
            conn.send('Incorrect password')
            conn.close()
    if username != user1["username"] and username != user2["username"] and username != user3["username"]:
        conn.send('Username does not exist')
        conn.close()
    
    while 1:
        data = conn.recv(1024)
        
        if not data:
            break

        #print data
        if data[0] == '1':            
            if currentUser == 1:
                user1["password"] = data[1:]
                conn.send('Password changed.')
            elif currentUser == 2:
                user2["password"] = data[1:]
                conn.send("Password changed.")
            elif currentUser == 3:
                user3["password"] = data[1:]
                conn.send("Password changed.")
        elif data[0] == '2':
            print "Logging out connection"
            if (currentUser == 1):
                user1["online"] = False
            elif (currentUser == 2):
                user2["online"] = False
            elif (currentUser == 3):
                user3["online"] = False
            conn.close()
            break
        elif data[0] == '3':
            if (data[1:] != user1["username"] and data[1:] != user2["username"]
            and data[1:] != user3["username"]):
                conn.send("No user by that name")
            else:
                user = data[1:]
                conn.send("OK")
                data = conn.recv(1024)
                if (user == user1["username"]):
                    nextMessage = "message" + str(user1["numberUnread"] + 1)
                    user1[nextMessage] = data
                    user1["numberUnread"] += 1
                    print ("Added message: " + user1[nextMessage])
                    print ("Number of unread: " + str(user1["numberUnread"]))
                    conn.send("Message sent to " + user)
                elif (user == user2["username"]):
                    nextMessage = "message" + str(user2["numberUnread"] + 1)
                    user2[nextMessage] = data
                    user2["numberUnread"] += 1
                    print ("Added message: " + user2[nextMessage])
                    print ("Number of unread: " + str(user2["numberUnread"]))
                    conn.send("Message sent to " + user)
                elif (user == user3["username"]):
                    nextMessage = "message" + str(user3["numberUnread"] + 1)
                    user3[nextMessage] = data
                    user3["numberUnread"] += 1
                    print ("Added message: " + user3[nextMessage])
                    print ("Number of unread: " + str(user3["numberUnread"]))
                    conn.send("Message sent to " + user)
        elif data[0] == '4':
            if (currentUser == 1):
                conn.send(str(user1["numberUnread"]))
            elif (currentUser == 2):
                conn.send(str(user2["numberUnread"]))
            elif (currentUser == 3):
                conn.send(str(user3["numberUnread"]))
        elif data[0] == '5':
            if (currentUser == 1):
                message = ""
                if (user1["numberUnread"] != 0):
                    for i in range(1, user1["numberUnread"]+1):
                        messageNumber = "message" + str(i)
                        message += user1[messageNumber] + "\n"
                    conn.send(message)
                else:
                    conn.send("No unread messages\n")
            elif (currentUser == 2):
                message = ""
                if (user2["numberUnread"] != 0):
                    for i in range(1, user2["numberUnread"]+1):
                        messageNumber = "message" + str(i)
                        message += user2[messageNumber] + "\n"
                    conn.send(message)
                else:
                    conn.send("No unread messages\n")
            elif (currentUser == 3):
                message = ""
                if (user3["numberUnread"] != 0):
                    for i in range(1, user3["numberUnread"]+1):
                        messageNumber = "message" + str(i)
                        message += user3[messageNumber] + "\n"
                    conn.send(message)
                else:
                    conn.send("No unread messages\n")
        elif data[0] == '6':
            if (user1["online"] == True):
                nextMessage = "message" + str(user1["numberUnread"] + 1)
                user1[nextMessage] = data[1:]
                user1["numberUnread"] += 1
                print ("Added message: " + user1[nextMessage])
                print ("Number of unread: " + str(user1["numberUnread"]))
            if (user2["online"] == True):
                nextMessage = "message" + str(user2["numberUnread"] + 1)
                user2[nextMessage] = data[1:]
                user2["numberUnread"] += 1
                print ("Added message: " + user2[nextMessage])
                print ("Number of unread: " + str(user2["numberUnread"]))
            if (user3["online"] == True):
                nextMessage = "message" + str(user3["numberUnread"] + 1)
                user3[nextMessage] = data[1:]
                user3["numberUnread"] += 1
                print ("Added message: " + user3[nextMessage])
                print ("Number of unread: " + str(user3["numberUnread"]))
                  
            conn.send("Message(s) sent\n")             


    conn.close()

while 1:
    conn, addr = s.accept()

    CLIENTS[conn.fileno()] = conn

    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(clientthread, (conn,))
    
s.close()