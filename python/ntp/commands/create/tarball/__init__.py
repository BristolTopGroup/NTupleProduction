"""
    create tarball:   Creates a tar-ball of the current workspace excluding
                      all temporary
        Usage:
                create tarball [compress=1,cleanup=1]
        Parameters:
            compress: will compress the tarball using gzip. Default is 1.
            cleanup: will delete the snapshot of the workspace. default is 1.
"""
import logging
import os
import sys
import shutil

from .. import Command as C
from ntp.interpreter import time_function

LOG = logging.getLogger(__name__)


class Command(C):
    DEFAULTS = {
        'cleanup': True,
        'compress': True,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('create tarball', LOG)
    def run(self, args, variables):
        from ntp import NTPROOT
        from ntp.commands.setup import CMSSW_SRC

        WORKSPACE = NTPROOT + '/workspace'
        TMP = WORKSPACE + '/tmp/ntp'

        self.__prepare(args, variables)
        if os.path.exists(TMP):
            shutil.rmtree(TMP)
        LOG.debug('Making snapshot of {0}'.format(CMSSW_SRC))
        ignore = self.__ignore('.git*', 'data/test')
        shutil.copytree(CMSSW_SRC, TMP, ignore=ignore)

        LOG.info("Creating workspace/tmp/ntp.tar.gz")

        archive_format = 'gztar' if self.__variables['compress'] else 'tar'
        archive_function = None
        if sys.version_info >= (2, 7):
            archive_function = shutil.make_archive
        else:
            from .backport import make_archive
            archive_function = make_archive
        archive_function(
            TMP, archive_format, root_dir=TMP, logger=LOG)

        if self.__variables['compress']:
            self.__text = "Created {0}.tar.gz".format(TMP)
        else:
            self.__text = "Created {0}.tar".format(TMP)

        if self.__variables['cleanup']:
            LOG.debug('Cleaning up snapshot of {0}'.format(CMSSW_SRC))
            shutil.rmtree(TMP)

        return True

    def __ignore(self, *patterns):
        import fnmatch

        def _ignore_patterns(path, names):
            ignored_names = []
            for pattern in patterns:
                # default from shutil.ignore_patterns
                ignored_names.extend(fnmatch.filter(names, pattern))
                # now check for folder
                if '/' in pattern:
                    tokens = pattern.split('/')
                    base = '/'.join(tokens[:-2])
                    name = tokens[-1]
                    if base in path:
                        ignored_names.extend(fnmatch.filter(names, name))
            return set(ignored_names)
        return _ignore_patterns
