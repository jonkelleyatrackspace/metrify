## Log splitter for now

import asyncore, socket, json
import zlib

class gelfTransmitter():
    """ Class capable of zlib compressing and sending over UDP wire."""
    def __init__(self, server='localhost', port=12201, maxChunkSize=8154):
        self.graylog2_server = server
        self.graylog2_port = port
        self.maxChunkSize = maxChunkSize

    def log(self, message):
        UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        zmessage = message #zmessage = zlib.compress(message)
        UDPSock.sendto(zmessage,(self.graylog2_server,self.graylog2_port))
        UDPSock.close()

class AsyncoreServerUDP(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)

        # Bind to port 5005 on all interfaces
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind(('', 5005))

   # Even though UDP is connectionless this is called when it binds to a port
    def handle_connect(self):
        print "Server Started..."

   # This is called everytime there is something to read
    def handle_read(self):
        self.data, self.addr = self.recvfrom(2048)
        self.handle_repeater()
        print str(self.addr)+" >> "+self.data

    def handle_repeater(self):
        pass
        graylog = gelfTransmitter()
        ###graylog.log(json.dumps(self.data))  == to a real graylog host
        graylog.log(self.data)

   # This is called all the time and causes errors if you leave it out.
    def handle_write(self):
        pass

AsyncoreServerUDP()
asyncore.loop()
