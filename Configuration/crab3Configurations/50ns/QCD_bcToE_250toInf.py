from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_bcToE_250toInf'
config.Data.inputDataset = '/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'QCD_bcToE_250toInf'
