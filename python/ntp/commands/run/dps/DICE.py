"""
    run dps where=DICE:
        Runs the DailyPythonScripts (DPS) analysis code to produce the final
        set of results (plots, tables & intermediate results) in the
        Data Intensive Computing Environment (DICE).
        See 'ntp help run dps' for a complete list of parameters.
"""
from __future__ import print_function
import os
import logging

from . import Command as C
from ntp.utils.hdfs import HDFS_STORE_BASE
from ntp import NTPROOT
from ntp.commands.setup import WORKSPACE, LOGDIR, RESULTDIR
from copy import deepcopy

LOG = logging.getLogger(__name__)

try:
    import htcondenser as htc
except:
    LOG.error('Could not import htcondenser')

CONDOR_ROOT = os.path.join(WORKSPACE, 'condor')
RETRY_COUNT = 10
PREFIX = 'dps'

SETUP_SCRIPT = """
tar -xf ntp.tar.gz
source bin/env.sh
ntp setup from_tarball=cmssw.tar.gz

"""

RUN_SCRIPT = """
ntp run dps where=local $@

"""

LOG_STEM = '{0}_job.$(cluster).$(process)'.format(PREFIX)
OUT_FILE = LOG_STEM + '.out'
ERR_FILE = LOG_STEM + '.err'
LOG_FILE = LOG_STEM + '.log'

OUTPUT_DIR = os.path.join(RESULTDIR, 'dps', 'normalisation')



class Command(C):

    DEFAULTS = C.DEFAULTS

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)

        variable = self.__variables['variable']
        self.__steps = self.__variables['steps']

        self.__visiblePS = self.__variables['visiblePS']
        if self.__visiblePS:
            self.__phase_space = 'VisiblePS'
        else:
            self.__phase_space = 'FullPS'

        # create tarball
        self.__create_tar_file(args, variables)

        self.__run_variable(variable)
        # to check status:
        msg = 'To check the status you can run\n'
        msg += 'DAGstatus {0}/*.status -s'.format(self.__outdirs[0])
        LOG.info(msg)

        return True

    def __run_variable(self, variable):
        name = '{0}_{1}'.format(variable, self.__phase_space)

        if not self.__job_dir:
            out_dir = self.__get_job_dir('DPS', name)
            self.set_condor_job_directory(out_dir)

        self.__create_condor_folders()

        self.create_config('DPS', variable)
        # create DAG for condor
        self.__create_dag()

        if not self.__variables['noop']:
            self.__dag.submit(force=True)
            self.__text += "\n Submitted {0} jobs".format(len(self.__dag))
#             for job in self.__dag:
#                 print(job.name, 'running:', job.manager.exe, ' '.join(job.args))

    def create_config(self, variable):
        self.__config = {}

        self.__config['parameters'] = deepcopy(self.__variables)
        del self.__config['parameters']['pset_template']

        self.__config['outputDir'] = os.path.join(
            HDFS_STORE_BASE, 'dps', variable, self.__phase_space,
        )
        
        self.__config['variable'] = variable
        self.__config['phase_space'] = self.__phase_space
        self.__configp['visiblePS'] = self.__visiblePS

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

        dps_jobs = self.create_job_layer()
        for job in dps_jobs:
            dag_man.add_job(job, retry=RETRY_COUNT)

        self.__dag = dag_man

        self.write_job_files()

    def create_job_layer(self):
        jobs = []
        self.__root_output_files = []

        config = self.__config

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
            common_input_files=[],
            transfer_hdfs_input=False,
            hdfs_store=hdfs_store,
            certificate=self.REQUIRE_GRID_CERT,
            cpus=1,
            memory='1500MB'
        )

        parameters = 'steps={steps} variable={variable} visiblePS={visiblePS}'
        
        output_file = OUTPUT_DIR
        i = 1
        args = parameters.format(
                steps=config['steps'],
                variable=config['variable'],
                visiblePS=config['visiblePS'],
            )
        rel_out_dir = os.path.relpath(RESULTDIR, NTPROOT)
        rel_log_dir = os.path.relpath(LOGDIR, NTPROOT)
        rel_out_file = os.path.join(rel_out_dir, output_file)
        rel_log_file = os.path.join(rel_log_dir, 'ntp.log')
        job = htc.Job(
            name='{0}_{1}_job_{2}'.format(PREFIX, config['variable'], i),
            args=args,
            output_files=[rel_out_file, rel_log_file]
        )
        job_set.add_job(job)
        jobs.append(job)

        return jobs
