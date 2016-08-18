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
