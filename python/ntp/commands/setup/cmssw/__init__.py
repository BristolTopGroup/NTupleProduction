"""
    setup cmssw:
        Sets up the CMS software in the workspace. Workspace must exist.
        
    Usage:
        setup cmssw version=<cmssw_version>
        
    Parameters:
        version: The version of CMSSW to set up (e.g. CMSSW_8_0_0)
                 Default: What is defined in metadata.json
"""
import logging
from .. import Command as C

LOG = logging.getLogger(__name__)

from .. import CMSSW_VERSION, WORKSPACE, SCRAM_ARCH


class Command(C):
    DEFAULTS = {
        'version': CMSSW_VERSION,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__version = self.__variables['version']
        if not self.__can_run():
            return False

        commands = [
            'cd {workspace}',
            'export SCRAM_ARCH={SCRAM_ARCH}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            '/cvmfs/cms.cern.ch/common/scram project CMSSW {cmssw_version}',
            'cd {cmssw_version}/src',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'git cms-init'
        ]
        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            workspace=WORKSPACE,
            SCRAM_ARCH=SCRAM_ARCH,
            cmssw_version=self.__version
        )

        from ntp.interpreter import call
        call(all_in_one, logger=LOG, shell=True)

        return True

    def __can_run(self):
        import os
        if not os.path.exists(WORKSPACE):
            LOG.error('Workspace does not exist: {0}'.format(WORKSPACE))
            return False
        if os.path.exists(WORKSPACE + '/' + self.__version):
            LOG.error('CMSSW is already set up: {0}'.format(
                WORKSPACE + '/' + self.__version))
            return False
        return True
