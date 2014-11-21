from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_Madgraph_PU20bx25'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'TTJets_Madgraph_PU20bx25'
