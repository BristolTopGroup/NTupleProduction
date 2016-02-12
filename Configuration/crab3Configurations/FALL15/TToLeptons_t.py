from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TToLeptons_t'
config.JobType.pyCfgParams = ['useJECFromFile=1']
config.Data.inputDataset = '/ST_t-channel_5f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'TToLeptons_t'
