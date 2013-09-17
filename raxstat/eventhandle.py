# Suppose to receive events and then send them out to the protocol level classes.
import logging; logger = logging.getLogger("raxstat") 

class event(object):
    def __init__(self,config,payload):
        """ Catches all events, then calls a method below to call the event. """
        if config['riemannOuts']:
            for output in config['riemannOuts']:
                self.riemannEvent(output['host'], payload)
        if config['graphiteOuts']:
            for output in config['graphiteOuts']:
                self.graphiteEvent(output['host'], payload)
        if config['udprepeatOuts']:
            for output in config['udprepeatOuts']:
                self.udprepeatEvent(output['host'], payload)

    def riemannEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        logger.debug("RIEMANN -->" + destination +  str(payload))
        
    def graphiteEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        logger.debug("GRAPHITE -->" + destination +  str(payload))
        
    def udprepeatEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        logger.debug("UDP_REPEAT -->" + destination  +  str(payload))
