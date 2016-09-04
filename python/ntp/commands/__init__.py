import os
import pwd
import logging
import copy

LOG = logging.getLogger(__name__)

from hepshell.commands import Command as BaseCommand

class Command(BaseCommand):
    """Base class for all commands"""
    REQUIRE_GRID_CERT = False
    DEFAULTS = {}

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
