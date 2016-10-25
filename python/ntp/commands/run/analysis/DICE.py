"""
    run analysis where=DICE:
        Runs the analysis in the Data Intensive Computing Environment.
        See 'ntp help run analysis' for a complete list of parameters.
"""
from __future__ import print_function
import os
import logging

from . import Command as C
from ntp.utils.hdfs import HDFS_STORE_BASE
from ntp import NTPROOT
from ntp.commands.setup import WORKSPACE, LOGDIR, RESULTDIR
from ntp.utils import make_even_chunks
from . import ANALYSIS_MODES
from copy import deepcopy

LOG = logging.getLogger(__name__)

try:
    import htcondenser as htc
except:
    LOG.error('Could not import htcondenser')

CONDOR_ROOT = os.path.join(WORKSPACE, 'condor')
RETRY_COUNT = 10
PREFIX = 'analysis'

SETUP_SCRIPT = """
tar -xf ntp.tar.gz
source bin/env.sh
ntp setup from_tarball=cmssw.tar.gz

"""

RUN_SCRIPT = """
ntp run analysis where=local $@ nevents=0

"""

LOG_STEM = '{0}_job.$(cluster).$(process)'.format(PREFIX)
OUT_FILE = LOG_STEM + '.out'
ERR_FILE = LOG_STEM + '.err'
LOG_FILE = LOG_STEM + '.log'


# file splitting for datasets containing 'key'
# Analysis jobs: 1 file = 17s processing time
SPLITTING_BY_FILE = {
    'SingleElectron': 3,
    'SingleMuon': 3,
    'TTJet': 4,
    'TT_': 5,
    'DEFAULT': 50,  # ~= 14 min
}

N_FILES_PER_ANALYSIS_JOB = SPLITTING_BY_FILE['DEFAULT']


class Command(C):

    DEFAULTS = C.DEFAULTS

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)

        dataset = self.__variables['dataset']
        mode = self.__variables['mode']

        # create tarball
        self.__create_tar_file(args, variables)

        self.__run_dataset(dataset, mode)
        # to check status:
        msg = 'To check the status you can run\n'
        if len(self.__outdirs) == 1:
            msg += 'DAGstatus {0}/*.status -s'.format(self.__outdirs[0])
        else:
            msg += 'DAGstatus workspace/condor/*/*.status -s'
        LOG.info(msg)

        return True

    def __run_dataset(self, dataset, mode):
        name = '{0}_{1}'.format(dataset, mode)

        if not self.__job_dir:
            out_dir = self.__get_job_dir('BAT', name)
            self.set_condor_job_directory(out_dir)

        self.__create_condor_folders()

        self.create_config('BAT', dataset)
        # create DAG for condor
        self.__create_dag()

        if not self.__variables['noop']:
            self.__dag.submit(force=True)
            self.__text += "\n Submitted {0} jobs".format(len(self.__dag))
#             for job in self.__dag:
#                 print(job.name, 'running:', job.manager.exe, ' '.join(job.args))

    def create_config(self, campaign, dataset):
        self.__config = {}

        self.__config['unitsPerJob'] = N_FILES_PER_ANALYSIS_JOB
        self.__config['parameters'] = deepcopy(self.__variables)
        del self.__config['parameters']['pset_template']

        self.__config['outputDir'] = os.path.join(
            HDFS_STORE_BASE, 'atOutput', dataset
        )

    def write_job_files(self):
        with open(self.__setup_script, 'w+') as f:
            f.write(SETUP_SCRIPT)

        with open(self.__run_script, 'w+') as f:
            f.write(RUN_SCRIPT)

        import json
        with open(self.__config_file, 'w+') as f:
            f.write(json.dumps(self.__config, indent=4))

    def __create_dag(self):
        """ Creates a Directional Acyclic Grag (DAG) for condor """
        dag_file = os.path.join(self.__job_dir, '{0}.dag'.format(PREFIX))
        dag_status = os.path.join(self.__job_dir, '{0}.status'.format(PREFIX))
        dot_file = '{0}.dot'.format(PREFIX)
        dag_man = htc.DAGMan(
            filename=dag_file, status_file=dag_status, dot=dot_file,
        )

        input_files = self.__config['parameters']['input_files']
        # layer 2 - analysis
        for mode in ANALYSIS_MODES:
            analysis_jobs = self.create_job_layer(input_files, mode)
            for job in analysis_jobs:
                dag_man.add_job(job, retry=RETRY_COUNT)
            # # layer 2b
            # # for each analysis mode create 1 merged file
            # merge_jobs = self.__create_merge_layer(analysis_jobs, mode)
            # for job in merge_jobs:
            #     dag_man.add_job(job, requires=analysis_jobs, retry=2)

        # # layer 2 - analysis
        # for mode in ANALYSIS_MODES:
        #     analysis_jobs = self.__create_analysis_layer(ntuple_jobs, mode)
        #     for job in analysis_jobs:
        #         dag_man.add_job(job, requires=ntuple_jobs, retry=RETRY_COUNT)
        #     # layer 2b
        #     # for each analysis mode create 1 merged file
        #     merge_jobs = self.__create_merge_layer(analysis_jobs, mode)
        #     for job in merge_jobs:
        #         dag_man.add_job(job, requires=analysis_jobs, retry=2)

        self.__dag = dag_man

        self.write_job_files()

    def create_job_layer(self, input_files, mode):
        jobs = []
        self.__root_output_files = []

        config = self.__config
        if self.__variables['test']:
            input_files = [input_files[0]]
        self.__config['input_files'] = input_files

        hdfs_store = config['outputDir']
        job_set = htc.JobSet(
            exe=self.__run_script,
            copy_exe=True,
            setup_script=self.__setup_script,
            filename=os.path.join(self.__job_dir, '{0}.condor'.format(PREFIX)),
            out_dir=self.__job_log_dir,
            out_file=OUT_FILE,
            err_dir=self.__job_log_dir,
            err_file=ERR_FILE,
            log_dir=self.__job_log_dir,
            log_file=LOG_FILE,
            share_exe_setup=True,
            common_input_files=self.__input_files,
            transfer_hdfs_input=False,
            hdfs_store=hdfs_store,
            certificate=self.REQUIRE_GRID_CERT,
            cpus=1,
            memory='1500MB',
        )

        job_set.job_template='/storage/ec6821/NTupleProd/new/NTupleProduction/job.condor'


        parameters = 'files={files} output_file_suffix={suffix} mode={mode}'
        parameters += ' dataset={dataset}'

        n_files_per_group = N_FILES_PER_ANALYSIS_JOB
        grouped_files = make_even_chunks(
            input_files, size_of_chunk=n_files_per_group)

        dataset = config['parameters']['dataset']
        for i, f in enumerate(grouped_files):
            suffix = 'atOutput_{job_number}.root'.format(
                dataset=dataset,
                mode=mode,
                job_number=i
            )

            args = parameters.format(
                files=','.join(f),
                suffix=suffix,
                mode=mode,
                dataset=dataset,
            )
            output_file = '_'.join([dataset, mode, suffix])
            rel_out_dir = os.path.relpath(RESULTDIR, NTPROOT)
            rel_log_dir = os.path.relpath(LOGDIR, NTPROOT)
            rel_out_file = os.path.join(rel_out_dir, output_file)
            rel_log_file = os.path.join(rel_log_dir, 'ntp.log')
            job = htc.Job(
                name='{0}_{1}_job_{2}'.format(PREFIX, mode, i),
                args=args,
                output_files=[rel_out_file, rel_log_file])
            job_set.add_job(job)
            jobs.append(job)

        return jobs