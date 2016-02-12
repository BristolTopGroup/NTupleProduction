from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'TTJets_PowhegPythia8_mtop1695'
config.JobType.pyCfgParams = ['isTTbarMC=1','useJECFromFile=1']
config.Data.inputDataset = '/TT_TuneCUETP8M1_mtop1695_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outputDatasetTag = 'TTJets_PowhegPythia8_mtop1695'
