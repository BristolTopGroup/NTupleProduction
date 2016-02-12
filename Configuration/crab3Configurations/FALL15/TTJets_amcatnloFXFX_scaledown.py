from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_amcatnloFXFX_mtop1695'
config.JobType.pyCfgParams = ['isTTbarMC=1','useJECFromFile=1']
config.Data.inputDataset = '/TTJets_mtop1695_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'TTJets_amcatnloFXFX_mtop1695'
config.Data.ignoreLocality = True
