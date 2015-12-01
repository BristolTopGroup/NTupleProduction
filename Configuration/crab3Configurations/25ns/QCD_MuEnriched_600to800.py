from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_MuEnriched_600to800'
config.Data.inputDataset = '/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v4/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'QCD_MuEnriched_600to800'
