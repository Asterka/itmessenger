from twisted.internet import protocol, reactor
import time
import math
#help(protocol.Protocol)
download_directory = "server_downloads/"

class TestProtocol(protocol.Protocol):
    name = "anonymous"
    file_buffer = []
    filesize = 0
    transfer = False
    file = None
    filename = ""
    def __init__(self, factory):
        self.factory = factory
        
    def dataReceived(self, data):
        if self.transfer == True:
            self.file_buffer += data
            print(len(self.file_buffer))
            if len(self.file_buffer) >= self.filesize:
                for i in self.factory.connections:
                    i.transport.write(b"0101" + (self.name+" "+self.filename).encode())
                f = open(download_directory+self.filename, 'wb')
                f.write(bytes(self.file_buffer))
                f.close()
                self.factory.saved_files.append(self.filename)
                del self.file_buffer[:]
                self.filesize = 0
                self.transfer = False
                pass
            else:
                pass
                
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
            if opcode == b"0111":#user is requesting data
                filename = splited[0]
                size = 0
                if filename in self.factory.saved_files:
                    f = open(download_directory+filename, "rb")
                    buffer = f.read()
                    f.close()
                    size =  len(buffer)
                    print(size)
                    self.transport.write(b"1001"+ (str(len(buffer))+" ").encode())
                    self.transport.write(buffer)
                    
                else:
                    self.transport.write(b"1000")
                pass
            if opcode == b"0001":
                for i in self.factory.connections:
                    i.transport.write(b"0001"+(user + " "+ message ).encode())
            
            if opcode == b"0010":
                self.transfer = True
                del self.file_buffer[:]
                for i in self.factory.connections:
                    i.transport.write(b"0100" + self.name.encode())
                self.filesize = int(buffer.decode())
                self.filename = str(math.floor(time.time())) + ext
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
                i.transport.write(b"0011"+(self.name).encode())
        self.factory.connections.remove(self)
        print("We have " + str(len(self.factory.connections)) + " connected users");
        
        
class TestFactory(protocol.Factory):
    number = 0
    connections = []
    saved_files = []
    def __init__(self, num=0):
        self.num = num
    def buildProtocol(self, adress):
        return TestProtocol(self)

reactor.listenTCP(12344, TestFactory())
reactor.run()
