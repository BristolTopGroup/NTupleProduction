from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_MuEnriched_600to800'
config.Data.inputDataset = '/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publishDataName = 'QCD_MuEnriched_600to800'
