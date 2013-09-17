# Suppose to receive events and then send them out to the protocol level classes.
import logging; logger = logging.getLogger("raxstat") 
import backends

class event(object):
    """ Handles events and data payloads from raxstats and sends them off to the respective services based on config
    setting. If config setting is missing, the event action is skipped. """
    def __init__(self,config,payload):
        """ Catches all events, then calls a method below to call the event. """
        print payload
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
        logger.debug("output(riemann)-->" + destination)
        
    def graphiteEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        logger.debug("output(graphite)-->" + destination)
        
    def udprepeatEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        logger.debug("output(udp)-->" + destination)
