"""
    run local:  Runs the n-tuple production on the current machine.
                All run commands require a valid grid certificate as they
                either read data from the grid via XRootD or run on grid
                resources.
                The command will use python/run/miniAODToNTuple_cfg.py.
        Usage:
            run local [campaign=<X>]  [dataset=<X>] [files=file1,file2,..]
                      [nevents=<N>] [noop=false]

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
"""
from __future__ import print_function
import os
import logging

from .. import Command as C
from ntp.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC, TMPDIR, RESULTDIR, LOGDIR
from crab.util import get_files

LOG = logging.getLogger(__name__)
PSET = os.path.join(TMPDIR, 'pset.py')
OUTPUT_FILE = os.path.join(RESULTDIR, 'ntuple.root')
BTAG_CALIB_FILE = os.path.join(NTPROOT, 'data/BTagSF/CSVv2.csv')

BASE = """
import FWCore.ParameterSet.Config as cms
from run.miniAODToNTuple_cfg import process

process.maxEvents.input = cms.untracked.int32({nevents})

process.TFileService.fileName=cms.string('{OUTPUT_FILE}')

process.source.fileNames = cms.untracked.vstring(
{input_files}
)

process.nTuplePFJets.btagCalibrationFile = cms.string('{BTAG_CALIB_FILE}')
"""


class Command(C):

    DEFAULTS = {
        'campaign': 'Test',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 1000,
        'files': '',
        'noop': False,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('run local', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        dataset = self.__variables['dataset']
        campaign = self.__variables['campaign']
        input_files = self.__variables['files'].split(',')
        LOG.debug('Chosen input files:\n{0}'.format('  \n'.join(input_files)))
        if not input_files:
            LOG.info(
                "Searching for files of {0}/{1}".format(campaign, dataset))
            files = get_files(campaign, dataset)
            input_files = files
        if not self.__check_files(input_files):
            return False
        input_files = self.__fix_paths(input_files)

        LOG.info(
            "Using files for NTP input:\n{0}".format('\n'.join(input_files)))

        self.__write_pset(input_files)

        if not self.__variables['noop']:
            self.__run_cmssw()
            self.__text = "Ran {PSET}\n"
            self.__text += "Created ntuples: {OUTPUT_FILE}\n"
            self.__text += "Logging information can be found in {LOGDIR}/ntp.log"
            self.__text = self.__text.format(
                PSET=PSET, LOGDIR=LOGDIR, OUTPUT_FILE=OUTPUT_FILE)
        else:
            LOG.info('Found "noop", not running CMSSW')

        return True

    def __write_pset(self, input_files):
        nevents = int(self.__variables['nevents'])
        input_files = self.__format_input_files(input_files)

        with open(PSET, 'w+') as f:
            content = BASE.format(
                nevents=nevents,
                input_files=input_files,
                OUTPUT_FILE=OUTPUT_FILE,
                BTAG_CALIB_FILE=BTAG_CALIB_FILE
            )
            f.write(content)

    def __format_input_files(self, input_files):
        results = []
        for f in input_files:
            results.append('"{0}"'.format(f))
        return ',\n'.join(results)

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
        from ntp.interpreter import call
        call([all_in_one], LOG, stdout_log_level=logging.INFO, shell=True)

    def __check_files(self, input_files):
        exists = []
        for f in input_files:
            if not f.startswith('/store') and not 'file://' in f:
                if not os.path.exists(f):
                    LOG.error('Could not find file "{0}"!'.format(f))
                    exists.append(False)
                    continue
            exists.append(True)
        return all(exists)

    def __fix_paths(self, input_files):
        new_paths = []
        for f in input_files:
            if not f.startswith('/store') and not 'file://' in f:
                f = 'file://' + os.path.abspath(f)
            new_paths.append(f)
        return new_paths
