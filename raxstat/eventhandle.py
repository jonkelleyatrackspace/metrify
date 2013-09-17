# Suppose to receive events and then send them out to the protocol level classes.
import logging
logger = logging.getLogger("raxstat") 
import preampOut

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
        """ Specialized logic that formats and sends remarkable conditions to Riemann.
        """
        # We'll use these.
        fromAddress = str(fromAddress[0])+":"+str(fromAddress[1])
        endpoint = payload['ept']+"."+payload['eprt']
        statusCode = int(payload['rc'])
        responseLen = int(payload['rl'])
        responseTook = int(payload['tt'])

        ###########################################################
        # Post latency metrics.

        # Colorize based on suckyness.
        if int(responseTook) <= 1:
            COLOR = 'green'
        elif int(responseTook) > 1 and int(responseTook) <= 4:
            COLOR = 'yellow'
        elif int(responseTook) > 4:
            COLOR = 'red'

        riemann = preampOut.riemannevent()
        name = "latency." + str(endpoint)
        riemann.post(destination,host=fromAddress,service=name,state=COLOR,description='Endpoint Latency',metric_f=1)
        logger.debug("output.riemann.latency:"+endpoint+" -->" + destination)
        ###########################################################
        # Post statuscode metrics.
        
        # Colorized based on suckyness.
        if int(statusCode) in [200]:
            COLOR = 'green'
        else:
            COLOR = 'red'

        riemann = preampOut.riemannevent()
        name = "statuscode." + str(endpoint)
        riemann.post(destination,host=fromAddress,service=name,state=COLOR,description='Status Code',metric_f=1)
        logger.debug("output.riemann.statcode:"+endpoint+" -->" + destination)

        return
        
    def graphiteEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        (desthost, destport) = destination.split(':')
        logger.debug("output(graphite)-->" + destination)

        return
        
    def udprepeatEvent(self,destination,payload):
        """ Generates a riemann event for this particular gig """
        udp = preampOut.udpevent(destination)
        udp.emit(payload)
        logger.debug("output(udp)-->" + destination)
        
        return
