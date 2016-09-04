"""
    run condor: Runs 'ntp run condor ntuple', 'ntp run condor analysis' and
                'ntp run condor merge' as a Directed Acyclic Graph workflow.
        Usage:
            run condor [campaign=<X>]  [dataset=<X>] [file=<path>]

        Parameters:
            campaign: which campaign to run. Corresponds to the folder
                      structure in crab/*
                      Default is 'Spring16'.
            dataset:  Alias for the single dataset you want to run over. Corresponds
                      to the file names (without extension) in crab/*/*.py.
                      Accepts wild-cards and comma-separated lists.
                      Default is 'TTJets_PowhegPythia8'.
                      Special value 'all' will submit all datasets for a given
                      campaign.
                      This parameter is ignored if parameter file is given.
            files:    Instead of running on a specific dataset, run over the
                      given (comma-separated) list of files
            noop:     'NO OPeration', will do everything except submitting jobs.
                      Default: false
            nevents:  Number of events to process.
                      Default is all (-1).
            test:     Run just one job for testing. Default: false.
"""
from __future__ import print_function
import os
import logging
import glob

from .. import Command as C
from crab.util import get_files
from ntp import NTPROOT
from ntp.commands.setup import WORKSPACE, LOGDIR, CACHEDIR, RESULTDIR
from ntp.utils import find_latest_iteration
from ntp.utils.hdfs import HDFS_STORE_BASE


LOG = logging.getLogger(__name__)

try:
    import htcondenser as htc
except:
    LOG.error('Could not import htcondenser')

CONDOR_ROOT = os.path.join(WORKSPACE, 'condor')
LOG_STEM = 'ntp_job.$(cluster).$(process)'

class Command(C):

    DEFAULTS = {
        'campaign': 'Spring16',
        'dataset': 'TTJets_PowhegPythia8',
        'files': '',
        'noop': False,
        'nevents': -1,
        'test': False,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        # used by sub-commands
        self.__input_files = []
        self.__outdirs = []
        self.__output_files = []
        self.__root_output_files = []
        self.__job_log_dir = ''
        self.__job_dir = ''
        self.__config = {}

    def run(self, args, variables):
        # sub commands
        from .ntuple import Command as NTupleCommand
        from ..analysis.DICE import Command as AnalysisCommand
        from .merge import Command as MergeCommand
        self.__ntuple = NTupleCommand()
        self.__analysis = AnalysisCommand()
        self.__merge = MergeCommand()

        self.__prepare(args, variables)
        self.__ntuple.__prepare(args, variables)
        self.__analysis.__prepare(args, variables)
        self.__merge.__prepare(args, variables)

        campaign = self.__variables['campaign']
        chosen_dataset = self.__variables['dataset']

        # create tarball
        self.__create_tar_file(args, variables)

        datasets = [chosen_dataset]
        if chosen_dataset.lower() == 'all':
            from crab.datasets import create_sample_list
            samples = create_sample_list()
            if campaign in samples:
                datasets = samples[campaign]
            else:
                LOG.error(
                    'Cannot find datasets for campaign {0}'.format(campaign))
                return False

        for dataset in datasets:
            self.__run_dataset(campaign, dataset)
        # to check status:
        msg = 'To check the status you can run\n'
        if len(self.__outdirs) == 1:
            msg += 'DAGstatus {0}/*.status -s'.format(self.__outdirs[0])
        else:
            msg += 'DAGstatus workspace/condor/*/*.status -s'
        LOG.info(msg)
        # ntp condor status

        return True

    def __run_dataset(self, campaign, dataset):
        self.set_job_dirs(campaign, dataset)

        self.__create_folders()

        # which dataset, file, etc
        self.__set_run_config(campaign, dataset)

        # create DAG for condor
        self.__create_dag()

        if not self.__variables['noop']:
            self.__dag.submit(force=True)
            self.__text += "\n Submitted {0} jobs".format(len(self.__dag))
#             for job in self.__dag:
#                 print(job.name, 'running:', job.manager.exe, ' '.join(job.args))

    def set_job_dirs(self, campaign, dataset):
        out_dir = os.path.join(CONDOR_ROOT, campaign, dataset, 'workflow')
        out_dir = self.__get_latest_outdir(out_dir)

        self.__job_dir = out_dir
        self.__job_log_dir = os.path.join(self.__job_dir, 'log')

        self.__ntuple.set_job_dir(out_dir)
        self.__analysis.set_job_dir(out_dir)
        self.__merge.set_job_dir(out_dir)

    def __create_folders(self):
        dirs = [CONDOR_ROOT, self.__job_dir, self.__job_log_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)

    def __create_tar_file(self, args, variables):
        from ntp.commands.create.tarball import Command as TarCommand
        if self.__variables['noop'] and TarCommand.tarballs_exist():
            return
        c = TarCommand()
        c.run(args, variables)
        self.__text += c.__text
        self.__input_files.extend(c.get_tar_files())

    def __set_run_config(self, campaign, dataset):
        from copy import deepcopy
        self.__config = self.__get_crab_config(campaign, dataset)
        self.__ntuple.__config = deepcopy(self.__config)
        self.__analysis.__config = deepcopy(self.__config)
        
        output_dir = self.__config['outLFNDirBase']
        self.__analysis.__config['outputDir'] = output_dir.replace(
            'ntuple', 'atOutput'
        )
        self.__merge.__config = deepcopy(self.__config)

    def __get_crab_config(self, campaign, dataset):
        from crab.util import find_input_files
        from crab import get_config
        from crab.base import __version__ as ntuple_version
        config = {
            'requestName': 'Test',
            'outputDatasetTag': 'Test',
            'inputDataset': 'Test',
            'splitting': 'FileBased',
            'unitsPerJob': 1,
            'outLFNDirBase': os.path.join(HDFS_STORE_BASE, 'ntuple'),
            'lumiMask': '',
            'pyCfgParams': [],
            'files': [],
            'ntuple_version': ntuple_version,
        }

        using_local_files = self.__variables['files'] != ''
        input_files = find_input_files(
            campaign, dataset, self.__variables, LOG)

        if not using_local_files:
            config = get_config(campaign, dataset)
            config['outLFNDirBase'] = self.__replace_output_dir(config)

        config['files'] = input_files
        parameters = self.__extract_params()
        if config['pyCfgParams']:
            params = '{parameters} {cfg_params}'.format(
                parameters=parameters,
                cfg_params=' '.join(config['pyCfgParams']),
            )
            config['pyCfgParams'] = params
        else:
            config['pyCfgParams'] = parameters

        LOG.info('Retrieved CRAB config')

        return config

    def __replace_output_dir(self, run_config):
        output = run_config['outLFNDirBase']
        LOG.debug('Replacing output directory {0}'.format(output))
        if output.startswith('/store/user'):
            tokens = output.split('/')
            base = '/'.join(tokens[4:])
            LOG.debug('Taking base of {0}'.format(base))
            LOG.debug('and replacing with {0}'.format(HDFS_STORE_BASE))
            output = os.path.join(HDFS_STORE_BASE, base)
            output = os.path.join(output, run_config['outputDatasetTag'])
            LOG.debug('Final output directory: {0}'.format(output))
        return output

    def __write_files(self):
        self.__ntuple.write_job_files()
        self.__analysis.write_job_files()
        self.__merge.write_job_files()

    def __create_dag(self):
        """ Creates a Directional Acyclic Grag (DAG) for condor """
        from .ntuple import RETRY_COUNT as NTUPLE_RETRY_COUNT
        from .analysis import RETRY_COUNT as ANALYSIS_RETRY_COUNT
        from .merge import RETRY_COUNT as MERGE_RETRY_COUNT
        dag_man = htc.DAGMan(
            filename=os.path.join(self.__job_dir, 'diamond.dag'),
            status_file=os.path.join(self.__job_dir, 'diamond.status'),
            dot='diamond.dot'
        )

        # layer 1 - ntuples
        ntuple_jobs = self.__ntuple.create_job_layer(self.__config['files'])
        for job in ntuple_jobs:
            dag_man.add_job(job, retry=NTUPLE_RETRY_COUNT)

        ntuple_output_files = self.__ntuple.get_root_output_files()

        # layer 2 - analysis
        from .analysis import ANALYSIS_MODES
        self.__analysis.__config['files'] = ntuple_output_files
        for mode in ANALYSIS_MODES:
            analysis_jobs = self.__analysis.create_job_layer(
                ntuple_output_files, mode)
            for job in analysis_jobs:
                dag_man.add_job(
                    job, requires=ntuple_jobs, retry=ANALYSIS_RETRY_COUNT)

            analysis_output_files = self.__analysis.get_root_output_files()
            # layer 2b
            # for each analysis mode create 1 merged file
            merge_jobs = self.__merge.create_job_layer(
                input_files=analysis_output_files,
                mode=mode
            )
            for job in merge_jobs:
                dag_man.add_job(
                    job, requires=analysis_jobs, retry=MERGE_RETRY_COUNT)

        self.__dag = dag_man
        
        self.__write_files()

    def get_root_output_files(self):
        return self.__root_output_files

    def __get_latest_outdir(self, out_dir):
        existing_dirs = glob.glob(out_dir + '_*')
        latest = 1
        if existing_dirs:
            latest = find_latest_iteration(existing_dirs)
            latest += 1
        out_dir += '_{0}'.format(latest)
        return out_dir
