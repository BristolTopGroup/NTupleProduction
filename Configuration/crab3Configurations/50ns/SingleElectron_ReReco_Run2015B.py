from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleElectron_Rereco_Run2015B'
config.JobType.pyCfgParams = ['isData=1','isRereco=1']
config.Data.inputDataset = '/SingleElectron/Run2015B-17Jul2015-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 250000
config.Data.publishDataName = 'SingleElectron_Rereco_Run2015B'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-255031_13TeV_PromptReco_Collisions15_50ns_JSON_v2.txt'
