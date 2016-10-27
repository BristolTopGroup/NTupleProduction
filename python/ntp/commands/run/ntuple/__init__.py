"""
    run ntuple: Runs the n-tuple production on the current machine.
                All run commands require a valid grid certificate as they
                either read data from the grid via XRootD or run on grid
                resources.
                This workflow uses a config file template which can be found here:
                {TEMPLATE}

        Usage:
            run local [campaign=<X>]  [dataset=<X>] [files=file1,file2,..]
                      [nevents=<N>] [noop=false] [output_file=<file name>]

        Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in {CRAB_PATH}/*
                      Default is 'Test'.
            dataset:  Alias for the single dataset you want to run over. Corresponds
                      to the file names (without extension) in
                      {CRAB_PATH}/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is 'TTJets_PowhegPythia8'.
                      This parameter is ignored if the parameter 'files' is given.
            files:    Instead of running on a specific dataset, run over the
                      given (comma-separated) list of files
            nevents:  Number of events to process.
                      Default is 1000.
            noop:     'NO OPeration', will not run CMSSW. Default: false
            output_file_suffix:
                  Suffix used for the output file. Default: ntuple
                  The resulting output file will be
                  <dataset>_<campaign>_<output_file_suffix>.root
            json_url: Data-only:
                      URL to JSON file, e.g. https://cms-service-dqm.web.cern.ch/../..._JSON.txt
                      or (local file) file://<path>. Default: ''
            where:    Where to run the analysis. Can be 'local|DICE'.
                  Default is 'local'.
            test:     Run just one job for testing (DICE only). Default: false.
"""
from __future__ import print_function
import os
import logging

import ntp
from hepshell.interpreter import time_function
from ntp import NTPROOT
from ntp.commands.setup import CMSSW_SRC, TMPDIR, RESULTDIR, LOGDIR
from ntp.commands.run import Command as ParentCommand
from crab.util import find_input_files
from .template import PYCONF

LOG = logging.getLogger(__name__)
PSET = os.path.join(TMPDIR, 'pset.py')
OUTPUT_FILE = os.path.join(RESULTDIR, '{ds}_ntuple.root')
BTAG_CALIB_FILE = os.path.join(NTPROOT, 'data/BTagSF/CSVv2.csv')


def get_datasets(campaign):
    from crab.datasets import create_sample_list
    datasets = []

    samples = create_sample_list()
    if campaign in samples:
        datasets = samples[campaign]
    else:
        LOG.error(
            'Cannot find datasets for campaign {0}'.format(campaign))
        return False
    return datasets


class Command(ParentCommand):

    DEFAULTS = {
        'campaign': 'Test',
        'dataset': 'TTJets_PowhegPythia8',
        'nevents': 1000,
        'files': '',
        'noop': False,
        'output_file_suffix': 'ntuple',
        'pset_template': PYCONF,
        'json_url': '',
        'where': 'local',
        'input_files': [],
        'test': False,
        'output_file': '',
    }

    def __init__(self, path=__file__, doc=__doc__):
        CRAB_PATH = os.path.join(NTPROOT, 'python', 'crab')
        doc = doc.format(
            TEMPLATE=path.replace('__init__', 'template'),
            CRAB_PATH=CRAB_PATH,
        )
        super(Command, self).__init__(path, doc)

    @time_function('run ntuple', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)

        campaign = self.__variables['campaign']
        dataset = self.__variables['dataset']
        datasets = get_datasets(
            campaign).keys() if dataset == 'all' else [dataset]

        results = []
        for dataset in datasets:
            results.append(self.__run(campaign, dataset))
        return all(results)

    def __run(self, campaign, dataset):
        self.__variables['dataset'] = dataset
        self.__variables['campaign'] = campaign
        suffix = self.__variables['output_file_suffix']
        self.__add_output_file(dataset, campaign, suffix)
        self.__add_input_files()
        self.__set_automatic_parameters()

        if self.__can_run():
            return self.__run_payload()
        else:
            return False

    def __add_output_file(self, dataset, campaign, suffix):
        output_file = '_'.join([dataset, campaign, suffix])
        output_file = os.path.join(RESULTDIR, output_file)
        if not output_file.endswith('.root'):
            output_file += '.root'
        self.__variables['output_file'] = output_file

    def __add_input_files(self):
        input_files = []
        path = self.__variables['files']
        dataset = self.__variables['dataset']
        campaign = self.__variables['campaign']
        if path != '':
            input_files = ParentCommand.input_files_from_path(path)
            # dress them for CMSSW (unless they have a global path)
            input_files = ['file://{0}'.format(f) if not f.startswith('/store') else f for f in input_files]
        else:
            input_files = find_input_files(
                campaign, dataset, self.__variables, LOG
            )
        self.__variables['input_files'] = input_files

    def __run_payload(self):
        # TODO: add checking/dynamic subcommand discovery
        if self.__variables['where'] == 'local':
            from .local import Command as PayLoad
        else:
            from .DICE import Command as PayLoad

        payload = PayLoad()
        return payload.run(self.__args, self.__variables)
