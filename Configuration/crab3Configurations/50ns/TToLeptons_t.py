from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TToLeptons_t'
config.Data.inputDataset = '/ST_t-channel_5f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'TToLeptons_t'
