from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleElectron_PromptReco'
config.JobType.pyCfgParams = ['isData=1']
config.Data.inputDataset = '/SingleElectron/Run2015C-PromptReco-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 250000
config.Data.publishDataName = 'SingleElectron_PromptReco'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt'
