from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_bcToE_15to20'
config.Data.inputDataset = '/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'QCD_bcToE_15to20'
