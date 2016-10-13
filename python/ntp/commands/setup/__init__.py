"""
    setup:
        Sets up NTP with all its dependencies. It will run the
        following commands in that order:
            ntp setup workspace
            ntp setup cmssw
            ntp setup links
            ntp setup dependencies
            ntp compile

        Usage:
            setup [ntp_tag] [force=true] [compile=true]
                  [from_tarball=<path to file>]

        Parameters:
            ntp_tag: specifies which version of NTP to load. Default is
                      'run2:latest' which is equal to 'master'

            force: forces workspace to be deleted if it already exists.

            from_tarball: Uses given tar file to create workspace.
                          Default: NOT SET.
"""
import json
import shutil
import os
import sys
import optparse
import subprocess
import logging

from .. import Command as C
from hepshell.interpreter import time_function
from ntp import NTPROOT

LOG = logging.getLogger(__name__)
WORKSPACE = os.path.join(NTPROOT, 'workspace')
CACHEDIR = os.path.join(WORKSPACE, 'cache')
LOGDIR = os.path.join(WORKSPACE, 'log')
RESULTDIR = os.path.join(WORKSPACE, 'results')
TMPDIR = os.path.join(WORKSPACE, 'tmp')

DPS_RESULTDIR = os.path.join(RESULTDIR, 'dps')


def get_setup():
    setup_file = os.path.join(NTPROOT, 'setup.json')
    with open(setup_file) as setup_file:
        setup = json.load(setup_file)
    return setup

SETUP = get_setup()
CMSSW_VERSION = SETUP['cmssw_version']
CMSSW_BASE = os.path.join(WORKSPACE, CMSSW_VERSION)
CMSSW_SRC = os.path.join(CMSSW_BASE, 'src')
DEPENDENCIES = SETUP['dependencies']
LINKS = SETUP['links']
SCRAM_ARCH = SETUP['scram_arch']
DESTINATION = SETUP['destination']


class Command(C):

    DEFAULTS = {
        'force': False,
        'ntp_tag': 'run2:latest',  # == master
        'compile': True,
        'ncpu': 1,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('setup', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        if 'from_tarball' in self.__variables:
            return self.__tarball_setup(args, variables)
        else:
            ntp_tag = self.__variables['ntp_tag']
            if args:
                ntp_tag = args[0]
            return self.__default_setup(args, variables, ntp_tag)

    def __default_setup(self, args, variables, ntp_tag='master'):
        from .workspace import Command as SetupWorkspace
        c = SetupWorkspace()
        c.run(args, variables)

        from .cmssw import Command as SetupCMSSW
        c = SetupCMSSW()
        c.run(args, variables)

        from .links import Command as SetupLinks
        c = SetupLinks()
        c.run(args, variables)

        from .dependencies import Command as SetupDeps
        c = SetupDeps()
        c.run(args, variables)

        if self.__variables['compile']:
            from ..compile import Command as Compile
            c = Compile()
            c.run(args, variables)

        return True

    def __tarball_setup(self, args, variables):
        tarball = self.__variables['from_tarball']
        if not os.path.exists(tarball):
            LOG.error('The given tarball {0} does not exist!'.format(tarball))
            return False
        tarball = os.path.abspath(tarball)
        LOG.info('Using tarball {0} for setup.'.format(tarball))

        variables['init-git'] = False

        from .workspace import Command as SetupWorkspace
        c = SetupWorkspace()
        c.run(args, variables)

        from .cmssw import Command as SetupCMSSW
        c = SetupCMSSW()
        c.run(args, variables)

        self.__extract_tarball(tarball)

        if self.__variables['compile']:
            from ..compile import Command as Compile
            c = Compile()
            c.run(args, variables)

        return True

    def __extract_tarball(self, tarball):
        commands = [
            'cd {CMSSW_BASE}',
            'tar xzf {tarball}',
            'cd {CMSSW_SRC}',
            'echo "{tarball}" > .tarball_setup'
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_BASE=CMSSW_BASE,
            CMSSW_SRC=CMSSW_SRC,
            tarball=tarball,
        )

        from hepshell.interpreter import call
        call(all_in_one, logger=LOG, shell=True)
