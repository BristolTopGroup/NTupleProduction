"""
    run ntuple where=DICE:
        Runs the ntuple production in the Data Intensive Computing Environment.
        See 'ntp help run ntuple' for a complete list of parameters.
"""
from __future__ import print_function
import os
import logging

from . import Command as ParentCommand
from ntp import NTPROOT
from ntp.commands.setup import WORKSPACE, LOGDIR, RESULTDIR
from ntp.utils import find_latest_iteration, make_even_chunks
from ntp.utils.hdfs import HDFS_STORE_BASE

LOG = logging.getLogger(__name__)

try:
    import htcondenser as htc
except:
    LOG.error('Could not import htcondenser')


CONDOR_ROOT = os.path.join(WORKSPACE, 'condor')

RETRY_COUNT = 10

SETUP_SCRIPT = """
tar -xf ntp.tar.gz
source bin/env.sh
ntp setup from_tarball=cmssw.tar.gz

"""

RUN_SCRIPT = """
ntp run ntuple $@ nevents=-1

"""

# file splitting for datasets containing 'key'
SPLITTING_BY_FILE = {
    'SingleElectron': 3,
    'SingleMuon': 3,
    'TTJet': 3,
    'TT_': 3,
    'ST' : 3,
    'DEFAULT': 10,
}


class Command(ParentCommand):
    DEFAULTS = ParentCommand.DEFAULTS

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)

        campaign = self.__variables['campaign']
        dataset = self.__variables['dataset']

        # create tarball
        self._create_tar_file(args, variables)

        self.__run(campaign, dataset)
        # to check status:
        msg = 'To check the status you can run\n'
        if len(self.__outdirs) == 1:
            msg += 'DAGstatus {0}/*.status -s'.format(self.__outdirs[0])
        else:
            msg += 'DAGstatus workspace/condor/*/*.status -s'
        LOG.info(msg)

        return True

    def __run(self, campaign, dataset):
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

    def __set_job_dirs(self, campaign, dataset):
        import glob
        out_dir = os.path.join(CONDOR_ROOT, campaign, dataset)

        existing_dirs = glob.glob(out_dir + '_*')
        latest = 1
        if existing_dirs:
            latest = find_latest_iteration(existing_dirs)
            latest += 1
        out_dir += '_{0}'.format(latest)

        self.__job_dir = out_dir
        self.__outdirs.append(out_dir)
        self.__job_log_dir = os.path.join(self.__job_dir, 'log')
        self.__setup_script = os.path.join(self.__job_dir, 'setup.sh')
        self.__run_script = os.path.join(self.__job_dir, 'run.sh')
        self.__run_config = os.path.join(self.__job_dir, 'config.json')

    def __create_folders(self):
        dirs = [CONDOR_ROOT, self.__job_dir, self.__job_log_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)

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

        run_config['additional_input_files'] = self.__input_files

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

        # layer 1 - ntuples
        ntuple_jobs = self.__create_ntuple_layer()
        for job in ntuple_jobs:
            dag_man.add_job(job, retry=RETRY_COUNT)

        self.__dag = dag_man

    def __create_ntuple_layer(self):
        LOG_STEM = 'ntuple_job.$(cluster).$(process)'
        jobs = []

        run_config = self.__config
        input_files = run_config['files']
        if self.__variables['test']:
            input_files = [input_files[0]]

        input_files.append(self.__run_script)
        input_files.append(self.__setup_script)
        print(input_files)

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
            transfer_hdfs_input=True,
            hdfs_store=run_config['outLFNDirBase'] + '/tmp',
            certificate=self.REQUIRE_GRID_CERT,
            cpus=1,
            memory='1500MB'
        )
        parameters = 'files={files} output_file={output_file} {params}'
        if run_config['lumiMask']:
            parameters += ' json_url={0}'.format(run_config['lumiMask'])
        n_files_per_group = SPLITTING_BY_FILE['DEFAULT']
        for name, value in SPLITTING_BY_FILE.items():
            if name in run_config['inputDataset']:
                n_files_per_group = value

        grouped_files = make_even_chunks(input_files, n_files_per_group)
        for i, f in enumerate(grouped_files):
            output_file = '{dataset}_ntuple_{job_number}.root'.format(
                dataset=run_config['outputDatasetTag'],
                job_number=i)
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
                name='ntuple_job_{0}'.format(i),
                args=args,
                output_files=[rel_out_file, rel_log_file])
            job_set.add_job(job)
            jobs.append(job)
        return jobs
