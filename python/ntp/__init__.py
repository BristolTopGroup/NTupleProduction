from __future__ import absolute_import
import os
import sys
import logging

__version__ = '0.0.2'
current_path = os.path.split(__file__)[0]
path_to_base = os.path.join(current_path, '..')
__path__.append(path_to_base)

if not 'HEP_PROJECT_ROOT' in os.environ:
    print("Could not find environmental variable 'HEP_PROJECT_ROOT'")
    print("You need to run 'source bin/env.sh' first!")
    sys.exit(-1)
NTPROOT = os.environ['HEP_PROJECT_ROOT']

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
# logging to a file
formatter = logging.Formatter(
    '%(asctime)s [%(name)s]  %(levelname)s: %(message)s')

logfile = '/tmp/hepshell_{0}.log'.format(os.geteuid())
if os.path.exists(NTPROOT + '/workspace/log'):
    logfile = NTPROOT + '/workspace/log/ntp.log'
fh = logging.FileHandler(logfile)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
LOG.addHandler(fh)

# logging to the console
formatter = logging.Formatter('%(message)s')
ch = logging.StreamHandler()
if not os.environ.get("DEBUG", False):
    ch.setLevel(logging.INFO)
else:
    ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
LOG.addHandler(ch)
