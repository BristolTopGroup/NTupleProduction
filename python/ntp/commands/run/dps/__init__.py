"""
    run dps:
        Just a dummy command to be copied & pasted when you create a new
        command.
        
    Usage:
        run condor analysis dataset=<data set> campaign=<campaign>
        
    Parameters:
        step: 01|02|03|04
"""
import logging
from .. import Command as C

LOG = logging.getLogger(__name__)

class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = "NOT IMPLEMENTED"

        return True
