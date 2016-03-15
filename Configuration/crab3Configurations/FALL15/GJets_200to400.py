from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'GJets_200to400'
# config.JobType.pyCfgParams = ['useJECFromFile=1']
config.Data.inputDataset = '/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.outputDatasetTag = 'GJets_200to400'
