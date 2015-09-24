from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleMuon_Rereco'
config.JobType.pyCfgParams = ['isData=1','isRereco=1']
config.Data.inputDataset = '/SingleMuon/Run2015B-17Jul2015-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 250000
config.Data.publishDataName = 'SingleMuon_Rereco'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt'
