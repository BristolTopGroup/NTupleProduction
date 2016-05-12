"""
    list:   Used to list things. By default it will list the things to list
        Usage:
                list <thing to list>
"""
from .. import Command as C


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        from ntp.commands.help import Command
        c = Command()
        result = c.run(['list'], variables)
        self.__text = c.get_text()

        return result
