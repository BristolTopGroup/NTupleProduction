from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'QCD_EMEnriched_15to20'
config.JobType.pyCfgParams = ['useJECFromFile=1']
config.Data.inputDataset = '/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'QCD_EMEnriched_15to20'
