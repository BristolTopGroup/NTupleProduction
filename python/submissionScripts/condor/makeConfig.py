import os
import glob

pathOfCrabWorkdirs = '/storage/ec6821/NTupleProd/CMSSW_7_4_0_pre7/src/workdirCrab/v16/2015-03-31/'

version = pathOfCrabWorkdirs.split('/')[-3]

ntupleBaseDir = '/gpfs_phys/storm/cms/user/ejclemen/'

outputBaseDir = '/hdfs/TopQuarkGroup/run2/ntuples/'
outputDirHdfs = outputBaseDir + version + '/'

configFile = open('mergeConfig.py','w');

configFile.write('outputDir = "' + outputDirHdfs + '"\n')
configFile.write('jobs = [\n')

if not os.path.exists(outputDirHdfs):
	os.mkdir(outputDirHdfs)

print "There are ",len(os.listdir(pathOfCrabWorkdirs))," jobs"
for crabWorkdir in os.listdir(pathOfCrabWorkdirs):

	crabLogFile = open(pathOfCrabWorkdirs+'/'+crabWorkdir+'/crab.log','r')

	gotTaskName = False
	gotRequestName = False
	gotInputDataset = False
	taskName = ''
	requestName = ''
	inputDataset = ''
	for line in crabLogFile.readlines():

		# Get info to put together output ntuple location
		if not gotTaskName and line.find('Task name')>=0:
			tasknameTemp = line
			tasknameTemp = tasknameTemp.split('Task name:')[-1]
			tasknameTemp = tasknameTemp.split('_')
			tasknameTemp = tasknameTemp[0].strip() + '_' + tasknameTemp[1].strip()
			taskName = tasknameTemp.split(':')[0]
			gotTaskName = True
		elif not gotRequestName and line.find('publishDataName')>=0:
			requestName = line.split('\'')[-2]
			gotRequestName = True
		elif not gotInputDataset and line.find('inputDataset')>=0:
			inputDataset = line.split('/')[1]
			gotInputDataset = True

		if gotTaskName and gotRequestName and gotInputDataset :
			break

	crabLogFile.close()

	# Check if this has already been merged/exists in hdfs
	# print outputDirHdfs + '/' + requestName
	# if os.path.exists(outputDirHdfs + '/' + requestName):
	# 	continue

	ntupleDir = ntupleBaseDir + '/' + inputDataset + '/' + requestName + '/' + taskName

	filesToMerge = glob.glob(ntupleDir+'/*/*.root')

	# print outputDirHdfs + '/' + requestName
	# print ntupleDir

	configFile.write('\t["'+requestName + '",\t"' + ntupleDir + '/"],\n')

	# Merge to storage first

	# command = 'hadd -f7 ' + pathOfCrabWorkdirs + '/' + crabWorkdir + '/' + requestName + '.root '
	# for file in filesToMerge:
	# 	command += file + ' '

	# mergeDir = pathOfCrabWorkdirs + '/' + crabWorkdir + '/' + requestName +'/'
	# if not os.path.exists(mergeDir):
	# 	os.mkdir(mergeDir)
	# command = 'python myTools/mergeROOTFilesWithCompression.py ' + ntupleDir + '/*/ -o ' + mergeDir

	# # print command
	# os.system(command)

	# # Move to hdfs
	# # print 'mv ' + mergeDir + ' ' + outputDirHdfs + '/'
	# os.system('mv ' + mergeDir + ' ' + outputDirHdfs + '/')

configFile.write(']\n')
configFile.close()

