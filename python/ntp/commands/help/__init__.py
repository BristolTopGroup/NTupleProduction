"""
    help:   Lists help for available commands. Pass a command as parameter
            to get the help for just that command
        Usage:
                help [command]
"""
from __future__ import print_function
from .. import Command as C
import textwrap


class Command(C):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        import ntp.interpreter
        HIERARCHY = ntp.interpreter.HIERARCHY
        self.__prepare(args, variables)

        if not args:
            # print everything
            self.__text = self.__collect_help_text(HIERARCHY, 'COMMANDS:')
        else:
            tmp = HIERARCHY
            for arg in args:
                if arg in tmp:
                    tmp = tmp[arg]
                else:
                    self.__text = 'Could not find command "' + \
                        ' '.join(args) + '"'
                    return False
            self.__text = self.__collect_help_text(tmp, 'COMMAND:')

        return True

    def __collect_help_text(self, hierarchy, text, level=0):
        """
            Walks through the command hierarchy and adds help texts to 'text'.
        """
        if 'this' in hierarchy:
            help_str = hierarchy['this']().help()
            help_str = textwrap.dedent(help_str)
            for line in help_str.split('\n'):
                text += '    ' * level
                text += line
                text += '\n'
            if len(hierarchy) > 1:
                text += '    ' * level + '**SUBCOMMANDS**:\n'
                text += '        ' * level + '-' * 50
        # add subcommands
        for name, command in hierarchy.items():
            if name == 'this':
                continue
            text = self.__collect_help_text(
                command, text, level=level + 1)

        if level == 1:
            text += '    ' + '=' * 74

        return text
