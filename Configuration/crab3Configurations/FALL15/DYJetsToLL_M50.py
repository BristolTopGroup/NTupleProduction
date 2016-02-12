from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'DYJetsToLL_M50'
config.JobType.pyCfgParams = ['useJECFromFile=1']
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM' #also with madgraphpythia
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'DYJetsToLL_M50'
