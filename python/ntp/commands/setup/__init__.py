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

        Parameters:
            ntp_tag:  specifies which version of NTP to load. Default is
                      'run2:latest' which is equal to 'master'

            force:    forces workspace to be deleted if it already exists.
"""
import json
import shutil
import os
import sys
import optparse
import subprocess
import logging

from .. import Command as C
from ntp import NTPROOT

LOG = logging.getLogger(__name__)
WORKSPACE = NTPROOT + '/workspace'


def get_metadata():
    metadata = {}
    with open(NTPROOT + '/metadata.json') as metadata_file:
        metadata = json.load(metadata_file)
    return metadata

METADATA = get_metadata()
CMSSW_VERSION = METADATA['cmssw_version']
CMSSW_SRC = WORKSPACE + '/{0}/src'.format(CMSSW_VERSION)
DEPENDENCIES = METADATA['dependencies']
LINKS = METADATA['links']
SCRAM_ARCH = METADATA['scram_arch']
DESTINATION = METADATA['destination']


class Command(C):

    DEFAULTS = {
        'force': False,
        'ntp_tag': 'run2:latest',  # == master
        'compile': True,
        'ncpu': 1,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)

        ntp_tag = self.__variables['ntp_tag']
        if args:
            ntp_tag = args[0]

        from .workspace import Command as SetupWorkspace
        c = SetupWorkspace()
        c.run(args, variables)

        from .cmssw import Commmand as SetupCMSSW
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
