import socket
import _thread as thread
import sys
import json

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

        self.currentID = 1
        self.connectedPlayers = 0

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = socket.gethostbyname(self.serveripv4)

        try:
            self.s.bind((self.serveripv4,self.port))
        except socket.error as e:
            print(str(e))

        self.s.listen(self.nPlayers)
        print("waiting for connection")



    def shutdown(self):
        sys.exit()

    def interpolate(self,data):
        dataType, info = data.split(";")
        dataType = int(dataType)
        info = info.split(":")
        print(dataType)
        print(info)

    
    def threaded_client(self,conn):
        initInfo = f"{self.currentID},{self.nPlayers}"
        conn.send(str.encode(initInfo))
        self.currentID +=1
        reply = ''
        while True:
            if self.connectedPlayers != self.nPlayers:
                #Waiting for people to connect
                continue
            print("yes")
            data = conn.recv(2048)
            if not data:
                conn.send(str.encode("Goodbye"))
                break

            # Decode the information
            recieved = data.decode('utf-8')
            self.interpolate(recieved)
            
        conn.close()
        self.shutdown()

    def run(self):
        self.start = False
        while True:
            conn, addr = self.s.accept()
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

