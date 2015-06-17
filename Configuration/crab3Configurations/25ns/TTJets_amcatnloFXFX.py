from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_amcatnloFXFX'
config.JobType.pyCfgParams = ['isTTbarMC=1']
config.Data.inputDataset = '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM'
config.Data.unitsPerJob = 8
config.Data.publishDataName = 'TTJets_amcatnloFXFX'
config.Data.ignoreLocality = True
