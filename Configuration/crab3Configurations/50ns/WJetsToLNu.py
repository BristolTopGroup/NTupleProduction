from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'WJetsToLNu'
config.Data.inputDataset = '/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publishDataName = 'WJetsToLNu'
config.Data.ignoreLocality = True
