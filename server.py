from twisted.internet import protocol, reactor
#help(protocol.Protocol)
class TestProtocol(protocol.Protocol):
    name = "anonymous"
    def __init__(self, factory):
        self.factory = factory
        
    def dataReceived(self, data):
        string = data.decode()
        print(string)
        splited = string.split()
        user = splited[1]
        message = ""
        for i in splited[2:]:
            message = message + " " + i;
        if string[0] != "0":
            for i in self.factory.connections:
                i.transport.write((user + " "+ message ).encode())
        else:
            self.name = string.split()[1]
            for i in self.factory.connections:
                i.transport.write((self.name+" has connected to the network").encode())
        
    def connectionMade(self):
        self.factory.connections.append(self)
        print("We have " + str(len(self.factory.connections)) + " connected users");
        
    def connectionLost(self, reason):
        for i in self.factory.connections:
            if i != self:
                i.transport.write((self.name+" has disconnected from the network").encode())
        self.factory.connections.remove(self)
        print("We have " + str(len(self.factory.connections)) + " connected users");
        
        
class TestFactory(protocol.Factory):
    number = 0
    connections = []
    def __init__(self, num=0):
        self.num = num
    def buildProtocol(self, adress):
        return TestProtocol(self)

reactor.listenTCP(12344, TestFactory())
reactor.run()
