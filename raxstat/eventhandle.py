# Suppose to receive events and then send them out to the protocol level classes.
import logging; logger = logging.getLogger("raxstat") 
import backends

class event(object):
    """ Handles events and data payloads from raxstats and sends them off to the respective services based on config
    setting. If config setting is missing, the event action is skipped. """
    def __init__(self,fromAddress,config,payload):
        """ Catches all events, then calls a method below to call the event. """
        self.fromAddress = fromAddress
        if config['riemannOuts']:
            for output in config['riemannOuts']:
                self.riemannEvent(fromAddress, output['host'], payload)
        if config['graphiteOuts']:
            for output in config['graphiteOuts']:
                self.graphiteEvent(output['host'], payload)
        if config['udprepeatOuts']:
            for output in config['udprepeatOuts']:
                self.udprepeatEvent(output['host'], payload)

    def riemannEvent(self,fromAddress,destination,payload):
        fromAddress = str(fromAddress[0])+":"+str(fromAddress[1])

        endpoint = payload['ept']+"."+payload['eprt']
        statusCode = int(payload['rc'])
        responseLen = int(payload['rl'])
        responseTook = int(payload['tt'])
        if int(responseTook) <= 2:
            COLOR = 'green'
        elif int(responseTook) > 2 and int(responseTook) <= 4:
            COLOR = 'yellow'
        elif int(responseTook) > 4:
            COLOR = 'red'

        riemann = backends.riemannevent()
        name = "latency." + str(endpoint)
        COLOR = 'green'
        riemann.post(destination,host=fromAddress,service=name,state=COLOR,description='Endpoint latency',metric_f=responseTook)
        """ Generates a riemann event for this particular gig """
        logger.debug("output(riemann)-->" + destination)
        
    def graphiteEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        (desthost, destport) = destination.split(':')
        logger.debug("output(graphite)-->" + destination)
        
    def udprepeatEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        logger.debug("output(udp)-->" + destination)
