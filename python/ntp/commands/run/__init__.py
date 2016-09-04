"""
    run:    Runs the n-tuple production.
            All run commands require a valid grid certificate as they
            either read data from the grid via XRootD or run on grid
            resources.
        Usage:
            run [<where>] [sample=<X>]
        Parameters:
            where:    Where to run NTP. Can be grid|condor|local.
                      For location specific parameters, please run
                        help run <where>
                      Default: local
            sample:   Which sample to run over.
                      Default: test
"""

from .. import Command as C
import subprocess
import os
from ..setup import WORKSPACE
CONDOR_ROOT = os.path.join(WORKSPACE, 'condor')


class Command(C):
    REQUIRE_GRID_CERT = True

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        from .local import Command
        c = Command()
        result = c.run(args, variables)
        self.__text = c.get_text()

        return result

    def __prepare(self, args, variables):
        super(Command, self).__prepare(args, variables)

    def __extract_params(self):
        args = []
        for var, value in self.__variables.items():
            if var in self.DEFAULTS:
                continue
            args.append('{0}={1}'.format(var, value))
        return ' '.join(args)

    def __format_input_files(self, input_files):
        results = []
        for f in input_files:
            results.append('"{0}"'.format(f))
        return ',\n'.join(results)

    def __create_tar_file(self, args, variables):
        from ntp.commands.create.tarball import Command as TarCommand
        no_operation = 'noop' in self.__variables and self.__variables['noop']
        if no_operation and TarCommand.tarballs_exist():
            return
        if self.__have_fresh_tar_files:
            return
        c = TarCommand()
        c.run(args, variables)
        self.__text += c.__text
        self.__input_files.extend(c.get_tar_files())
        self.__have_fresh_tar_files = True

    def __get_job_dir(self, category, name):
        out_dir = os.path.join(CONDOR_ROOT, category, name)
        out_dir = self.__get_latest_outdir(out_dir)

        return out_dir

    def set_condor_job_directory(self, directory):
        self.__job_dir = directory
        self.__outdirs.append(directory)
        self.__job_log_dir = os.path.join(directory, 'log')
        self.__setup_script = os.path.join(directory, self.__setup_script)
        self.__run_script = os.path.join(directory, self.__run_script)
        self.__config_file = os.path.join(directory, self.__config_file)

    def __get_latest_outdir(self, out_dir):
        from ntp.utils import find_latest_iteration
        import glob
        existing_dirs = glob.glob(out_dir + '_*')
        latest = 1
        if existing_dirs:
            latest = find_latest_iteration(existing_dirs)
            latest += 1
        out_dir += '_{0}'.format(latest)
        return out_dir

    def __create_condor_folders(self):
        dirs = [CONDOR_ROOT, self.__job_dir, self.__job_log_dir]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
