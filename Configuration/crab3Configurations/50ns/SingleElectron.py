from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleElectron'
config.JobType.pyCfgParams = ['isData=1']
config.Data.inputDataset = '/SingleElectron/Run2015B-PromptReco-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 100000
config.Data.publishDataName = 'SingleElectron'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-251252_13TeV_PromptReco_Collisions15_JSON.txt'
