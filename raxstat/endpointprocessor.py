#!/usr/bin/env python
# ---------------------------------------------------------------------------------------------------
# Logging magic. If nothing else, basic logging _WILL WORK_
import config,logging
CONFIG = config.context().get()
# ---
if CONFIG['log']['level'].lower() == 'debug': loglevel = logging.DEBUG
elif  CONFIG['log']['level'].lower() == 'warn': loglevel = logging.WARN
elif  CONFIG['log']['level'].lower() == 'info': loglevel = logging.INFO
elif  CONFIG['log']['level'].lower() == 'notice': loglevel = logging.NOTICE
elif  CONFIG['log']['level'].lower() == 'critical': loglevel = logging.CRITICAL
import logclass; ohai = logclass.instance('raxstat',CONFIG['log']['level'],loglevel,logging.DEBUG)
logger = logging.getLogger("raxstat"); logger.debug('*startup*')
# ---------------------------------------------------------------------------------------------------

import json
logger.debug(json.dumps(CONFIG, indent=3))
import os, fcntl, struct
import asyncore, socket, json, zlib
class gelfTransmitter():
    """ Class capable of zlib compressing and sending over UDP wire."""
    def __init__(self, server='localhost', port=12201, maxChunkSize=8154):
        self.graylog2_server = server
        self.graylog2_port = port
        self.maxChunkSize = maxChunkSize
        self.localAddress = self.return_lan_ip()

    def log(self, message):
        UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        message = json.loads(message)
        message['xCappilaryPeer'] = self.localAddress
        if 'DROP' in message.keys():
            return

        message = json.dumps(message)
        zmessage = zlib.compress(message)
        UDPSock.sendto(zmessage,(self.graylog2_server,self.graylog2_port))
        UDPSock.close()

    def get_interface_ip(self,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

    def return_lan_ip(self):
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name == "posix":

            interfaces = [
                "eth0",
                "eth1",
                "eth2",
                "wlan0",
                "wlan1",
                "wifi0",
                "ath0",
                "ath1",
                "ppp0",
                ]
            for ifname in interfaces:
                try:
                    ip = self.get_interface_ip(ifname)
                    break
                except IOError:
                    pass
        return ip

class AsyncoreServerUDP(asyncore.dispatcher):
    def __init__(self):
        logger.debug('*asyncore.start*')
        asyncore.dispatcher.__init__(self)

        # Bind to port 5005 on all interfaces
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.bind(('127.0.0.1', 5005))

   # Even though UDP is connectionless this is called when it binds to a port
    def handle_connect(self):
        logger.info('Server started.')

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
