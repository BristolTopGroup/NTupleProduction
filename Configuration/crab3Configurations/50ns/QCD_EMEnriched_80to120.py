from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_EMEnriched_80to120'
config.Data.inputDataset = '/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'QCD_EMEnriched_80to120'
