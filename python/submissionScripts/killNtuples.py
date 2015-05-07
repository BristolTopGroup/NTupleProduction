import os, subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

pathOfCrabWorkdirs = '/storage/ec6821/NTupleProd/CMSSW_7_4_0_pre7/src/workdirCrab/v11/2015-03-05/'

for crabWorkdir in os.listdir(pathOfCrabWorkdirs):
	os.system('crab kill ' + pathOfCrabWorkdirs+crabWorkdir )

