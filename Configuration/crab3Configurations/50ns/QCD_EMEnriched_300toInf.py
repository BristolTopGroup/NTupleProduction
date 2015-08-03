from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_EMEnriched_300toInf'
config.Data.inputDataset = '/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publishDataName = 'QCD_EMEnriched_300toInf'
