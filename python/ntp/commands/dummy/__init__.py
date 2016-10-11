"""
    dummy:
        Just a dummy command to be copied & pasted when you create a new
        command.
        
    Usage:
        dummy <nothing> [something]
        
    Parameters:
        something: a weird parameter
"""
import logging
from ntp.commands import Command as C
from hepshell.interpreter import time_function
LOG = logging.getLogger(__name__)


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('dummy', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = "Running dummy command"

        return True
