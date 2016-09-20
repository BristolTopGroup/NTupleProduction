"""
    pick bins:
        Runs DailyPythonScripts/dps/analysis/xsection/00_pick_bins.py
        
    Usage:
        pick bins [-c] [-v]
        
    Flags:
        -c: Combine channels
        -v: Use visible phase space
"""
import logging
from ntp.commands.run import Command as C
from hepshell.interpreter import time_function
LOG = logging.getLogger(__name__)


class Command(C):
    REQUIRE_GRID_CERT = False

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('pick bins', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        import importlib
        pick_bins = importlib.import_module(
            'dps.analysis.xsection.00_pick_bins', 'dps.analysis.xsection')
        LOG.info('Running dps.analysis.xsection.00_pick_bins.main()')
        pick_bins.main()
        return True
