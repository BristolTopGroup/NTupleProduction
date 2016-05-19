"""
    run local:  Runs the n-tuple production on the current machine.
                All run commands require a valid grid certificate as they
                either read data from the grid via XRootD or run on grid
                resources.
                The command will use python/run/miniAODToNTuple_cfg.py.
        Usage:
            run local [campaign=<X>]  [dataset=<X>] [file=<path>] [nevents=<N>]

        Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in crab/*
                      Default is 'Test'.
            dataset:  Alias for the single dataset you want to run over. Corresponds
                      to the file names (without extension) in crab/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is 'TTJets_PowhegPythia8'.
                      This parameter is ignored if parameter file is given.
            file:     Instead of running on a specific dataset, just run over the given file
            nevents:  Number of events to process.
                      Default is 1000.
"""
from __future__ import print_function
import os
import logging

from .. import Command as C
from ntp.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC, TMPDIR, RESULTDIR
from crab.util import get_files

BASE = """
import FWCore.ParameterSet.Config as cms
from run.miniAODToNTuple_cfg import process

process.maxEvents.input = cms.untracked.int32({nevents})

process.TFileService.fileName=cms.string('{output_file}')

process.source.fileNames = cms.untracked.vstring(
'{input_file}',
)

process.nTuplePFJets.btagCalibrationFile = cms.string('{btag_calib_file}')
"""

LOG = logging.getLogger(__name__)


class Command(C):

    DEFAULTS = {
        'campaign': 'Test',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 1000,
        'file': '',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('run local', LOG)
    def run(self, args, variables):
        from ntp.interpreter import call
        import resource
        self.__prepare(args, variables)

        tmp_folder = TMPDIR
        pset = tmp_folder + '/pset.py'
        workspace = CMSSW_SRC
        output_file = RESULTDIR + '/ntuple.root'

        nevents = int(self.__variables['nevents'])
        dataset = self.__variables['dataset']
        campaign = self.__variables['campaign']
        input_file = self.__variables['file']
        btag_calib_file = NTPROOT + '/data/BTagSF/CSVv2.csv'

        if input_file == '':
            LOG.info(
                "Searching for a file of {0}/{1}".format(campaign, dataset))
            files = get_files(campaign, dataset)
            input_file = files[0]
        if not input_file.startswith('/store') and not 'file://' in input_file:
            if os.path.exists(input_file):
                input_file = 'file://' + os.path.abspath(input_file)
            else:
                LOG.error('Could not find file "{0}"!'.format(input_file))
                return False
        LOG.info("Using file {0} for NTP input".format(input_file))

        with open(pset, 'w+') as f:
            content = BASE.format(
                nevents=nevents,
                input_file=input_file,
                output_file=output_file,
                btag_calib_file=btag_calib_file)
            f.write(content)

        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'cmsRun {pset} {params}',
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC, pset=pset, params=self.__extract_params())

        LOG.info("Executing cmsRun")
        call([all_in_one], LOG, stdout_log_level=logging.INFO, shell=True)

        self.__text = "Ran {pset}\n"
        self.__text = "Created ntuples: {output_file}\n"
        self.__text += "Logging information can be found in {LOGDIR}/ntp.log"
        self.__text = self.__text.format(
            pset=pset, LOGDIR=LOGDIR, output_file=output_file)

        return True

    def __run_cmssw(self, workspace):
        pass
