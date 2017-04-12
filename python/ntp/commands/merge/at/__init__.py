"""
    merge:
        Merges ROOT files
        
    Usage:
        merge file1 [file2 file3 ...] output_file=merged.root [compression=<int>]
        
    Parameters:
        output_file: name of the output file. Default: merged.root
        compression: compression factor [0-9]. Default: 7
"""
# import htcondenser as htc
# import condor-comforter as cc
# from cc.haddaway import haddaway

import glob
import shutil
import logging
import os
import time
import subprocess
from .. import Command as C
from hepshell.interpreter import time_function

# from ntp.utils import make_even_chunks

LOG = logging.getLogger(__name__)
import haddaway

try:
    import htcondenser as htc
except:
    LOG.error('Could not import htcondenser')

PREFIX = 'atMerge'
LOG_STEM = '{0}_job.$(cluster).$(process)'.format(PREFIX)
OUT_FILE = LOG_STEM + '.out'
ERR_FILE = LOG_STEM + '.err'
LOG_FILE = LOG_STEM + '.log'

# skipGroupsUntil = 0
# startWithGroup = 1
# sizePerFile = 1024 * 1024 * 1024 * 2
# timeCut = 0

class Command(C):
    DEFAULTS = {
        'output_file': 'merged.root',
        'compression': 7,
        'output_dir': '',
        'input_jobs': '',
        'input_dir': '/hdfs/TopQuarkGroup/{user}/{version}/atOutput/',
        'user': 'ec6821',
        'version': '1.0.5',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        # condor specific
        self.__have_fresh_tar_files = False
        self.__input_files = []
        self.__job_log_dir = ''
        self.__job_dir = ''
        self.__outdirs = []
        self.__run_merging = 'merge.sh'
        self.__run_script = 'run.sh'
        self.__config_file = 'config.json'


    def get_datasets(self):
        from .atMerge import mergingFiles
        return mergingFiles

    def get_file_base(self):
        path = self.__variables['input_dir']
        path = path.format(user=self.__variables['user'], version = self.__variables['version'])
        return path

    def get_complete_list(self, filesToMerge, path):
        for i, sample in enumerate(filesToMerge):
            # [output file name][input file names][central|+-JES|+-JES]
            f_list = sample[1]
            for j, f in enumerate(f_list):
                datasetMidpath = f.split('_atOutput')[0]
                datasetMidpath = datasetMidpath.split('_'+sample[2])[0]
                datasetMidpath += '/analysis_{variation}_job_*/'.format(variation=sample[2])
                filesToMerge[i][1][j]=path+datasetMidpath+f
        return filesToMerge

    @time_function('merge', LOG)
    def run(self, args, variables):
        print "Good Morning/Afternoon/Evening"
        # set all self.__variables to those in DEFAULT / args
        self.__prepare(args, variables)

        filesToMerge = self.get_datasets()
        path = self.get_file_base()
        jobs = self.get_complete_list(filesToMerge, path)

        for sample_to_merge in jobs:
            OUTPUTFILE = path+'combined/'+sample_to_merge[0]
            INPUTFILES = []
            for f in sample_to_merge[1]:
                INPUTFILES += glob.glob(f)

            nJobs = len(INPUTFILES)
            INPUTFILES = ' '.join(INPUTFILES)

            SIZE = 15
            SIZE = str(SIZE)

            command = ' '.join([
                'haddaway.py', 
                '--output', OUTPUTFILE, 
                '--size', SIZE, 
                '--input', INPUTFILES,
                ]
            )
            print "Merging to : ", OUTPUTFILE
            print "Number of Intermediate hadds : ", nJobs / int(SIZE)
            os.system(command)
            time.sleep(2)
