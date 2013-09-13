import logging

import graypy

my_logger = logging.getLogger('test_logger')
my_logger.setLevel(logging.DEBUG)

handler = graypy.GELFHandler('localhost', 12201)
my_logger.addHandler(handler)

my_logger.debug('Hello Graylog2.')

try:
    puff_the_magic_dragon()
except NameError:
    my_logger.debug('broke', exc_info=1)
