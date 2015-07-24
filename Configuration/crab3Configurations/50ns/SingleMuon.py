from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleMuon'
config.JobType.pyCfgParams = ['isData=1']
config.Data.inputDataset = '/SingleMuon/Run2015B-PromptReco-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 500000
config.Data.publishDataName = 'SingleMuon'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-251252_13TeV_PromptReco_Collisions15_JSON.txt'
