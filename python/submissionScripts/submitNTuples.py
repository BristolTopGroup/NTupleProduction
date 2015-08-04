from datetime import date
import io
from shutil import move
from os import remove
import os

version = '22'
crabWorkArea = 'workdirCrab/v'+version+'/'+str(date.today())
print 'Using workdir ',crabWorkArea
miniAodDir = 'BristolAnalysis/NTupleTools/Configuration/crab3Configurations/50ns/'
jobConfigs = [

miniAodDir+'SingleMuon_PromptReco.py',
miniAodDir+'SingleMuon_ReReco.py',
miniAodDir+'SingleElectron_PromptReco.py',
miniAodDir+'SingleElectron_ReReco.py',


# miniAodDir + 'TTJets_PowhegPythia8.py',

# miniAodDir + 'DYJetsToLL_M50.py',
# miniAodDir + 'GJets_15to6000.py',
# miniAodDir + 'QCD_EMEnriched_120to170.py',
# miniAodDir + 'QCD_EMEnriched_15to20.py',
# miniAodDir + 'QCD_EMEnriched_170to300.py',
# miniAodDir + 'QCD_EMEnriched_20to30.py',
# miniAodDir + 'QCD_EMEnriched_300toInf.py',
# miniAodDir + 'QCD_EMEnriched_30to50.py',
# miniAodDir + 'QCD_EMEnriched_50to80.py',
# miniAodDir + 'QCD_EMEnriched_80to120.py',
# miniAodDir + 'QCD_MuEnriched_1000toInf.py',
# miniAodDir + 'QCD_MuEnriched_120to170.py',
# miniAodDir + 'QCD_MuEnriched_15to20.py',
# miniAodDir + 'QCD_MuEnriched_170to300.py',
# miniAodDir + 'QCD_MuEnriched_20to30.py',
# miniAodDir + 'QCD_MuEnriched_300to470.py',
# miniAodDir + 'QCD_MuEnriched_30to50.py',
# miniAodDir + 'QCD_MuEnriched_470to600.py',
# miniAodDir + 'QCD_MuEnriched_50to80.py',
# miniAodDir + 'QCD_MuEnriched_600to800.py',
# miniAodDir + 'QCD_MuEnriched_800to1000.py',
# miniAodDir + 'QCD_MuEnriched_80to120.py',
# miniAodDir + 'QCD_bcToE_15to20.py',
# miniAodDir + 'QCD_bcToE_170to250.py',
# miniAodDir + 'QCD_bcToE_20to30.py',
# miniAodDir + 'QCD_bcToE_250toInf.py',
# miniAodDir + 'QCD_bcToE_30to80.py',
# miniAodDir + 'QCD_bcToE_80to170.py',
# miniAodDir + 'TTJets_PowhegPythia6Tauola.py',
# miniAodDir + 'TTJets_PowhegPythia8_mtop1695.py',
# miniAodDir + 'TTJets_PowhegPythia8_mtop1755.py',
# miniAodDir + 'TTJets_PowhegPythia8_scaledown.py',
# miniAodDir + 'TTJets_PowhegPythia8_scaleup.py',
# miniAodDir + 'TTJets_amcatnloFXFX.py',
# miniAodDir + 'TTJets_amcatnloFXFX_mtop1695.py',
# miniAodDir + 'TTJets_amcatnloFXFX_mtop1755.py',
# miniAodDir + 'TTJets_amcatnloFXFX_scaledown.py',
# miniAodDir + 'TTJets_amcatnloFXFX_scaleup.py',
# miniAodDir + 'TTJets_madgraphMLM.py',
# miniAodDir + 'TToLeptons_t.py',
# miniAodDir + 'T_tW.py',
# miniAodDir + 'Tbar_tW.py',
# miniAodDir + 'WJetsToLNu.py',


# ## 74X MC
# ## 25 ns
# miniAodDir+'TTJets_amcatnloFXFX.py',
# miniAodDir+'DYJetsToLL_M50.py',
# miniAodDir+'QCD_EMEnriched_120to170.py',
# miniAodDir+'QCD_EMEnriched_15to20.py',
# miniAodDir+'QCD_EMEnriched_170to300.py',
# miniAodDir+'QCD_EMEnriched_20to30.py',
# miniAodDir+'QCD_EMEnriched_30to50.py',
# miniAodDir+'QCD_EMEnriched_50to80.py',
# miniAodDir+'QCD_EMEnriched_80to120.py',
# miniAodDir+'QCD_MuEnriched_1000toInf.py',
# miniAodDir+'QCD_MuEnriched_120to170.py',
# miniAodDir+'QCD_MuEnriched_15to20.py',
# miniAodDir+'QCD_MuEnriched_170to300.py',
# miniAodDir+'QCD_MuEnriched_20to30.py',
# miniAodDir+'QCD_MuEnriched_300to470.py',
# miniAodDir+'QCD_MuEnriched_30to50.py',
# miniAodDir+'QCD_MuEnriched_470to600.py',
# miniAodDir+'QCD_MuEnriched_50to80.py',
# miniAodDir+'QCD_MuEnriched_600to800.py',
# miniAodDir+'QCD_MuEnriched_80to120.py',
# miniAodDir+'QCD_bcToE_15to20.py',
# miniAodDir+'QCD_bcToE_170to250.py',
# miniAodDir+'QCD_bcToE_20to30.py',
# miniAodDir+'QCD_bcToE_250toInf.py',
# miniAodDir+'QCD_bcToE_80to170.py',
# miniAodDir+'TTJets_amcatnloFXFX_mtop1695.py',
# miniAodDir+'TTJets_amcatnloFXFX_scaledown.py',
# miniAodDir+'TTJets_madgraphMLM.py',
# miniAodDir+'TToLeptons_t.py',
# miniAodDir+'T_tW.py',
# miniAodDir+'Tbar_tW.py',
# miniAodDir+'WJetsToLNu.py',

### PHYS14
 # miniAodDir+'TTJets_Madgraph_PU20bx25.py',
 # miniAodDir+'TTJets_Madgraph_PU30bx50.py',
 # # miniAodDir+'TTJets_Madgraph_PU4bx50.py',
 # miniAodDir+'TT_Pythia8_PU20bx25.py',
 # miniAodDir+'TT_Pythia8_PU20bx25_mass1755.py',
 # miniAodDir+'TT_Pythia8_PU20bx25_scaleup.py',
 # miniAodDir+'TT_Pythia8_PU30bx50.py',
 # miniAodDir+'TT_Pythia8_PU40bx25.py',

 # miniAodDir+'TBarToLeptons_s_PU20bx25.py',
 # miniAodDir+'TBarToLeptons_t_PU20bx25.py',
 # miniAodDir+'TToLeptons_s_PU20bx25.py',
 # miniAodDir+'TToLeptons_t_PU20bx25.py',
 # miniAodDir+'T_tW_PU20bx25.py',
 # miniAodDir+'Tbar_tW_PU20bx25.py',
 # miniAodDir+'WJets_PU20bx25.py',
 # miniAodDir+'DYJetsToLL_M50_PU20bx25.py',

 # miniAodDir+'GJets_100to200_PU20bx25.py',
 # miniAodDir+'GJets_200to400_PU20bx25.py',
 # miniAodDir+'GJets_400to600_PU20bx25.py',
 # miniAodDir+'GJets_600toInf_PU20bx25.py',
 # miniAodDir+'QCD_EMEnriched_20to30_PU20bx25.py',
 # miniAodDir+'QCD_EMEnriched_30to80_PU20bx25.py',
 # miniAodDir+'QCD_EMEnriched_80to170_PU20bx25.py',
 # miniAodDir+'QCD_bcToE_170toInf_PU20bx25.py',
 # miniAodDir+'QCD_bcToE_80to170_PU20bx25.py',
 # miniAodDir+'QCD_bcToE_30to80_PU20bx25.py',
 # miniAodDir+'QCD_bcToE_20to30_PU20bx25.py',
 # miniAodDir+'QCD_MuEnriched_20toInf_PU20bx25.py',
 # miniAodDir+'QCD_MuEnriched_30to50_PU20bx25.py',
 # miniAodDir+'QCD_MuEnriched_50to80_PU20bx25.py',
 # miniAodDir+'QCD_MuEnriched_80to120_PU20bx25.py',
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
