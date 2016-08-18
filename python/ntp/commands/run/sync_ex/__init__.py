"""
    run sync_ex:
        Runs the synchronisation exercise on a given data set.
        Only the first 10,000 events of the first file will be
        read.
        
        
    Usage:
            run sync_ex [campaign=<X>]  [dataset=<X>] [output_file=<X>]
        
    Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in crab/*
                      Default is 'Spring16'.
            dataset:  Alias for the single dataset you want to run over. Corresponds
                      to the file names (without extension) in crab/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is 'TTJets_PowhegPythia8'.
            files:    Instead of running on a specific dataset, run over the
                      given (comma-separated) list of files
            output_file: Name of the output file. Default: sync_exercise.root
"""
import logging
import os
from .. import Command as C
from hepshell.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import RESULTDIR
from crab.util import find_input_files

LOG = logging.getLogger(__name__)
OUTPUT_FILE = os.path.join(RESULTDIR, 'sync_exercise.root')

BASE = """
import FWCore.ParameterSet.Config as cms
from run.miniAODToNTuple_cfg import process

process.maxEvents.input = cms.untracked.int32({nevents})

process.TFileService.fileName=cms.string('{OUTPUT_FILE}')

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
"""


class Command(C):
    DEFAULTS = {
        'campaign': 'Spring16',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 10000,
        'files': '',
        'output_file': OUTPUT_FILE,
        'pset_template': BASE,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('run sync_ex', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        campaign = self.__variables['campaign']
        chosen_dataset = self.__variables['dataset']
        input_files = self.__variables['files']
        if not input_files:
            input_files = find_input_files(
                campaign, chosen_dataset, self.__variables, logger=LOG
            )
            input_files = str(input_files[0])
        # take only first file
        self.__variables['files'] = input_files
        self.__variables['isTTbarMC'] = 1

        from ..local import Command as LocalC
        run_local = LocalC()
        rc = run_local.run(args, self.__variables)
        self.__text = run_local.get_text()

        return rc
