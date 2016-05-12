
from crab.base import config
NAME = __file__.split('/')[-1]
NAME = NAME.replace('.py', '')

config.General.requestName = NAME
config.Data.outputDatasetTag = NAME
config.Data.inputDataset = '/SingleElectron/Run2015C_25ns-16Dec2015-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 500000
config.Data.lumiMask = '/hdfs/TopQuarkGroup/run2/json/ReReco_MinusBeamSpotIssue.txt'

