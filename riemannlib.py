#!/bin/env python
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

        # Now lets use our external module
        riemann = externalModule(RIEMANNHOST, RIEMANNPORT)
        riemann.submit(payloadDict)

