from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleElectron_16Dec2015_RunC'
config.JobType.pyCfgParams = ['isData=1']#,'useJECFromFile=1']
config.Data.inputDataset = '/SingleElectron/Run2015C_25ns-16Dec2015-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 500000
config.Data.outputDatasetTag = 'SingleElectron_16Dec2015_RunC'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/ReReco_MinusBeamSpotIssue.txt'
