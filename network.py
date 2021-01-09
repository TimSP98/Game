import socket


class Network:

    def __init__(self,serverip,port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = serverip # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = port
        self.addr = (self.host, self.port)
        self.inter = {3 : self.interType3, 0 :self.interType0 , 4 : self.interType4}
        data = self.connect()
        self.id , self.nPlayers = map(int,data.split(","))
        print(self.id,self.nPlayers)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def interpolate(self,data):
        # Format is dataType ; data ; *gamestate
        dataType, info = data.split(";")
        dataType = int(dataType)
        self.inter[dataType](info)

    def interType3(self,data):
        data = data[1:-1].split(",")
        for i in range(len(data)):
            data[i] = data[i].strip()[1:-1]
        self._gameP.actionQ = data
        self._gameP.recieved = True
        

    def interType4(self,data):
        # All players have connected, and sets the seed for random
        self._gameP.seed = int(data) 
        self._gameP.recieved = True


    def interType0(self,data):
        self.client.send(str.encode("0;0"))
        return

    def recieve(self):
        try:
            reply = self.client.recv(2048).decode()
            self.interpolate(reply)
            

        except socket.error as e:
            print(str(e))
    def send(self, data,dataType):
        """
        :param data: str
        :return: str
        """
        sendData = f"{dataType};{data}"
        self.client.send(str.encode(sendData))