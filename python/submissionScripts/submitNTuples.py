from datetime import date
import io
from shutil import move
from os import remove
import os

version = '16'
crabWorkArea = 'workdirCrab/v'+version+'/'+str(date.today())
print 'Using workdir ',crabWorkArea
miniAodDir = 'BristolAnalysis/NTupleTools/Configuration/crab3Configurations/'
jobConfigs = [
 miniAodDir+'TTJets_Madgraph_PU20bx25.py',
 miniAodDir+'TTJets_Madgraph_PU30bx50.py',
 # miniAodDir+'TTJets_Madgraph_PU4bx50.py',
 miniAodDir+'TT_Pythia8_PU20bx25.py',
 miniAodDir+'TT_Pythia8_PU20bx25_mass1755.py',
 miniAodDir+'TT_Pythia8_PU20bx25_scaleup.py',
 miniAodDir+'TT_Pythia8_PU30bx50.py',
 miniAodDir+'TT_Pythia8_PU40bx25.py',

 miniAodDir+'TBarToLeptons_s_PU20bx25.py',
 miniAodDir+'TBarToLeptons_t_PU20bx25.py',
 miniAodDir+'TToLeptons_s_PU20bx25.py',
 miniAodDir+'TToLeptons_t_PU20bx25.py',
 miniAodDir+'T_tW_PU20bx25.py',
 miniAodDir+'Tbar_tW_PU20bx25.py',
 miniAodDir+'WJets_PU20bx25.py',
 miniAodDir+'DYJetsToLL_M50_PU20bx25.py',

 miniAodDir+'GJets_100to200_PU20bx25.py',
 miniAodDir+'GJets_200to400_PU20bx25.py',
 miniAodDir+'GJets_400to600_PU20bx25.py',
 miniAodDir+'GJets_600toInf_PU20bx25.py',
 miniAodDir+'QCD_EMEnriched_20to30_PU20bx25.py',
 miniAodDir+'QCD_EMEnriched_30to80_PU20bx25.py',
 miniAodDir+'QCD_EMEnriched_80to170_PU20bx25.py',
 miniAodDir+'QCD_bcToE_170toInf_PU20bx25.py',
 miniAodDir+'QCD_bcToE_80to170_PU20bx25.py',
 miniAodDir+'QCD_bcToE_30to80_PU20bx25.py',
 miniAodDir+'QCD_bcToE_20to30_PU20bx25.py',
 miniAodDir+'QCD_MuEnriched_20toInf_PU20bx25.py',
 miniAodDir+'QCD_MuEnriched_30to50_PU20bx25.py',
 miniAodDir+'QCD_MuEnriched_50to80_PU20bx25.py',
 miniAodDir+'QCD_MuEnriched_80to120_PU20bx25.py',
]

# Replace workArea name in commonConfig.py
commonConfig = 'BristolAnalysis/NTupleTools/python/commonConfig.py'
tempCommonConfig = 'BristolAnalysis/NTupleTools/python/commonConfig.py_temp'
openCommonConfig = open(commonConfig)
openTempCommonConfig = open(tempCommonConfig, 'w')

oldLine = 'config.General.workArea'
newLine = 'config.General.workArea = \''+crabWorkArea+'\'\n'

for line in openCommonConfig:
	if line.find(oldLine)>=0:
		openTempCommonConfig.write(newLine)
	else:
		openTempCommonConfig.write(line)
openCommonConfig.close()
openTempCommonConfig.close()
move(tempCommonConfig,commonConfig)

# Submit jobs
for config in jobConfigs:
	os.system('crab submit '+config)
