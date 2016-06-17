"""
    diff:
        Base command for diffing things
        
    Usage:
        diff <thing>
        
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
