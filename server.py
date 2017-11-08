from twisted.internet import protocol, reactor
import time
import math
#help(protocol.Protocol)
class TestProtocol(protocol.Protocol):
    name = "anonymous"
    def __init__(self, factory):
        self.factory = factory
        
    def dataReceived(self, data):
        print(self.factory.transfer)
        if self.factory.transfer == True:
            self.factory.file_buffer += data
            print(len(self.factory.file_buffer))
            if len(self.factory.file_buffer) >= self.factory.filesize:
                print("Ready")
                f = open(self.factory.filename, 'wb')
                f.write(bytes(self.factory.file_buffer))
                f.close()
                self.factory.file_buffer = []
                self.factory.filesize = 0
                self.factory.transfer = False
            else:
                print(str(len(self.factory.file_buffer))+ " " + str(self.factory.filesize))
        else:
            opcode = data[0:4]
            message = ""
            string = ""
            user = ""
            splited = []
            buffer = []
            data = data[4:]
            if opcode != b'0010':
                string = data.decode()
                splited = string.split()
                user = splited[0]
            else:
                ext = data[0:4].decode()
                buffer = data[4:]
                
            for i in splited[1:]:
                message = message + " " + i;
                
            if opcode == b"0001":
                for i in self.factory.connections:
                    i.transport.write(b"0001"+(user + " "+ message ).encode())
            
            if opcode == b"0010":
                self.factory.transfer = True

                self.factory.filesize = int(buffer.decode())
                print(str(self.factory.transfer) + " here "+ str(self.factory.filesize))
                self.factory.filename = str(math.floor(time.time())) + ext

                pass
                    
            if opcode == b"0000":   
                self.name = data.decode()
                #print(self.name)
                for i in self.factory.connections:
                    i.transport.write(b"0000"+(self.name).encode())
        
    def connectionMade(self):
        self.factory.connections.append(self)
        print("We have " + str(len(self.factory.connections)) + " connected users");
        
    def connectionLost(self, reason):
        for i in self.factory.connections:
            if i != self:
                i.transport.write(b"0011"(self.name).encode())
        self.factory.connections.remove(self)
        print("We have " + str(len(self.factory.connections)) + " connected users");
        
        
class TestFactory(protocol.Factory):
    number = 0
    filesize = 0
    transfer = False
    file = None
    filename = ""
    connections = []
    file_buffer = []
    
    def __init__(self, num=0):
        self.num = num
    def buildProtocol(self, adress):
        return TestProtocol(self)

reactor.listenTCP(12344, TestFactory())
reactor.run()
