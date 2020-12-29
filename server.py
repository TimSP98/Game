import socket
from _thread import *
import sys
import json

with open("ServerConf.json","r") as infile:
    settings = json.load(infile)
for param,val in settings.items():
    print(param,val)
    try:
        exec(param+"="+str(val))
    except NameError:
        exec(param+"='"+str(val)+"'")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = serverip
port = serverPort
server_ip = socket.gethostbyname(server)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen(nPlayers)
print("waiting for connection")


currentId = 0
pos = ["0:50,50","1:100,100"]
connectedPlayers = 0

def shutdown():
    sys.exit()


def threaded_client(conn):
    global currentId, pos, nPlayers, connectedPlayers
    initInfo = str(currentId) + ","+ str(nPlayers)
    conn.send(str.encode(initInfo))
    currentId = "1"
    reply = ''
    while True:
        if connectedPlayers != nPlayers:
            #Waiting for people to connect
            continue

        data = conn.recv(2048)
        reply = data.decode('utf-8')
        if not data:
            conn.send(str.encode("Goodbye"))
            break
        else:
            print("Recieved: "+ reply)
            arr = reply.split(":")
            pid = int(arr[0])
            pos[pid] = reply

            if pid == 0: nid = 1
            if pid == 1: nid = 0

            reply = pos[nid][:]
            print("Sending: "+ reply)

        conn.close()
        shutdown()

start = False
while True:
    conn, addr = s.accept()
    print("Connected to:",addr)
    connectedPlayers +=1
    if( connectedPlayers == nPlayers):          start = True
    if(start and connectedPlayers != nPlayers): break
    start_new_thread(threaded_client, (conn,))