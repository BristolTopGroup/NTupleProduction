from __future__ import absolute_import
from .interpreter import run_cli
from .interpreter import run_command

import os
__version__ = '0.0.1'
current_path = os.path.split(__file__)[0]
path_to_base = os.path.join(current_path, '..')
__path__.append(path_to_base)


__all__ = ['interpreter', 'run_cli', 'run_command']
