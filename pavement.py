#!/usr/bin/env python

import sys
from os.path import dirname

# make sure the current directory is in the python import path
sys.path.append(dirname(__file__))

try:
    import paver.doctools
    from paver.easy import options
    
    # default task options
    options(root_dir=dirname(__file__))

    # import our tasks
#    from task.tests import *
    from task.virtualenv import *
    from task.deploy import *
except:
    pass

from paver.setuputils import setup, find_packages

#
# project dependencies
#
install_requires = [
    'python-statsd==1.6.0', # statsd
    'eagleeye==0.2.0' # riemann
]

#
# Setuptools configuration, used to create python .eggs and such.
# See: http://bashelton.com/2009/04/setuptools-tutorial/ for a nice
# setuptools tutorial.
#

setup(
    # metadata
    name="metrify",
    version="0.1",
    author="Jonathan Kelley",
    author_email="jonkelley@gmail.com",
    description="Recieve little UDP packets and make various metrics from it.",
    url="https://github.com/jonkelleyatrackspace/metrify",
    
    # packaging info
    packages=find_packages(exclude=['test', 'test.*', 'task', 'task.*']),
    install_requires=install_requires,
    
    entry_points={
        'console_scripts': [
            'pyjojo = pyjojo.util:main'
        ]
    },
    
    zip_safe=False
)
