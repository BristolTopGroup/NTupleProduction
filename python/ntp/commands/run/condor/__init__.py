"""
    run condor: Runs the n-tuple production on the a condor batch syste,.
                All run commands require a valid grid certificate as they
                either read data from the grid via XRootD or run on grid
                resources.
                The command will use python/run/miniAODToNTuple_cfg.py.
        Usage:
            run condor [campaign=<X>]  [dataset=<X>] [file=<path>] [nevents=<N>]

        Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in crab/*
                      Default is 'Spring16'.
            dataset:  Alias for the single dataset you want to run over. Corresponds
                      to the file names (without extension) in crab/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is 'TTJets_PowhegPythia8'.
                      This parameter is ignored if parameter file is given.
            file:     Instead of running on a specific dataset, just run over the given file
            nevents:  Number of events to process.
                      Default is -1.
"""
from __future__ import print_function
import logging

from .. import Command as C
from ntp.commands.setup import get_cmssw_workspace
from crab.util import get_files

from ntp import NTPROOT

CACHE = NTPROOT + '/workspace/cache'

BASE = """
import FWCore.ParameterSet.Config as cms
from run.miniAODToNTuple_cfg import process

process.maxEvents.input = cms.untracked.int32({nevents})

process.TFileService.fileName=cms.string('{output_file}')

process.source.fileNames = cms.untracked.vstring(
{input_files}
)

process.nTuplePFJets.btagCalibrationFile = cms.string('{btag_calib_file}')
"""

from ntp import NTPROOT
LOG_DIR = NTPROOT + '/workspace/log/condor'
HDFS_OUTPUT_DIR = '/hdfs/user/{user}/ntuples/'


class Command(C):

    DEFAULTS = {
        'campaign': 'Spring16',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': -1,
        'file': '',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        import htcondenser as ht
        from ntp.commands.create.tarball import Command as TarCommand
        self.__prepare(args, variables)

        # create tarball
        tar = TarCommand()
        result = tar.run(args=[], variables={})
        self.__text = tar.__text
        # create DAG for condor
        # to check status:
        # ntp condor status
        self.__text += "\n Rest is NOT IMPLEMENTED (yet) - but would be running condor"

        return result

    def create_tar_file(self):
        pass
