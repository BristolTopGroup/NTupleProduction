from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleElectron'
config.Data.inputDataset = '/SingleElectron/Run2015B-PromptReco-v1/MINIAOD'
config.Data.unitsPerJob = 1
config.Data.publishDataName = 'SingleElectron'
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/json_DCSONLY_Run2015B.txt'
