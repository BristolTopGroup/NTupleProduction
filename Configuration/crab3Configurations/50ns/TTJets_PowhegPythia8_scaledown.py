from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_PowhegPythia8_scaledown'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.publishDataName = 'TTJets_PowhegPythia8_scaledown'
config.Data.ignoreLocality = True
