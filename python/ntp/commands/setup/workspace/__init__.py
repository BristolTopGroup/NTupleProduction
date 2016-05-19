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

from .. import WORKSPACE, CACHEDIR, LOGDIR, RESULTDIR, TMPDIR

LOG = logging.getLogger(__name__)


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
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
        os.makedirs(CACHEDIR)
        os.makedirs(LOGDIR)
        os.makedirs(RESULTDIR)
        os.makedirs(TMPDIR)
        LOG.info('Created workspace {0}'.format(WORKSPACE))

        return True
