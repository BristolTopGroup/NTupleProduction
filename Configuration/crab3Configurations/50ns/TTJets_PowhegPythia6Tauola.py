from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_PowhegPythia6Tauola'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TT_TuneZ2star_13TeV-powheg-pythia6-tauola/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 8
config.Data.publishDataName = 'TTJets_PowhegPythia6Tauola'
