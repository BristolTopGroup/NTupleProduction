"""
    compile:
        Compiles NTP and all of its dependencies. Requires workspace, CMSSW
        and NTP links to be set up.
        
    Usage:
        compile [ncpu=1]
        
    Parameters:
        npcu: number of CPUs to be used for compilation. Default: 1
"""
import logging
from .. import Command as C
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)


class Command(C):

    DEFAULTS = {
        'ncpu': 1,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('compile', LOG)
    def run(self, args, variables):
        if not self.__can_run():
            return False
        from ..setup import CMSSW_SRC
        self.__prepare(args, variables)
        n_jobs = int(self.__variables['ncpu'])
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'scram b -j{n_jobs}'
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(CMSSW_SRC=CMSSW_SRC, n_jobs=n_jobs)

        from hepshell.interpreter import call
        call(all_in_one, logger=LOG, shell=True)

        return True

    def __can_run(self):
        import os
        from ..setup import CMSSW_SRC, DESTINATION, LINKS

        if not os.path.exists(CMSSW_SRC):
            LOG.error('CMSSW is not set up: {0}'.format(CMSSW_SRC))
            return False

        if not os.path.exists(CMSSW_SRC + '/.tarball_setup'):
            # only needs links if it is not a tarball setup
            for link in LINKS:
                path = '{cmssw_src}/{destination}/{link}'.format(
                    cmssw_src=CMSSW_SRC, destination=DESTINATION, link=link)
                if not os.path.exists(path):
                    LOG.error('Link {0} is not set up.'.format(path))
                    return False
        return True
