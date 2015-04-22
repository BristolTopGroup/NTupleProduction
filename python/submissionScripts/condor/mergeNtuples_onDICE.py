from mergeConfig import *
from optparse import OptionParser
import sys
import os
import subprocess

parser = OptionParser("Merge ntuples on DICE")
parser.add_option("-n", dest="jobNumber", default=-1,
                  type='int',
                  help="Specify which job number to run")
(options, _) = parser.parse_args()

jobNumber = options.jobNumber

if jobNumber < 0 :
	print 'Job number %i too stupid' % jobNumber
	sys.exit()
if jobNumber > len(jobs) :
	print 'Job number %i too large' % jobNumber
	sys.exit()

jobToRun = jobs[jobNumber]
sampleName = jobToRun[0]
ntupleDir = jobToRun[1]
print "Running merge for :"
print sampleName
print ntupleDir

if not os.path.exists(sampleName):
	os.mkdir(sampleName)

command = 'python mergeROOTFilesWithCompression.py ' + ntupleDir + '/*/ -o ' + sampleName
p = subprocess.Popen(command, shell=True)
p.wait()

# os.system(command)

# print 'mv ' + sampleName + ' ' + outputDir + '/'
os.system('mv ' + sampleName + ' ' + outputDir + '/')