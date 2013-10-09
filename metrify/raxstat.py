#!/usr/bin/env python

# ---------------------------------------------------------------------------------------------------
# Logging is the only thing that should work if nothing else. That is why it is prominent.
# ---------------------------------------------------------------------------------------------------
# Logging magic. If nothing else, basic logging _WILL WORK_
import logging
import config
logconfdict = config.context().logger()
INSTANCE_NAME = logconfdict['name']
LOG_OUTFILE = logconfdict['filename']
LOG_FILELEVEL= logconfdict['filelevel']
LOG_STDLEVEL = logconfdict['consolelevel']

# Logger.
logger = logging.getLogger(INSTANCE_NAME)
logger.setLevel(logging.DEBUG)
# File handle.
fh = logging.FileHandler(LOG_OUTFILE)
fh.setLevel(LOG_FILELEVEL)
# Console handle.
ch = logging.StreamHandler()
ch.setLevel(LOG_STDLEVEL) 
# Apply logformat.
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s - PID: %(process)d  ' )
formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s ' )
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# Add handdler to logger instance.
logger.addHandler(fh)
logger.addHandler(ch)
logger.warning('*!*!*!*!*!*!*!*!*!*! START *!*!*!*!*!*!*!*!*!*! ')

CONFIG = config.context().get()



# ---------------------------------------------------------------------------------------------------
# Event handling stack. Calls all the other classes out of the toybox to do stuff.
import eventhandle

import os, fcntl, struct
import asyncore, socket, json, zlib
class AsyncoreServerUDP(asyncore.dispatcher):
    def __init__(self,host='localhost',port=12201,config=None):
        self.config = config
        self.port = port
        self.host = host
        asyncore.dispatcher.__init__(self)
        # Bind to port 5005 on all interfaces
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.bind((host, int(port)))
        except:
            logger.fatal('Failed to bind ' + host +":"+port, exc_info=True)
            raise() # might as well break the loop, we're not viable without bind()

   # Even though UDP is connectionless this is called when it binds to a port
    def handle_connect(self):
        logger.warn( "Now Listening (async) for Datagram @ "+ self.host+":" +str(self.port) + " (udp)")

    def handle_error(self):
        try:
            raise
        except:
            logger.fatal('I just thought you should know there was an EXCEPTION!', exc_info=True)
   # This is called everytime there is something to read
    def handle_read(self):
        self.compressed_packet, self.sourceAddr = self.recvfrom(2048)
        self.data = json.loads(zlib.decompress(self.compressed_packet))
        self.data = json.loads(self.data)
        self.handle_event()
        # Logs event if in debug mode.
        logger.debug ( "DST:localhost:" + str(self.port) + ", SRC:" + str(self.sourceAddr[0])+":"+str(self.sourceAddr[1])+" >>PAYLOAD>> "+json.dumps(self.data,indent=0))

    def handle_event(self):
        handle = eventhandle.event(self.sourceAddr,self.config,self.data)

   # This is called all the time and causes errors if you leave it out.
    def handle_write(self):
        pass # has to exist

for listen,config in CONFIG['gigs'].items():
        (host,port) = listen.split(':')
        AsyncoreServerUDP(host=host,port=port,config=config)

asyncore.loop()

