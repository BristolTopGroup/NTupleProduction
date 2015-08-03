from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'GJets_15to6000'
config.Data.inputDataset = '/GJet_Pt-15To6000_TuneCUETP8M1-Flat_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'GJets_15to6000'
