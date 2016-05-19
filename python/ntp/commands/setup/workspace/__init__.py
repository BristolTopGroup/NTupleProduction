"""
    setup workspace:
        Creates the workspace structure.
        
    Usage:
        setup workspace [force=false]
        
    Parameters:
        force: forces workspace to be deleted if it already exists.
"""
import logging
import os
import sys
import shutil
from .. import Command as C

LOG = logging.getLogger(__name__)


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        from .. import WORKSPACE
        self.__prepare(args, variables)
        if os.path.exists(WORKSPACE):
            LOG.warning('Workspace already exists')
            if self.__variables['force']:
                LOG.info('Deleting existing workspace')
                if os.path.exists(WORKSPACE + '.save'):
                    shutil.rmtree(WORKSPACE + '.save')
                shutil.move(WORKSPACE, WORKSPACE + '.save')
            else:
                sys.exit(-1)

        LOG.info('Creating workspace')
        os.makedirs(WORKSPACE + '/cache')
        os.makedirs(WORKSPACE + '/log')
        os.makedirs(WORKSPACE + '/results')
        os.makedirs(WORKSPACE + '/tmp')
        LOG.info('Created workspace {0}'.format(WORKSPACE))

        return True
