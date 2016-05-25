"""
    setup links:
        Links the relevant folders (as defined in metadata.json) to the
        CMSSW setup. Requires workspace & CMSSW to be set up
        
    Usage:
        setup links
"""
import logging
from .. import Command as C

LOG = logging.getLogger(__name__)


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        if not self.__can_run():
            return False
        self.__prepare(args, variables)
        from .. import CMSSW_SRC, DESTINATION, LINKS
        from ntp import NTPROOT

        c1 = 'mkdir -p {cmssw_src}/{destination}'.format(
            cmssw_src=CMSSW_SRC,
            destination=DESTINATION
        )
        commands = [c1]

        for l in LINKS:
            command = 'ln -s {NTPROOT}/{link} {cmssw_src}/{destination}/{link}'
            command = command.format(NTPROOT=NTPROOT,
                                     link=l,
                                     cmssw_src=CMSSW_SRC,
                                     destination=DESTINATION)
            commands.append(command)

        all_in_one = ' && '.join(commands)

        from ntp.interpreter import call
        call(all_in_one, logger=LOG, shell=True)

        return True

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
