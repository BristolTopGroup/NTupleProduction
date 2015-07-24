from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_bcToE_20to30'
config.Data.inputDataset = '/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'QCD_bcToE_20to30'
