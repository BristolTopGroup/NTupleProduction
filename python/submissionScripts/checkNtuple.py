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

pathOfCrabWorkdirs = '/storage/db0268/TopCrossSections/NTupleProduction/CMSSW_7_4_15/src/workdirCrab/v29/2015-10-28'

for crabWorkdir in os.listdir(pathOfCrabWorkdirs):
	if crabWorkdir == 'crab_TTJets_PowhegPythia6Tauola' : continue

	unkownOrFailed = True
	finished = False
	failedToSubmit = False
	someJobsFailed = False
	numberOfAttempts = 0
	percentDone = '0'
	while unkownOrFailed:
		if numberOfAttempts > 0 : 'Trying again'
		p = subprocess.Popen(['crab', 'status',pathOfCrabWorkdirs+crabWorkdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = p.communicate()

		for line in out.split('\n'):
			if line.find('finished')>=0 :
				if line.find('100')>=0:
					percentDone = '100'
					finished = True
					unkownOrFailed = False
					break
				else :
					percentDone = line.split('finished')[-1].split('%')[0].strip()
			elif line.find('Task status')>=0 and line.find('FAILED')>=0:
				failedToSubmit = True
				break
			elif line.find('failed')>=0:
				someJobsFailed = True
				break

		numberOfAttempts += 1
		# Limit number of attempts of checking status of particular job
		if numberOfAttempts >=3 : break

	if finished: print crabWorkdir + ' ' + bcolors.OKGREEN + 'FINISHED' + bcolors.ENDC
	elif failedToSubmit:
		print crabWorkdir + ' ' + bcolors.FAIL + 'FAILED TO SUBMIT' + bcolors.ENDC #+ '...' + bcolors.OKBLUE + 'RESUBMITTING' + bcolors.ENDC
		p = subprocess.Popen(['crab', 'status',pathOfCrabWorkdirs+crabWorkdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# out, err = p.communicate()
		p = subprocess.Popen(['crab', 'resubmit',pathOfCrabWorkdirs+crabWorkdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# out, err = p.communicate() 
		# print out
	elif someJobsFailed:
		print crabWorkdir + ' ' + bcolors.FAIL + 'SOME JOBS FAILED' + bcolors.ENDC + '...' + bcolors.OKBLUE + percentDone + '%' + bcolors.ENDC + '...' + bcolors.OKBLUE + 'RESUBMITTING' + bcolors.ENDC
		p = subprocess.Popen(['crab', 'resubmit',pathOfCrabWorkdirs+crabWorkdir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# out, err = p.communicate() 
		# print out
	else: print crabWorkdir + ' ' + bcolors.WARNING + 'INCOMPLETE' + bcolors.ENDC + '...' + bcolors.OKBLUE + percentDone + '%' + bcolors.ENDC + '\n' + out
