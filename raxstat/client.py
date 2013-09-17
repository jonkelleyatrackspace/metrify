import socket, asyncore

#from socket import *
import zlib

class Client():
    def __init__(self, server='localhost', port=12202, maxChunkSize=8154):
        self.graylog2_server = server
        self.graylog2_port = port
        self.maxChunkSize = maxChunkSize

    def log(self, message):
        UDPSock = socket(AF_INET,SOCK_DGRAM)
        zmessage = zlib.compress(message)
        UDPSock.sendto(zmessage,(self.graylog2_server,self.graylog2_port))
        UDPSock.close()

class AsyncoreClientUDP(asyncore.dispatcher):

   def __init__(self, server, port):
      self.server = server
      self.port = port
      self.buffer = ""

      # Network Connection Magic!
      asyncore.dispatcher.__init__(self)
      self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.bind( ('', 0) ) # bind to all interfaces and a "random" free port.
      print "Connecting..."

   # Once a "connection" is made do this stuff.
   def handle_connect(self):
      print "Connected"
   
   # If a "connection" is closed do this stuff.
   def handle_close(self):
      self.close()

   # If a message has arrived, process it.
   def handle_read(self):
      data, addr = self.recv(2048)
      print data

   # Actually sends the message if there was something in the buffer.
   def handle_write(self):
      if self.buffer != "":
         print self.buffer

#    = zlib.compress(message)

         import json
         message={}
         message['ept'] = 'identity.api.rackspacecloud.com' # endpoint
         message['eprt'] = '443' # port
         message['rc'] = '200' # stat code
         message['rl'] = '0' # resp len
         message['tt'] = self.buffer # time taken
         message = json.dumps(message)
         message = zlib.compress(json.dumps(message))


         sent = self.sendto(message, (self.server, self.port))
         self.buffer = self.buffer[sent:]

connection = AsyncoreClientUDP("127.0.0.1",12201) # create the "connection"
while 1:
   asyncore.loop(count = 10) # Check for upto 10 packets this call?
   connection.buffer += raw_input(" GELF > ") # raw_input (this is a blocking call)
