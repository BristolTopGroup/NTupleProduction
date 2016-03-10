from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_amcatnloFXFX'
config.JobType.pyCfgParams = ['isTTbarMC=1']#,'useJECFromFile=1']
config.Data.inputDataset = '/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 8
config.Data.outputDatasetTag = 'TTJets_amcatnloFXFX'
config.Data.ignoreLocality = True
