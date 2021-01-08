import socket


class Network:

    def __init__(self,serverip,port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = serverip # For this to work on your machine this must be equal to the ipv4 address of the machine running the server
                                    # You can find this address by typing ipconfig in CMD and copying the ipv4 address. Again this must be the servers
                                    # ipv4 address. This feild will be the same for all your clients.
        self.port = port
        self.addr = (self.host, self.port)

        data = self.connect()
        self.id , self.nPlayers = map(int,data.split(","))
        print(self.id,self.nPlayers)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def recieve(self):
        try:
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            print(str(e))
    def send(self, data,dataType):
        """
        :param data: str
        :return: str
        """
        data = str(dataType) + ";" + ":".join([str(item) for item in data])
        self.client.send(str.encode(data))