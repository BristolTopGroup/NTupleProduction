import os
import glob
from mergeROOTFilesWithCompression import getGroupedFilesToUse

pathOfCrabWorkdirs = '/storage/db0268/TopCrossSections/NTupleProduction/CMSSW_7_4_15/src/workdirCrab/v2/2015-11-10'

version = pathOfCrabWorkdirs.split('/')[-2]
print version

ntupleBaseDir = '/hdfs/dpm/phy.bris.ac.uk/home/cms/store/user/doburns/'

outputBaseDir = '/hdfs/TopQuarkGroup/run2/ntuples/25ns/'
outputDirHdfs = outputBaseDir + version + '/'
print outputDirHdfs
configFile = open('mergeConfig.py','w');

configFile.write('outputDir = "' + outputDirHdfs + '"\n')
configFile.write('jobs = [\n')

if not os.path.exists(outputDirHdfs):
	os.mkdir(outputDirHdfs)

print "There are ",len(os.listdir(pathOfCrabWorkdirs))," samples"
nJobs = 0
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
		elif not gotRequestName and line.find('outputDatasetTag')>=0:
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

	files, uniqueFiles, allButUsedFiles, groupedFiles = getGroupedFilesToUse( ntupleDir + '/*/' )

	if len(groupedFiles) <= 5:
		configFile.write('\t["'+requestName + '",\t"' + ntupleDir + '/",\t-1\t],\n')
		nJobs += 1
	else :
		for job in range(0,len(groupedFiles)):
			configFile.write('\t["'+requestName + '",\t"' + ntupleDir + '/",\t'+str(job)+'\t],\n')
			nJobs += 1

configFile.write(']\n')
configFile.close()

print 'There are %s jobs' % nJobs