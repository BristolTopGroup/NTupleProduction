"""
    run analysis:
        Runs the ntuple based analysis code (AnalysisSoftware) to produce the
        final set of trees.
        This workflow uses a config file template which can be found here:
        {TEMPLATE}
        
    Usage:
        run analysis dataset=<data set> [files=<f1,f2,..>]
                    [nevents={nevents_default}] [noop=0] [output_file=atOutput.root]
        
    Parameters:
        dataset:  Alias for the single dataset you want to run over. Corresponds
                  to keys of 'datasets_13TeV' dictionary in
                  {ANALYSIS_INFO_FILE}.
                  Accepts a valid key or 'all'.
                  Default is 'TTJets_PowhegPythia8'.
                  This parameter is ignored if parameter file is given.
        files:    Instead of running on a specific dataset, run over the
                  given (comma-separated) list of files
        nevents:  Number of events to process.
                  Default is {nevents_default}.
        noop:     'NO OPeration', will not run AnalysisSoftware. Default: false
        output_file_suffix:
                  Suffix used for the output file. Default: atOutput
                  The resulting output file will be
                  <dataset>_<output_file_suffix>.root
        mode:     The analysis mode: {modes}
        where:    Where to run the analysis. Can be 'local|DICE'.
                  Default is 'local'.
        test:     Run just one job for testing (DICE only). Default: false.
"""
from __future__ import print_function
import os
import logging
import glob
import shutil

from ntp.commands.run import Command as ParentCommand
from hepshell.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC, TMPDIR, RESULTDIR, LOGDIR

from crab.util import find_input_files
from .template import PYCONF

BAT_BASE = os.path.join(CMSSW_SRC, 'BristolAnalysis', 'Tools')
BAT_PYTHON = os.path.join(BAT_BASE, 'python')
ANALYSIS_INFO_FILE = os.path.join(BAT_PYTHON, 'analysis_info_2016.py')
LOG = logging.getLogger(__name__)

ANALYSIS_MODES = [
    'central',
    'JES_down',
    'JES_up',
    'JetSmearing_down',
    'JetSmearing_up',
]

class Command(ParentCommand):
    #     """
    #         This command is used for input file discovery & steering of anlysis
    #         jobs. Once all arguments and parameters are passed this commands calls
    #         one of its sub-commands, local or DICE, to execute the job in the
    #         correct environment.
    #     """

    DEFAULTS = {
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 10000,
        'files': '',
        'noop': False,
        'output_file_suffix': 'atOutput',
        'pset_template': PYCONF,
        'mode': 'central',
        'where': 'local',
        'input_files': [],
        'output_file': '',
        'test': False,
    }

    REQUIRE_GRID_CERT = False

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(
            modes='|'.join(ANALYSIS_MODES),
            ANALYSIS_INFO_FILE=ANALYSIS_INFO_FILE,
            TEMPLATE=path.replace('__init__', 'template'),
            nevents_default=self.DEFAULTS['nevents'],
        )
        super(Command, self).__init__(path, doc)

    @time_function('run local', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        dataset = self.__variables['dataset']
        mode = self.__variables['mode']
        modes = ANALYSIS_MODES if mode == 'all' else [mode]
        datasets = get_datasets().keys() if dataset == 'all' else [dataset]

        results = []
        for dataset in datasets:
            for mode in modes:
                # Don't do Jet Smearing or Jet Scale for data
                if ('SingleMuon' in dataset or 'SingleElectron' in dataset ) and 'central' not in mode: continue
                results.append(self.__run(dataset, mode))
        return all(results)

    def __run(self, dataset, mode):
        self.__variables['dataset'] = dataset
        self.__variables['mode'] = mode
        suffix = self.__variables['output_file_suffix']
        self.__add_output_file(dataset, mode, suffix)
        self.__add_input_files()
        self.__set_automatic_parameters()

        if self.__can_run():
            return self.__run_payload()
        else:
            return False

    def __add_output_file(self, dataset, mode, suffix):
        output_file = '_'.join([dataset, mode, suffix])
        output_file = os.path.join(RESULTDIR, output_file)
        if not output_file.endswith('.root'):
            output_file += '.root'
        self.__variables['output_file'] = output_file

    def __add_input_files(self):
        input_files = []
        path = self.__variables['files']
        dataset = self.__variables['dataset']
        if path != '':
            input_files = ParentCommand.input_files_from_path(path)
        else:
            input_files = self.__input_files_from_dataset(dataset)
        self.__variables['input_files'] = input_files

    def __run_payload(self):
        # TODO: add checking/dynamic subcommand discovery
        if self.__variables['where'] == 'local':
            from .local import Command as PayLoad
        else:
            from .DICE import Command as PayLoad

        payload = PayLoad()
        return payload.run(self.__args, self.__variables)

    def __can_run(self):
        isData = self.__variables['isData']
        mode = self.__variables['mode']
        bad = mode != 'central' and isData
        if bad:
            LOG.debug('Mode {0} is only supported for simulation'.format(mode))
        return not bad

    def __get_datasets(self):
        from imp import load_source
        analysis_info = load_source('analysis_info', ANALYSIS_INFO_FILE)
        return analysis_info.datasets_13TeV

    def __input_files_from_dataset(self, dataset):
        datasets = self.__get_datasets()
        if not dataset in datasets:
            msg = 'Cannot find dataset {0}'.format(dataset)
            LOG.error(msg)
            import sys
            sys.exit(msg)

        path = [os.path.join(p, '*/*.root') for p in datasets[dataset]]
        return ParentCommand.input_files_from_path(path)

