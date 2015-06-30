from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TT_Pythia8_PU20bx25_mass1755'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TT_mass1755_Tune4C_13TeV-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'TT_Pythia8_PU20bx25_mass1755'
