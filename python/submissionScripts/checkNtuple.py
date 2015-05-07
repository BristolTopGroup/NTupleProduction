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

pathOfCrabWorkdirs = '/storage/ec6821/NTupleProd/CMSSW_7_4_0_pre7/src/workdirCrab/v16/2015-03-31/'

for crabWorkdir in os.listdir(pathOfCrabWorkdirs):
	# if crabWorkdir != 'crab_TTJets_Madgraph_PU4bx50' : continue

	unkownOrFailed = True
	finished = False
	failedToSubmit = False
	numberOfAttempts = 0
	while unkownOrFailed:
		if numberOfAttempts > 0 : 'Trying again'
		p = subprocess.Popen(['crab', 'status',pathOfCrabWorkdirs+crabWorkdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()

		for line in out.split('\n'):
			if line.find('finished')>=0 and line.find('100')>=0:
				finished = True
				unkownOrFailed = False
				break
			elif line.find('Task status')>=0 and line.find('FAILED')>=0:
				failedToSubmit = True
				break

		numberOfAttempts += 1
		# Limit number of attempts of checking status of particular job
		if numberOfAttempts >=3 : break

	if finished: print crabWorkdir + ' ' + bcolors.OKGREEN + 'FINISHED' + bcolors.ENDC
	elif failedToSubmit:
		print crabWorkdir + ' ' + bcolors.FAIL + 'FAILED TO SUBMIT' + bcolors.ENDC #+ '...' + bcolors.OKBLUE + 'RESUBMITTING' + bcolors.ENDC
		# p = subprocess.Popen(['crab', 'status',pathOfCrabWorkdirs+crabWorkdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# out, err = p.communicate()
	else: print crabWorkdir + ' ' + bcolors.WARNING + 'INCOMPLETE' + bcolors.ENDC + '\n' + out
