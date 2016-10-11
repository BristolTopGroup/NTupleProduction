"""
    run analysis where=local:
        Runs the ntuple based analysis code (AnalysisSoftware) to produce the
        final set of trees on the current machine.
        See 'ntp help run analysis' for a complete list of parameters
"""
from __future__ import print_function
import os
import logging
import glob
import shutil

from . import Command as C
from hepshell.interpreter import time_function
from ntp.commands.setup import CMSSW_SRC, TMPDIR, LOGDIR
from . import BAT_BASE

LOG = logging.getLogger(__name__)
PSET = os.path.join(TMPDIR, 'bat.py')


class Command(C):

    DEFAULTS = C.DEFAULTS

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('run analysis where=local', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        self.__write_pset(self.__variables['input_files'])

        no_operation = self.__variables['noop']
        if no_operation:
            LOG.info('Found "noop", not running BAT')
            return True
        else:
            return self.__run()

    def __write_pset(self, input_files):
        nevents = int(self.__variables['nevents'])
        input_files = self.__format_input_files(input_files)

        with open(PSET, 'w+') as f:
            content = self.__variables['pset_template'].format(
                nevents=nevents,
                input_files=input_files,
                BAT_BASE=BAT_BASE,
                maxEvents=nevents,
                mode=self.__variables['mode'],
                dataset=self.__variables['dataset'],
            )
            f.write(content)

    def __run(self):
        dataset = self.__variables['dataset']
        mode = self.__variables['mode']
        output_file = self.__variables['output_file']
        code = self.__run_analysisSoftware(dataset, mode, output_file)
        self.__text = "Ran {PSET}\n"
        self.__text += "Logging information can be found in {LOGDIR}/ntp.log\n"
        if code == 0:
            self.__text += "Created atOutput: {OUTPUT_FILE}\n"
            self.__text = self.__text.format(
                PSET=PSET, LOGDIR=LOGDIR, OUTPUT_FILE=output_file)
        else:
            self.__text += "BAT experienced an error,"
            self.__text += " return code: {code}\n"
            self.__text = self.__text.format(
                PSET=PSET, LOGDIR=LOGDIR, code=code)
            if code == 139:
                LOG.warning(
                    '########################################################')
                LOG.warning(
                    '####  Ignoring segault (hopefully) at the end of AS ####')
                LOG.warning(
                    '########################################################')
                return True
            return False

        return True

    @time_function('__run_analysisSoftware', LOG)
    def __run_analysisSoftware(self, dataset, mode, output_file):
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'sample="{dataset}" analysisMode="{mode}" BAT {PSET} {params}',
        ]

        # BAT expects parameters to start with '--'
        params = self.__extract_additional_parameters(
            prefix='--', skip=['isData', 'isReHLT', 'isTTbarMC'],
        )

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC,
            dataset=dataset,
            mode=mode,
            PSET=PSET,
            params=params,
        )
        print (params)

        LOG.info("Executing BAT")
        from hepshell.interpreter import call
        code, _, _ = call(
            [all_in_one], LOG, stdout_log_level=logging.INFO, shell=True)
        self.__move_output_file(output_file)

        return code

    def __move_output_file(self, output_file):
        output_files = glob.glob(
            '{CMSSW_SRC}/*.root'.format(CMSSW_SRC=CMSSW_SRC))

        for f in output_files:
            if 'tree_' in f:
                LOG.debug('Moving {0} -> {1}'.format(f, output_file))
                shutil.move(f, output_file)
            else:
                LOG.debug('Removing obsolete file: {0}'.format(f))
                os.remove(f)
