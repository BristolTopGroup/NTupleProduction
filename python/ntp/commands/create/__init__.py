"""
    create:   Used to create various things
        Usage:
                create <thing>
"""
from .. import Command as C


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = __name__ + " NOT IMPLEMENTED"

        return False
