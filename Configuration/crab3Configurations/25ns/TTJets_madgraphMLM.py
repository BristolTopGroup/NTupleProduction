from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_madgraphMLM'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'TTJets_madgraphMLM'
