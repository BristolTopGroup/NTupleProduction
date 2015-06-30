from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_madgraphMLM'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'TTJets_madgraphMLM'
