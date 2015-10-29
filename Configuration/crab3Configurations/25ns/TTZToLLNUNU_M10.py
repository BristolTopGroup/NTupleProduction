from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTZToLLNuNu_M-10'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'TTZToLLNuNu_M-10'
