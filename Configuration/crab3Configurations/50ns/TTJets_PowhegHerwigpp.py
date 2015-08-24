from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_PowhegHerwigpp'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publishDataName = 'TTJets_PowhegHerwigpp'
