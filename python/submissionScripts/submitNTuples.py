from datetime import date
import io
from shutil import move
from os import remove
import os

version = '11'
crabWorkArea = 'workdirCrab/v'+version+'/'+str(date.today())
print 'Using workdir ',crabWorkArea
miniAodDir = 'BristolAnalysis/NTupleTools/python/crab/FALL15/'
jobConfigs = [

# Data
miniAodDir+'SingleMuon_16Dec2015_RunC.py',
miniAodDir+'SingleElectron_16Dec2015_RunC.py',
miniAodDir+'SingleMuon_16Dec2015_RunD.py',
miniAodDir+'SingleElectron_16Dec2015_RunD.py',

# MC
# Central
miniAodDir + 'TTJets_PowhegPythia8.py',

# Backgrounds and Tunes/Generators
miniAodDir + 'DYJetsToLL_M50.py',
miniAodDir + 'GJets_100to200.py',
miniAodDir + 'GJets_200to400.py',
miniAodDir + 'GJets_400to600.py',
miniAodDir + 'GJets_600toInf.py',
miniAodDir + 'QCD_EMEnriched_120to170.py',
miniAodDir + 'QCD_EMEnriched_15to20.py',
miniAodDir + 'QCD_EMEnriched_170to300.py',
miniAodDir + 'QCD_EMEnriched_20to30.py',
miniAodDir + 'QCD_EMEnriched_300toInf.py',
# miniAodDir + 'QCD_EMEnriched_30to50.py',
miniAodDir + 'QCD_EMEnriched_50to80.py',
miniAodDir + 'QCD_EMEnriched_80to120.py',
miniAodDir + 'QCD_MuEnriched_1000toInf.py',
miniAodDir + 'QCD_MuEnriched_120to170.py',
# miniAodDir + 'QCD_MuEnriched_15to20.py',
miniAodDir + 'QCD_MuEnriched_170to300.py',
miniAodDir + 'QCD_MuEnriched_20to30.py',
miniAodDir + 'QCD_MuEnriched_300to470.py',
miniAodDir + 'QCD_MuEnriched_30to50.py',
miniAodDir + 'QCD_MuEnriched_470to600.py',
miniAodDir + 'QCD_MuEnriched_50to80.py',
miniAodDir + 'QCD_MuEnriched_600to800.py',
miniAodDir + 'QCD_MuEnriched_800to1000.py',
miniAodDir + 'QCD_MuEnriched_80to120.py',
miniAodDir + 'QCD_bcToE_15to20.py',
miniAodDir + 'QCD_bcToE_170to250.py',
miniAodDir + 'QCD_bcToE_20to30.py',
miniAodDir + 'QCD_bcToE_250toInf.py',
miniAodDir + 'QCD_bcToE_30to80.py',
miniAodDir + 'QCD_bcToE_80to170.py',
miniAodDir + 'TTJets_PowhegPythia8_mtop1695.py',
miniAodDir + 'TTJets_PowhegPythia8_mtop1755.py',
miniAodDir + 'TTJets_PowhegPythia8_scaledown.py',
miniAodDir + 'TTJets_PowhegPythia8_scaleup.py',
miniAodDir + 'TTJets_amcatnloFXFX.py',
miniAodDir + 'TTJets_amcatnloHerwigpp.py',
miniAodDir + 'TTJets_PowhegHerwigpp.py',
miniAodDir + 'TTJets_madgraphMLM.py',
miniAodDir + 'TToLeptons_t.py',
miniAodDir + 'T_tW.py',
miniAodDir + 'Tbar_tW.py',
miniAodDir + 'WJetsToLNu.py',
]

# Replace workArea name in commonConfig.py
commonConfig = 'BristolAnalysis/NTupleTools/python/crab/base.py'
tempCommonConfig = 'BristolAnalysis/NTupleTools/python/crab/base.py_temp'
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
