import yaml, json
import logging; logger = logging.getLogger("raxstat") 

class context(object):
    """ Possibly have a write config option added? """
    def __init__(self,filename='config.yaml'):
        self.filename = filename
    def loadConfigFromSource(self):
        """ This loads a config from your disk, but it could be from
            any source.
        """
        filehandle = file(self.filename, 'r')
        return yaml.load(filehandle)
    def get(self):
        """ This returns a dictionary representation of config, for easy
        use by the rest of this app. """
        config = self.loadConfigFromSource()
        outDict = {}
        
        # Grab log levels
        outDict['log'] = {}
        (outDict['log']['file'], outDict['log']['level']) = (config['logging']['file'], config['logging']['level'])

        gigs = config['gigs']
        
        for gig in gigs:
            listener = gig['listen']
            outDict[listener] = {}
            outDict[listener]['gigs'] = {} 
            outDict[listener]['gigs']['graphiteOuts'] = gig['outputs'].get('graphite',None)
            outDict[listener]['gigs']['riemannOuts'] = gig['outputs'].get('riemann',None)
            outDict[listener]['gigs']['udprepeatOuts'] = gig['outputs'].get('udprepeater',None)
            outDict[listener]['gigs']['unimplementedOuts'] = gig['outputs'].get('lol',None)

        logger.debug( json.dumps(outDict,indent=1) )
        return outDict
if __name__ == '__main__':
    c = context()
    c.get()
