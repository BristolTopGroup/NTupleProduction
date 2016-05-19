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
from ntp.commands.setup import CMSSW_SRC, TMPDIR
from ntp import NTPROOT

CMSSW_TAR = os.path.join(TMPDIR, 'cmssw_src')
NTP_TAR = os.path.join(TMPDIR, 'ntp')

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

        self.__prepare(args, variables)

        self.__cleanup(
            CMSSW_TAR, CMSSW_TAR + '.tar', CMSSW_TAR + '.tar.gz',
            NTP_TAR, NTP_TAR + '.tar', NTP_TAR + '.tar.gz',
        )
        self.__make_snapshot(CMSSW_SRC, CMSSW_TAR, '.git*', 'data/test')
        self.__make_snapshot(
            NTPROOT, NTP_TAR, '.git*', 'data/test', 'workspace*', '*.root', '.*')

        self.__create_tar(CMSSW_TAR)
        self.__create_tar(NTP_TAR)

        if self.__variables['cleanup']:
            self.__cleanup(CMSSW_TAR, NTP_TAR)

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

    def __make_snapshot(self, src, dst, *ignore):
        LOG.debug('Making snapshot of {0}'.format(src))
        ignore_func = self.__ignore(*ignore)
        shutil.copytree(src, dst, ignore=ignore_func)

    def __create_tar(self, snapshot):
        file_suffix = 'tar.gz' if self.__variables['compress'] else 'tar'
        archive_format = 'gztar' if self.__variables['compress'] else 'tar'

        LOG.info("Creating {0}.{1}".format(snapshot, file_suffix))

        archive_function = None
        if sys.version_info >= (2, 7):
            archive_function = shutil.make_archive
        else:
            from .backport import make_archive
            archive_function = make_archive

        archive_function(
            snapshot, archive_format, root_dir=snapshot, logger=LOG)

        LOG.info("Created {0}.{1}".format(snapshot, file_suffix))

    def __cleanup(self, *what):
        for item in what:
            if os.path.exists(item):
                LOG.info('Cleaning up {0}'.format(item))
                if os.path.isfile(item):
                    os.remove(item)
                else:
                    shutil.rmtree(item)
