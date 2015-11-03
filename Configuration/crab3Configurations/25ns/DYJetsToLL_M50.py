from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'DYJetsToLL_M50'
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM' #also with madgraphpythia
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10
config.Data.publishDataName = 'DYJetsToLL_M50'
