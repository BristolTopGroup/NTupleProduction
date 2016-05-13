from __future__ import absolute_import
from .interpreter import run_cli
from .interpreter import run_command

import os
import logging

__version__ = '0.0.1'
current_path = os.path.split(__file__)[0]
path_to_base = os.path.join(current_path, '..')
__path__.append(path_to_base)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
# logging to a file
NTPROOT = os.environ['NTPROOT']
formatter = logging.Formatter('%(asctime)s [%(name)s]  %(levelname)s: %(message)s')
fh = logging.FileHandler(NTPROOT + '/workspace/log/ntp.log')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
LOG.addHandler(fh)

# logging to the console
formatter = logging.Formatter('%(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
LOG.addHandler(ch)

__all__ = ['interpreter', 'run_cli', 'run_command']
