"""
    run dps:
        Runs the DailyPythonScripts (DPS) analysis code to produce the final
        set of results (plots, tables & intermediate results).
        
        
    Usage:
        run dps steps=[{steps}] [noop=0]
        
    Parameters:
        noop:     'NO OPeration', will not run AnalysisSoftware. Default: false
        where:    Where to run the analysis. Can be 'local|DICE'.
                  Default is 'local'.
        test:     Run just one job for testing (DICE only). Default: false.
"""
from __future__ import print_function
import os
import logging
import glob
import shutil

from .. import Command as C
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)


class Command(C):

    DEFAULTS = {
        'steps': '0,1,2,3,4,5',
        'variable': 'MET',
        'noop': False,
        'where': 'local',
        'test': False,
        'centre-of-mass-energy': 13,
        'visiblePS': True
    }

    REQUIRE_GRID_CERT = False

    def __init__(self, path=__file__, doc=__doc__):
        from .local import STEPS
        doc = doc.format(steps = ','.join(STEPS.keys()))
        super(Command, self).__init__(path, doc)

    @time_function('run dps', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        
        if self.__variables['where'] == 'local':
            from .local import Command as PayLoad
        else:
            from .DICE import Command as PayLoad
        
        payload = PayLoad()
        return payload.run(self.__args, self.__variables)
        

    