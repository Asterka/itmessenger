from twisted.internet import protocol, reactor
import time
import math
#help(protocol.Protocol)
class TestProtocol(protocol.Protocol):
    name = "anonymous"
    def __init__(self, factory):
        self.factory = factory
        
    def dataReceived(self, data):
        opcode = data[0:4]
        data = data[4:]
        buffer = []
        #print(str(opcode))
        message = ""
        string = ""
        user = ""
        splited = []
        
        if opcode == b"0100":
            self.factory.file_size = data.decode();
            print(self.factory.file_size)
            
        if opcode != b'0010' and self.factory.transfer == False:
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
            filename = str(math.floor(time.time())) + ext
            print(self.factory.transfer)
            file = open(filename,"wb")
            
            file.write(buffer);
            for i in self.factory.connections:
                i.transport.write(b"0010"+(filename).encode())
                
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
    transfer = False
    connections = []
    file_buffer = []
    file_size = 0
    def __init__(self, num=0):
        self.num = num
    def buildProtocol(self, adress):
        return TestProtocol(self)

reactor.listenTCP(12344, TestFactory())
reactor.run()
