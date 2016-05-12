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
from .. import Command as C
from ntp.commands.setup import get_cmssw_workspace
from crab.util import get_files

BASE = """
import FWCore.ParameterSet.Config as cms
from run.miniAODToNTuple_cfg import process

process.maxEvents.input = cms.untracked.int32({nevents})

process.TFileService.fileName=cms.string('{output_file}')

process.source.fileNames = cms.untracked.vstring(
'{input_file}',
)
"""


class Command(C):

    DEFAULTS = {
        'campaign': 'Test',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 1000,
        'file': '',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        import subprocess
        self.__prepare(args, variables)

        NTPROOT = os.environ['NTPROOT']
        tmp_folder = NTPROOT + '/workspace/tmp'
        pset = tmp_folder + '/pset.py'
        workspace = get_cmssw_workspace()
        output_file = NTPROOT + '/workspace/results/ntuple.root'

        nevents = self.__variables['nevents']
        dataset = self.__variables['dataset']
        campaign = self.__variables['campaign']
        input_file = self.__variables['file']

        if input_file == '':
            print("Searching for a file of {0}/{1}".format(campaign, dataset))
            files = get_files(campaign, dataset)
            input_file = files[0]
        print("Using file {0} for NTP input".format(input_file))

        with open(pset, 'w+') as f:
            content = BASE.format(
                nevents=nevents, input_file=input_file, output_file=output_file)
            f.write(content)

        commands = [
            'cd {workspace}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'cmsRun {pset} {params}',
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            workspace=workspace, pset=pset, params=self.__extract_params())

        log_file = NTPROOT + '/workspace/log/local.log'
        error_file = NTPROOT + '/workspace/log/local.err'
        with open(log_file, 'a+') as f:
            with open(error_file, 'a+') as e:
                print("executing cmsRun")
                subprocess.call(all_in_one, shell=True, stdout=f, stderr=e)

        self.__text = "Ran {pset}\n"
        self.__text += "Logs can be found in {workspace}/log/local.*"
        self.__text = self.__text.format(pset=pset, workspace=workspace)

#         self.__text = "NOT IMPLEMENTED - but would be running locally"

        return True

    def __run_cmssw(self, workspace):
        pass

    def __extract_params(self):
        args = []
        for var, value in self.__variables.items():
            if var in self.DEFAULTS:
                continue
            args.append('{0}={1}'.format(var, value))
        return ' '.join(args)
