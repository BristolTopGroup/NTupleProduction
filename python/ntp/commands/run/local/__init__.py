"""
DEPRECATED
    run local:  Runs the n-tuple production on the current machine.
                All run commands require a valid grid certificate as they
                either read data from the grid via XRootD or run on grid
                resources.
                The command will use python/run/miniAODToNTuple_cfg.py.
        Usage:
            run local [campaign=<X>]  [dataset=<X>] [files=file1,file2,..]
                      [nevents=<N>] [noop=false] [output_file=<file name>]

        Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in crab/*
                      Default is 'Test'.
            dataset:  Alias for the single dataset you want to run over. Corresponds
                      to the file names (without extension) in crab/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is 'TTJets_PowhegPythia8'.
                      This parameter is ignored if parameter file is given.
            files:    Instead of running on a specific dataset, run over the
                      given (comma-separated) list of files
            nevents:  Number of events to process.
                      Default is 1000.
            noop:     'NO OPeration', will not run CMSSW. Default: false
            output_file: Name of the output file. Default: ntuple.root
            json_url: URL to JSON file, e.g. https://cms-service-dqm.web.cern.ch/../..._JSON.txt
                      Default: ''
"""
from __future__ import print_function
import os
import logging

from .. import Command as C
from hepshell.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC, TMPDIR, RESULTDIR, LOGDIR
from crab.util import find_input_files

LOG = logging.getLogger(__name__)
PSET = os.path.join(TMPDIR, 'pset.py')
OUTPUT_FILE = os.path.join(RESULTDIR, '{ds}_ntuple.root')
from ntp.commands.run.ntuple.template import PYCONF
BTAG_CALIB_FILE = os.path.join(CMSSW_SRC, 'BristolAnalysis', 'NTupleTools', 'data','BTagSF','CSVv2.csv')
BASE = """
import FWCore.ParameterSet.Config as cms
from run.miniAODToNTuple_cfg import process

process.maxEvents.input = cms.untracked.int32({nevents})

process.TFileService.fileName='{OUTPUT_FILE}'

# In order to work around the limitation of 255 parameters to a python function
# we pass 1 tuple of all the files to the vstring function
# see
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePoolInputSources#Example_3_More_than_255_input_fi
process.source.fileNames = cms.untracked.vstring(
*(
{input_files},
)
)

process.jetUserData.btagCalibrationFile = cms.string('{BTAG_CALIB_FILE}')

if '{JSON_URL}':
    import FWCore.PythonUtilities.LumiList as LumiList
    process.source.lumisToProcess = LumiList.LumiList(url = '{JSON_URL}').getVLuminosityBlockRange()

"""


class Command(C):

    DEFAULTS = {
        'campaign': 'Test',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 1000,
        'files': '',
        'noop': False,
        'output_file': OUTPUT_FILE.format(ds='TTJets_PowhegPythia8'),
        'pset_template': PYCONF,
        'json_url': '',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('run local', LOG)
    def run(self, args, variables):
        self.__text = """This command is deprecated and will be replaced with
        a newer version soon."""
        return False
        output_file = None
        if 'output_file' in variables:
            output_file = os.path.join(RESULTDIR, variables['output_file'])
            if not output_file.endswith('.root'):
                output_file += '.root'
        else:
            output_file = OUTPUT_FILE.format(ds=variables['dataset'])
        variables['output_file'] = output_file

        self.__prepare(args, variables)
        campaign = self.__variables['campaign']
        chosen_dataset = self.__variables['dataset']
        input_files = find_input_files(
            campaign, chosen_dataset, self.__variables, logger=LOG
        )
        LOG.debug(
            "Using files for NTP input:\n{0}".format('\n'.join(input_files)))

        self.__output_file = self.__variables['output_file']

        self.__write_pset(input_files)

        # making sure the correct HLT menu is read
        if 'reHLT' in input_files[0]:
            self.__variables['isReHLT'] = 1

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

        if self.__variables['json_url'] != '':
            if not 'https://cms-service-dqm.web.cern.ch' in self.__variables['json_url']:
                local_json = 'file:{0}/{1}/{2}'.format( CMSSW_SRC, 'BristolAnalysis/NTupleTools', self.__variables['json_url']) 
                LOG.debug('Local json :{0}'.format(local_json) )
                self.__variables['json_url']= local_json


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
