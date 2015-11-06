from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'GJets_15toInf'
config.Data.inputDataset = '/GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'GJets_15toInf'
