"""
    run dps steps=[{steps}] where=local:
        Runs the DailyPythonScripts (DPS) analysis code to produce the final
        set of results (plots, tables & intermediate results) on the current machine.
        See 'ntp help run dps' for a complete list of parameters
"""
from __future__ import print_function
import logging
import importlib
from collections import OrderedDict

from . import Command as C
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)

STEPS = OrderedDict([
    ('0', 'ntp.commands.create.dps.configs'),
    ('1', 'ntp.commands.get.ttjet.normalisation'),
    ('2', 'ntp.commands.unfold.and.measure'),
    ('3', 'ntp.commands.calculate.systematics'),
    ('4', 'ntp.commands.make.plots'),
    ('5', 'ntp.commands.make.tables'),
])


class Command(C):

    DEFAULTS = C.DEFAULTS

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(steps = ','.join(STEPS.keys()))
        super(Command, self).__init__(path, doc)

    @time_function('run dps where=local', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        steps = self.__variables['steps']
        if isinstance(steps, (bool, int, float)): 
            # single numbers are converted to either bool or float
            # we need to undo this
            steps = [str(int(steps))]
        else:
            steps = steps.split(',')
            steps = [int(x) for x in steps]
        self.__steps = sorted(steps)

        results = []
        for step in self.__steps:
            result = self.__run(step)
            results.append(result)

    def __run(self, step):
        module = STEPS[step]
        Step = importlib.import_module(module).Command
        s = Step()
        s.run([], self.__variables)
