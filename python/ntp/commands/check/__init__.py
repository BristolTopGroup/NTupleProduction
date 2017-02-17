"""
    check:
        Checks the status of ongoing submissions to DICE
        
    Usage:
        check regime
        
    Parameters:
        regime: NTP or BAT? [DEFAULT: Moriond17] found in workspace/condor/{}
"""

import glob
import shutil
import os
import subprocess

from ntp.commands.setup import WORKSPACE
from ntp.utils import find_latest_iteration
from crab.datasets import DATASETS

from .. import Command as C

class Command(C):
    DEFAULTS = {
        'regime': 'Moriond17',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def get_folder(self):
        '''
        Returns a list of all folders within 'workspace/condor/{regime}/'
        '''
        r = self.__variables['regime']
        p = WORKSPACE+'/condor/{regime}/'.format(
            regime=r
        ) + '*/'

        d = DATASETS[r].keys()
        print d

        check_files = glob.glob(p)
        check_files.sort()
        return check_files, d

    def return_datasets_to_check(self):
        '''
        Returns the newest version of datasets to check.
        '''
        list_of_all_files, datasets = self.get_folder()

        list_of_datasets = []
        for dataset in datasets:
            list_of_files = []
            for l in list_of_all_files:
                if dataset in l:
                    list_of_files.append(l)

            i = find_latest_iteration(list_of_files)
            f_to_use = list_of_files[0].replace('_1', '_'+str(i))+'*.status'
            list_of_datasets.append(f_to_use)

        return list_of_datasets

    def run(self, args, variables):
        print "Good Morning/Afternoon/Evening"
        self.__prepare(args, variables)

        files_to_check = self.return_datasets_to_check()

        for f in files_to_check:
            command = ' '.join([
                'DAGstatus', 
                f, 
                '-s']
            )
            os.system(command)
