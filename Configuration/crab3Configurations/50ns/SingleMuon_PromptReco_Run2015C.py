from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleMuon_PromptReco_Run2015C'
config.JobType.pyCfgParams = ['isData=1']
config.Data.inputDataset = '/SingleMuon/Run2015C-PromptReco-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 250000
config.Data.publishDataName = 'SingleMuon_PromptReco_Run2015C'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt'
