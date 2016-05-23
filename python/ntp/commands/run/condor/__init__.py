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
                      This parameter is ignored if parameter file is given.
            files:    Instead of running on a specific dataset, run over the
                      given (comma-separated) list of files
            noop:     'NO OPeration', will do everything except submitting jobs.
                      Default: false
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

SETUP_SCRIPT = """
tar -xf ntp.tar.gz
source bin/env.sh
ntp setup from_tarball=cmssw_src.tar.gz

"""

RUN_SCRIPT = """
ntp run local $@

"""

LOG_STEM = 'ntp_job.$(cluster).$(process)'


class Command(C):

    DEFAULTS = {
        'campaign': 'Spring16',
        'dataset': 'TTJets_PowhegPythia8',
        'files': '',
        'noop': False,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        self.__input_files = []

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__set_job_dirs()

        self.__create_folders()

        # create tarball
        self.__create_tar_file(args, variables)
        # which dataset, file, etc
        self.__get_run_config()
        self.__write_files()
        # create DAG for condor
        self.__create_dag()

        if not self.__variables['noop']:
            self.__dag.submit(force=True)
            self.__text += "\n Submitted {0} jobs".format(len(self.__dag))
#             for job in self.__dag:
#                 print(job.name, 'running:', job.manager.exe, ' '.join(job.args))
        # to check status:
        # ntp condor status

        return True

    def __set_job_dirs(self):
        campaign = self.__variables['campaign']
        dataset = self.__variables['dataset']
        out_dir = os.path.join(CONDOR_ROOT, campaign, dataset)

        existing_dirs = glob.glob(out_dir + '_*')
        latest = 1
        if existing_dirs:
            latest = self.__find_highest_numbering(existing_dirs)
            latest += 1
        out_dir += '_{0}'.format(latest)

        self.__job_dir = out_dir
        self.__job_log_dir = os.path.join(self.__job_dir, 'log')
        self.__setup_script = os.path.join(self.__job_dir, 'setup.sh')
        self.__run_script = os.path.join(self.__job_dir, 'run.sh')
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
        result = c.run(args, variables)
        self.__text += c.__text
        self.__input_files.extend(c.get_tar_files())

    def __get_run_config(self):
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
        input_files = find_input_files(self.__variables, LOG)

        if not using_local_files:
            dataset = self.__variables['dataset']
            campaign = self.__variables['campaign']
            run_config = get_config(campaign, dataset)
            run_config['outLFNDirBase'] = self.__replace_output_dir(run_config)
            run_config['outLFNDirBase'] = os.path.join(
                run_config['outLFNDirBase'], run_config['outputDatasetTag'])

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
        if output.startswith('/store/user'):
            tokens = output.split('/')
            output = os.path.join(HDFS_STORE_BASE, '/'.join(tokens[4:]))
            output = os.path.join(output, run_config['outputDatasetTag'])
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

        layer_1_jobs = self.__create_layer1()
        for job in layer_1_jobs:
            dag_man.add_job(job)

        layer_2_jobs = self.__create_layer2()
        for job in layer_2_jobs:
            dag_man.add_job(job, requires=layer_1_jobs)

        self.__dag = dag_man

    def __create_layer1(self):
        jobs = []

        run_config = self.__config
        input_files = run_config['files']

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
            hdfs_store=self.__config['outLFNDirBase'],
            certificate=self.REQUIRE_GRID_CERT,
            cpus=1,
            memory='1500MB'
        )
        parameters = 'files={files} output_file={output_file} {params}'
        for i, f in enumerate(input_files):
            output_file = 'ntuple_{0}.root'.format(i)
            args = parameters.format(
                files=f,
                output_file=output_file,
                params=run_config['pyCfgParams']
            )
            rel_out_dir = os.path.relpath(RESULTDIR, NTPROOT)
            rel_log_dir = os.path.relpath(LOGDIR, NTPROOT)
            rel_out_file = os.path.join(rel_out_dir, output_file)
            rel_log_file = os.path.join(rel_out_dir, 'ntp.log')
            job = htc.Job(
                name='job_{0}'.format(i),
                args=args,
                output_files=[rel_out_file, rel_log_file])
            job_set.add_job(job)
            jobs.append(job)
        return jobs

    def __create_layer2(self):
        # reserved for hadd
        return []
