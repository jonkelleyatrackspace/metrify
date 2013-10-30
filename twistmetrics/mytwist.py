#!/usr/bin/python

import sys


from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import time

# Here's a UDP version of the simplest possible protocol
class EchoUDP(DatagramProtocol):
    def datagramReceived(self, datagram, (host, port)):
        now = time.localtime(time.time())  
        timeStr = str(time.strftime("%y/%m/%d %H:%M:%S",now)) 
        print "received %r from %s:%d at %s" % (datagram, host, port, timeStr)

## Sender
from random import randint
import json
class EchoClientDatagramProtocol(DatagramProtocol):
    def __init__(self):
        self.instancename =  randint(2,9999999)
    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8001)
        self.sendDatagram()

    def sendDatagram(self):
        for i in range(1,100):
            datagram = json.dumps({ "name" : str(self.instancename) , "value" : str(i)})
            self.transport.write(datagram)

def main():
    args = sys.argv
    print 'args:', str(args)

    if any(item.startswith('list') for item in args): # Listener
        print "Listener selected."
        reactor.listenUDP(8000, EchoUDP())
        reactor.listenUDP(8001, EchoUDP())
        reactor.run()
    elif any(item.startswith('send') for item in args): # Sender
        print "Sender selected."
        protocol = EchoClientDatagramProtocol()
        reactor.listenUDP(0, protocol)
        reactor.run()
    else:
        print("Seems ambiguous: %s" % args)

if __name__ == '__main__':
    main()




