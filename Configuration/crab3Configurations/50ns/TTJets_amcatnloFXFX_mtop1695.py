from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_amcatnloFXFX_mtop1695'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TTJets_mtop1695_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publishDataName = 'TTJets_amcatnloFXFX_mtop1695'
