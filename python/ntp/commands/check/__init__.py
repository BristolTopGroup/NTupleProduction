"""
    check:
        Checks the status of ongoing submissions to DICE
        
    Usage:
        check regime
        
    Parameters:
        regime: NTP or BAT [DEFAULT: Moriond17] found in workspace/condor/{}
"""

import glob
import shutil
import os
import subprocess
from .. import Command as C

class Command(C):
    DEFAULTS = {
        'folder': 'workspace/condor/{regime}/',
        'regime': 'Moriond17',
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)


    def get_folder(self):
        '''
        Returns a list of all folders within 'workspace/condor/{regime}/'
        '''
        d = self.__variables['folder'].format(
            regime=self.__variables['regime']
        ) + '*/'

        check_files = glob.glob(d)
        return check_files

    def remove_old(self, list_of_all_files):
        '''
        Removes any previous iterations. i.e. _2 supercedes _1.
        This is a very shoddy way of doing it - there must be some more elegent way?
        '''
        regime = self.__variables['regime']

        list_of_runs = []
        f_names = [f.split('/')[-2:-1][0] for f in list_of_all_files ]

        # Sort into alphabetical order
        f_names.sort()

        # Remove any older runs i.e. keep _3 over _2
        # Deal with ordering issue _1 _10 _2...
        f_old=-1
        prev_run = ''
        skip_to_1 = False
        for run in f_names:
            f_new = int(run.split('_')[-1:][0])
            if skip_to_1:
                if f_new > 1 : continue
                else: skip_to_1=False

            # End condition to always include last file.
            if run == f_names[-1]: 
                if f_new <= f_old: 
                    list_of_runs.append(prev_run)
                list_of_runs.append(run)
                break

            if f_new <= f_old: 
                if f_new > 1 : 
                    skip_to_1 = True
                    continue
                list_of_runs.append(prev_run)

            f_old = f_new 
            prev_run = run

        list_of_files = ['workspace/condor/'+regime+'/'+f+'/*.status' for f in list_of_runs]
        return list_of_files

    def run(self, args, variables):
        print "Good Morning/Afternoon/Evening"
        self.__prepare(args, variables)

        folders_in_path = self.get_folder()
        files_to_check = self.remove_old(folders_in_path)

        for f in files_to_check:
            command = ' '.join([
                'DAGstatus', 
                f, 
                '-s']
            )
            os.system(command)
