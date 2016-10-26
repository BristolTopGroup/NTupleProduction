"""
    setup dependencies:
        Sets up NTP's dependencies as defined in setup.json
        Workspace & CMSSW must be set up

    Usage:
        setup dependencies
"""
import logging
from .. import Command as C
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('setup dependencies', LOG)
    def run(self, args, variables):
        if not self.__can_run():
            return False
        self.__prepare(args, variables)
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
        ]
        from .. import DEPENDENCIES, CMSSW_SRC
        from hepshell.interpreter import call

        rcs = []
        for dep in DEPENDENCIES:
            LOG.info('Setting up dependency "{0}"'.format(dep['name']))
            provider = dep['provider']
            source = dep['source']
            destination = dep['destination']
            command = ''
            if provider == 'git':
                command = 'git clone {source} {destination}'.format(
                    source=source, destination=destination)
            elif provider == 'git-cms-merge-topic':
                command = 'git-cms-merge-topic {source}'.format(source=source)
            elif provider == 'pip':
                command = 'pip install -U --user {source}'.format(source=source)
            else:
                LOG.error('Unknown provider "{0}"'.format(provider))
                return False
            if 'setup-cmds' in dep:
                additional_commands = ' && '.join(dep['setup-cmds'])
                command = command + ' && ' + additional_commands

            all_in_one = ' && '.join(commands)
            all_in_one = all_in_one + ' && ' + command + ' \n'
            all_in_one = all_in_one.format(CMSSW_SRC=CMSSW_SRC)
            rc = call(all_in_one, logger=LOG, shell=True)
            rcs.append(rc)

        return all(rcs)

    def __can_run(self):
        import os
        from .. import CMSSW_VERSION, WORKSPACE

        if not os.path.exists(WORKSPACE):
            LOG.error('Workspace does not exist: {0}'.format(WORKSPACE))
            return False
        if not os.path.exists(WORKSPACE + '/' + CMSSW_VERSION):
            LOG.error('CMSSW is not set up: {0}'.format(
                WORKSPACE + '/' + CMSSW_VERSION))
            return False
        return True
