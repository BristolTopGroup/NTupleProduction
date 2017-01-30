"""
    run ntuple where=local:
                Runs the n-tuple production on the current machine.
                See 'ntp help run ntuple' for a complete list of parameters
"""
from __future__ import print_function
import os
import logging

from . import Command as ParentCommand
from hepshell.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC, TMPDIR, RESULTDIR, LOGDIR

LOG = logging.getLogger(__name__)
PSET = os.path.join(TMPDIR, 'pset.py')
OUTPUT_FILE = os.path.join(RESULTDIR, '{ds}_ntuple.root')
BTAG_CALIB_FILE = os.path.join(CMSSW_SRC, 'BristolAnalysis/NTupleTools/data/BTagSF/CSVv2Moriond17_2017_1_26_BtoH.csv')

class Command(ParentCommand):

    DEFAULTS = ParentCommand.DEFAULTS

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('run local', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        input_files = self.__variables['input_files']
        LOG.debug(
            "Using files for NTP input:\n{0}".format('\n'.join(input_files)))

        self.__output_file = self.__variables['output_file']

        self.__write_pset(input_files)

        if not self.__variables['noop']:
            code = self.__run_cmssw()
            self.__text = "Ran {PSET}\n"
            self.__text += "Logging information can be found in {LOGDIR}/ntp.log\n"
            if code == 0:
                self.__text += "Created ntuples: {OUTPUT_FILE}\n"
                self.__text = self.__text.format(
                    PSET=PSET, LOGDIR=LOGDIR, OUTPUT_FILE=self.__output_file)
            else:
                self.__text += "CMSSW experienced an error,"
                self.__text += " return code: {code}\n"
                self.__text = self.__text.format(
                    PSET=PSET, LOGDIR=LOGDIR, code=code)
                return False

        else:
            LOG.info('Found "noop", not running CMSSW')

        return True

    def __write_pset(self, input_files):
        nevents = int(self.__variables['nevents'])
        input_files = self.__format_input_files(input_files)

        with open(PSET, 'w+') as f:
            content = self.__variables['pset_template'].format(
                nevents=nevents,
                input_files=input_files,
                OUTPUT_FILE=self.__output_file,
                BTAG_CALIB_FILE=BTAG_CALIB_FILE,
                JSON_URL=self.__variables['json_url'],
            )
            f.write(content)

    @time_function('__run_cmssw', LOG)
    def __run_cmssw(self):
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'cmsRun {PSET} {params}',
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC, PSET=PSET, params=self.__extract_params())

        LOG.info("Executing cmsRun")
        from hepshell.interpreter import call
        code, _, _ = call(
            [all_in_one], LOG, stdout_log_level=logging.INFO, shell=True)

        return code
