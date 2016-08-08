"""
    run condor: Runs the n-tuple production on the a condor batch system.
                All run commands require a valid grid certificate as they
                either read data from the grid via XRootD or run on grid
                resources.
                The command will use python/run/miniAODToNTuple_cfg.py.
                All unknown parameters will be bassed to 'ntp run local'
                inside the condor job.
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
import getpass
import logging
import glob

from .. import Command as C
from crab.util import get_files
from ntp import NTPROOT
from ntp.commands.setup import WORKSPACE, LOGDIR, CACHEDIR, RESULTDIR

LOG = logging.getLogger(__name__)

try:
    import htcondenser as htc
except:
    LOG.error('Could not import htcondenser')


CONDOR_ROOT = os.path.join(WORKSPACE, 'condor')
HDFS_STORE_BASE = "/hdfs/TopQuarkGroup/{user}".format(
    user=getpass.getuser())

RETRY_COUNT = 10

SETUP_SCRIPT = """
tar -xf ntp.tar.gz
source bin/env.sh
ntp setup from_tarball=cmssw_src.tar.gz

"""

RUN_SCRIPT = """
ntp run local $@ nevents=-1

"""

MERGE_SETUP_SCRIPT = """
tar -xf ntp.tar.gz
source bin/env.sh
ntp setup from_tarball=cmssw_src.tar.gz compile=0

"""

MERGE_SCRIPT = """
ntp merge $@

"""

LOG_STEM = 'ntp_job.$(cluster).$(process)'

# file splitting for datasets containing 'key'
SPLITTING_BY_FILE = {
    'SingleElectron': 3,
    'SingleMuon': 3,
    'TTJet': 5,
    'TT_': 5,
    'DEFAULT': 10,
}


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
        self.__input_files = []
        self.__outdirs = []

    def run(self, args, variables):
        self.__prepare(args, variables)

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
            msg += 'DAGstatus {0}/diamond.status -s'.format(self.__outdirs[0])
        else:
            msg += 'DAGstatus workspace/condor/*/diamond.status -s'
        LOG.info(msg)
        # ntp condor status

        return True

    def __run_dataset(self, campaign, dataset):
        self.__set_job_dirs(campaign, dataset)

        self.__create_folders()

        # which dataset, file, etc
        self.__get_run_config(campaign, dataset)
        self.__write_files()
        # create DAG for condor
        self.__create_dag()

        if not self.__variables['noop']:
            self.__dag.submit(force=True)
            self.__text += "\n Submitted {0} jobs".format(len(self.__dag))
#             for job in self.__dag:
#                 print(job.name, 'running:', job.manager.exe, ' '.join(job.args))

    def __set_job_dirs(self, campaign, dataset):
        out_dir = os.path.join(CONDOR_ROOT, campaign, dataset)

        existing_dirs = glob.glob(out_dir + '_*')
        latest = 1
        if existing_dirs:
            latest = self.__find_highest_numbering(existing_dirs)
            latest += 1
        out_dir += '_{0}'.format(latest)

        self.__job_dir = out_dir
        self.__outdirs.append(out_dir)
        self.__job_log_dir = os.path.join(self.__job_dir, 'log')
        self.__setup_script = os.path.join(self.__job_dir, 'setup.sh')
        self.__run_script = os.path.join(self.__job_dir, 'run.sh')
        self.__merge_setup_script = os.path.join(
            self.__job_dir, 'merge_setup.sh')
        self.__merge_script = os.path.join(self.__job_dir, 'merge.sh')
        self.__run_config = os.path.join(self.__job_dir, 'config.json')

    def __find_highest_numbering(self, folders):
        numbers = []
        for f in folders:
            number = int(f.split('_')[-1])
            numbers.append(number)
        return max(numbers)

    def __create_folders(self):
        dirs = [CONDOR_ROOT, self.__job_dir, self.__job_log_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)

    def __create_tar_file(self, args, variables):
        from ntp.commands.create.tarball import Command as TarCommand
        c = TarCommand()
        c.run(args, variables)
        self.__text += c.__text
        self.__input_files.extend(c.get_tar_files())

    def __get_run_config(self, campaign, dataset):
        from crab.util import find_input_files
        from crab import get_config
        run_config = {
            'requestName': 'Test',
            'outputDatasetTag': 'Test',
            'inputDataset': 'Test',
            'splitting': 'FileBased',
            'unitsPerJob': 1,
            'outLFNDirBase': os.path.join(HDFS_STORE_BASE, 'ntuple'),
            'lumiMask': '',
            'pyCfgParams': None,
            'files': [],
        }

        using_local_files = self.__variables['files'] != ''
        input_files = find_input_files(
            campaign, dataset, self.__variables, LOG)

        if not using_local_files:
            run_config = get_config(campaign, dataset)
            run_config['outLFNDirBase'] = self.__replace_output_dir(run_config)

        run_config['files'] = input_files
        parameters = self.__extract_params()
        if run_config['pyCfgParams']:
            params = '{parameters} {cfg_params}'.format(
                parameters=parameters,
                cfg_params=' '.join(run_config['pyCfgParams']),
            )
            run_config['pyCfgParams'] = params
        else:
            run_config['pyCfgParams'] = parameters

        LOG.info('Retrieved CRAB config')

        self.__config = run_config

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
        with open(self.__setup_script, 'w+') as f:
            f.write(SETUP_SCRIPT)

        with open(self.__run_script, 'w+') as f:
            f.write(RUN_SCRIPT)

        with open(self.__merge_script, 'w+') as f:
            f.write(MERGE_SCRIPT)

        with open(self.__merge_setup_script, 'w+') as f:
            f.write(MERGE_SETUP_SCRIPT)

        import json
        with open(self.__run_config, 'w+') as f:
            f.write(json.dumps(self.__config, indent=4))

    def __create_dag(self):
        """ Creates a Directional Acyclic Grag (DAG) for condor """
        dag_man = htc.DAGMan(
            filename=os.path.join(self.__job_dir, 'diamond.dag'),
            status_file=os.path.join(self.__job_dir, 'diamond.status'),
            dot='diamond.dot'
        )

        layer_1_jobs = self.__create_layer1()
        for job in layer_1_jobs:
            dag_man.add_job(job, retry=RETRY_COUNT)

        layer_2_jobs = self.__create_layer2(layer_1_jobs)
        for job in layer_2_jobs:
            dag_man.add_job(job, requires=layer_1_jobs, retry=2)

        self.__dag = dag_man

    def __create_layer1(self):
        jobs = []

        run_config = self.__config
        input_files = run_config['files']
        if self.__variables['test']:
            input_files = [input_files[0]]

        job_set = htc.JobSet(
            exe=self.__run_script,
            copy_exe=True,
            setup_script=self.__setup_script,
            filename=os.path.join(
                self.__job_dir, 'ntuple_production.condor'),
            out_dir=self.__job_log_dir,
            out_file=LOG_STEM + '.out',
            err_dir=self.__job_log_dir,
            err_file=LOG_STEM + '.err',
            log_dir=self.__job_log_dir,
            log_file=LOG_STEM + '.log',
            share_exe_setup=True,
            common_input_files=self.__input_files,
            transfer_hdfs_input=False,
            hdfs_store=run_config['outLFNDirBase'] + '/tmp',
            certificate=self.REQUIRE_GRID_CERT,
            cpus=1,
            memory='1500MB'
        )
        parameters = 'files={files} output_file={output_file} {params}'
        n_files_per_group = SPLITTING_BY_FILE['DEFAULT']
        for name, value in SPLITTING_BY_FILE.items():
            if name in run_config['inputDataset']:
                n_files_per_group = value

        grouped_files = self.__group_files(
            input_files, n_files_per_group)
        for i, f in enumerate(grouped_files):
            output_file = 'ntuple_{0}.root'.format(i)
            args = parameters.format(
                files=','.join(f),
                output_file=output_file,
                params=run_config['pyCfgParams']
            )
            rel_out_dir = os.path.relpath(RESULTDIR, NTPROOT)
            rel_log_dir = os.path.relpath(LOGDIR, NTPROOT)
            rel_out_file = os.path.join(rel_out_dir, output_file)
            rel_log_file = os.path.join(rel_log_dir, 'ntp.log')
            job = htc.Job(
                name='job_{0}'.format(i),
                args=args,
                output_files=[rel_out_file, rel_log_file])
            job_set.add_job(job)
            jobs.append(job)
        return jobs

    def __create_layer2(self, layer1_jobs):
        run_config = self.__config

        job_set = htc.JobSet(
            exe=self.__merge_script,
            copy_exe=True,
            setup_script=self.__merge_setup_script,
            filename=os.path.join(
                self.__job_dir, 'ntuple_merge.condor'),
            out_dir=self.__job_log_dir,
            out_file=LOG_STEM + '.out',
            err_dir=self.__job_log_dir,
            err_file=LOG_STEM + '.err',
            log_dir=self.__job_log_dir,
            log_file=LOG_STEM + '.log',
            share_exe_setup=True,
            common_input_files=self.__input_files,
            transfer_hdfs_input=False,
            hdfs_store=run_config['outLFNDirBase'],
            certificate=self.REQUIRE_GRID_CERT,
            cpus=1,
            memory='1500MB'
        )

        parameters = '{files} output_file={output_file}'
        output_file = '{0}.root'.format(run_config['outputDatasetTag'])

        all_output_files = [
            f for job in layer1_jobs for f in job.output_file_mirrors]
        root_output_files = [
            f.hdfs for f in all_output_files if f.hdfs.endswith('.root')]

        args = parameters.format(
            files=' '.join(root_output_files),
            output_file=output_file,
        )
        rel_log_dir = os.path.relpath(LOGDIR, NTPROOT)
        rel_log_file = os.path.join(rel_log_dir, 'ntp.log')
        job = htc.Job(
            name='merge',
            args=args,
            output_files=[output_file, rel_log_file])
        job_set.add_job(job)

        return [job]

    def __group_files(self, input_files, n_files_per_group):
        N = n_files_per_group
        grouped_files = [input_files[n:n + N]
                         for n in range(0, len(input_files), N)]
        return grouped_files
