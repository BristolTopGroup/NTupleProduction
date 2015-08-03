from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_madgraphMLM'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publishDataName = 'TTJets_madgraphMLM'
