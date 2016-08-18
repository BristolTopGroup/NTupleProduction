"""
    merge:
        Merges ROOT files
        
    Usage:
        merge file1 [file2 file3 ...] output_file=merged.root [compression=<int>]
        
    Parameters:
        output_file: name of the output file. Default: merged.root
        compression: compression factor [0-9]. Default: 7
"""
import logging
import os
from .. import Command as C
from ntp.commands.setup import CMSSW_SRC
from hepshell.interpreter import time_function

LOG = logging.getLogger(__name__)

MAX_INPUT_HADD = 500

# skipGroupsUntil = 0
# startWithGroup = 1
# sizePerFile = 1024 * 1024 * 1024 * 2
# timeCut = 0


class Command(C):
    DEFAULTS = {
        'output_file': 'merged.root',
        'compression': 7,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    @time_function('merge', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        files = [os.path.abspath(f) for f in args]
        output_file = os.path.abspath(self.__variables['output_file'])
        compression = self.__variables['compression']

        n_files = len(files)
        if n_files < MAX_INPUT_HADD:
            self.__run_hadd(output_file, files, compression)
        else:
            N = MAX_INPUT_HADD - 1
            grouped_files = [files[n:n + N]
                             for n in range(0, len(files), N)]
            tmp_outputs = []
            for i, input_files in enumerate(grouped_files):
                tmp_output = 'tmp_merge_{0}.root'.format(i)
                tmp_outputs.append(tmp_output)
                self.__run_hadd(tmp_output, input_files, compression=0)
            self.__run_hadd(output_file, tmp_outputs, compression)
            for f in tmp_outputs:
                os.remove(f)
            

        self.__text = "Merged {0} files into {1}".format(n_files, output_file)

        return True

    def __run_hadd(self, output_file, files, compression):
        '''
            If the option -k is used, hadd will not exit on corrupt or
            non-existant input files but skip the offending files instead.
        '''
        commands = [
            'cd {CMSSW_SRC}',
            'source /cvmfs/cms.cern.ch/cmsset_default.sh',
            'eval `/cvmfs/cms.cern.ch/common/scram runtime -sh`',
            'hadd -k -f{compression} {output_file} {files}',
        ]

        all_in_one = ' && '.join(commands)
        all_in_one = all_in_one.format(
            CMSSW_SRC=CMSSW_SRC,
            files=' '.join(files),
            output_file=output_file,
            compression=compression,
        )

        LOG.info("Merging files")
        from hepshell.interpreter import call
        code, _, _ = call(
            [all_in_one], LOG, stdout_log_level=logging.INFO, shell=True)

        return code
