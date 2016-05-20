"""
    run:    Runs the n-tuple production.
            All run commands require a valid grid certificate as they
            either read data from the grid via XRootD or run on grid
            resources.
        Usage:
            run [<where>] [sample=<X>]
        Parameters:
            where:    Where to run NTP. Can be grid|condor|local.
                      For location specific parameters, please run
                        help run <where>
                      Default: local
            sample:   Which sample to run over.
                      Default: test
"""

from .. import Command as C
import subprocess


class Command(C):
    REQUIRE_GRID_CERT = True

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        from .local import Command
        c = Command()
        result = c.run(args, variables)
        self.__text = c.get_text()

        return result

    def __prepare(self, args, variables):
        super(Command, self).__prepare(args, variables)

    def __extract_params(self):
        args = []
        for var, value in self.__variables.items():
            if var in self.DEFAULTS:
                continue
            args.append('{0}={1}'.format(var, value))
        return ' '.join(args)

    def __format_input_files(self, input_files):
        results = []
        for f in input_files:
            results.append('"{0}"'.format(f))
        return ',\n'.join(results)
