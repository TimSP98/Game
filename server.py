import socket
import _thread as thread
import sys
import json
import time
import random


class Server:

    def __init__(self):
        with open("ServerConf.json","r") as infile:
            settings = json.load(infile)
        for param,val in settings.items():
            print(param,val)
            try:
                exec(f"self.{param}={val}")
            except NameError:
                exec(f"self.{param}='{val}'")

        # 1 = alive and 3 actions, 2 = I ded 
        self.inter = {1:self.interType1 , 2:self.interType2}
        self.currentID = 0
        self.connectedPlayers = 0
        self.playersAlive = [False]*self.nPlayers
        self.allActions = [None]*self.nPlayers
        self.finalOrder = []
        self.called = False

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = socket.gethostbyname(self.serveripv4)

        try:
            self.s.bind((self.serveripv4,self.port))
        except socket.error as e:
            print(str(e))

        self.s.listen(self.nPlayers)
        print("waiting for connection")

    def interType1(self,info):
        # Info is a list of the three actions that info[0][1] should act, bit scuffed I know
        info = info[1:-1].split(",")
        for i in range(len(info)):
            info[i] = info[i].strip()[1:-1]
        print("info:",info)
        playerID = int(info[0][0])
        print(info)
        print(playerID)
        self.allActions[playerID] = info
    
    def interType2(self,info):
        # info should be just an int of the player who sent the data, as he is dead
        self.playersAlive[info[0]] = False

    def shutdown(self):
        sys.exit()

    def interpolate(self,data):
        # Format is dataType ; data ; *gamestate
        dataType, info = data.split(";")
        dataType = int(dataType)
        self.inter[dataType](info)

    def allSubmitted(self):
        returnVal = True
        for i in range(self.nPlayers):
            if(self.allActions[i] == None and self.playersAlive[i]):
                returnVal = False
        return returnVal
    
    def allActionOrder(self):
        self.called = True
        self.finalOrder = []
        for _ in range(3):
            for i in range(self.nPlayers):
                if (self.allActions[i]):
                    action = self.allActions[i].pop(0)
                    self.finalOrder.append(action)
        self.finalOrder = str(self.finalOrder)
        print(self.finalOrder)


    def threaded_client(self,conn):
        initInfo = f"{self.currentID},{self.nPlayers}"
        conn.send(str.encode(initInfo))
        self.playersAlive[self.currentID] = True
        self.currentID +=1
        reply = ''
        while(self.connectedPlayers != self.nPlayers):
            #Waiting for people to connect
            conn.send(str.encode("0;0"))
            conn.recv(2048)

        #Send info that all players have connected
        conn.send(str.encode(f"4;{self.seed}"))
        while True:
            data = conn.recv(2048)
            if not data:
                conn.send(str.encode("Goodbye"))
                break

            # Decode the information
            recieved = data.decode('utf-8')
            self.interpolate(recieved)
            while(not self.allSubmitted()):
                conn.send(str.encode("0;0"))
                conn.recv(2048)
            #All (alive) players have sent in their actions
            if(not self.called):
                self.allActionOrder()
            # dataType and info
            conn.send(str.encode("3;"+self.finalOrder))
            time.sleep(20)
            self.called = False
            self.allActions = [None]*self.nPlayers
            
        conn.close()
        self.shutdown()

    def run(self):
        self.start = False
        self.seed = random.randint(0,1000)
        while True:
            conn, addr = self.s.accept()
            if(self.connectedPlayers == self.nPlayers):
                print("declined",addr)
                continue
            print("Connected to:",addr)
            self.connectedPlayers +=1
            if( self.connectedPlayers == self.nPlayers): start = True
            if(self.start and self.connectedPlayers != self.nPlayers): break
            thread.start_new_thread(self.threaded_client, (conn,))


def main():
    srv = Server()
    srv.run() 

if __name__ == "__main__":
    main()

