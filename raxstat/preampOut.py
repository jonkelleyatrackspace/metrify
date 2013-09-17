#!/bin/env python
import config,logging
logger = logging.getLogger('raxstat')

#jonkelley sep 15 2013
# Class wrapper for: https://github.com/WoLpH/python-statsd
import statsd

# This files goal is to do a generic class wrap of a 'riemann' interface to do this:
#riemann = Riemann('127.0.0.1', 5555)
#riemann.submit({'host':'WebServer1',
#                'service': 'MyCoolWebApp_APIResponse',
#                'state': 'critical',
#                'description': 'my_api_function() took 72ms',
#                'metric_f': '72'})

class graphiteevent(object):
    """ This will instanciate a graphite as a common interface, and let you put metrics its way.
        We will use the python-statsd library as it is the most legitimate.

    Usage:
    >> graphite = graphiteevent('127.0.0.1','8125')
    """
    def __init__(self,hostv='localhost',portv='8125',appname='helloworld'):
        statsd.Connection.set_defaults(host=hostv, port=portv, sample_rate=1, disabled=False)
        self.YourApplicationName = appname

    def plotaverage(self,name='SomeName',key='somekey:',value=3):
        average = statsd.Average(self.YourApplicationName, connection)
        average.send('SomeName', 'somekey:%d'.format(value))

    def plotraw(self,name='SomeName',value=3,timestamp=None):
        # None means the server generates epoch, otherwise insert an epoch value
        raw = statsd.Raw(self.YourApplicationName, connection)
        raw.send(name, value, timestamp)

    def plotguage(self,name='SomeName',value=3):
        guage = statsd.Guage(self.YourApplicationName)
        gauge.send(name, value)

    def movecounter(self,name='somename',value='1'):
        counter = statsd.Counter(self.YourApplicationName)
        counter.send(name, value)


#jonkelley sep 15 2013
# Class wrapper for: https://github.com/hawkowl/eagleeye/blob/master/README.md

from eagleeye.riemann import Riemann as externalModule

# This files goal is to do a generic class wrap of a 'riemann' interface to do this:
#riemann = Riemann('127.0.0.1', 5555)
#riemann.submit({'host':'WebServer1',
#                'service': 'MyCoolWebApp_APIResponse',
#                'state': 'critical',
#                'description': 'my_api_function() took 72ms',
#                'metric_f': '72'})

class riemannevent(object):
    """ This will instanciate a riemann class as a common interface, and let you put metrics its way.
    
    Usage:
    >> riemann = riemannevent()
    >> riemann.post('127.0.0.1:5555',host='Web1',service='MyCoolWebApp_APIResponse'
    >>                                     state='critical',description='function() took 72ms',
    >>                                     metric_f='72' )
    """
    def post(self,riemannendpoint,**kwargs):
        (RIEMANNHOST, RIEMANNPORT ) = riemannendpoint.split(':')
        logger.info("RIEMANN output -> " + RIEMANNHOST+":"+RIEMANNPORT)
        RIEMANNPORT = int(RIEMANNPORT)
        
        host        = kwargs.get("host")
        service     = kwargs.get("service")
        state       = kwargs.get("state")
        description = kwargs.get("description")
        metric_f    = kwargs.get("metric_f")

        payloadDict = {}
        if host:
            payloadDict['host'] = host
        if service:
            payloadDict['service'] = service
        if state:
            payloadDict['state'] = state
        if description:
            payloadDict['description'] = description
        if metric_f:
            payloadDict['metric_f'] = metric_f
        logger.debug("RIEMANN payload-> " + str(payloadDict))
        # Now lets use our external module
        riemann = externalModule(RIEMANNHOST, RIEMANNPORT)
        riemann.submit(payloadDict)

