from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleMuon_16Dec2015_RunD'
config.JobType.pyCfgParams = ['isData=1']#,'useJECFromFile=1']
config.Data.inputDataset = '/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 500000
config.Data.outputDatasetTag = 'SingleMuon_16Dec2015_RunD'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/ReReco_MinusBeamSpotIssue.txt'

