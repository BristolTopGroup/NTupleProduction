from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'T_tw'
# config.JobType.pyCfgParams = ['useJECFromFile=1']
config.Data.inputDataset = '/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'T_tw'
