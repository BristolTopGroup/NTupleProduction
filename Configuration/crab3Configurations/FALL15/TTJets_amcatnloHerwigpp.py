from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_amcatnloHerwigpp'
config.JobType.pyCfgParams = ['isTTbarMC=1']#,'useJECFromFile=1']
config.Data.inputDataset = '/TT_TuneEE5C_13TeV-amcatnlo-herwigpp/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outputDatasetTag = 'TTJets_amcatnloHerwigpp'
