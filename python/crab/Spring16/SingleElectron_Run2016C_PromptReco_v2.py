import crab.base
from copy import deepcopy
NAME = __file__.split('/')[-1].replace('.pyc', '')
NAME = NAME.split('/')[-1].replace('.py', '')
CAMPAIGN = __file__.split('/')[-2]

config = deepcopy(crab.base.config)
config.General.requestName = NAME
config.Data.outputDatasetTag = NAME
config.Data.outLFNDirBase += '/' + CAMPAIGN
config.Data.inputDataset = '/SingleElectron/Run2016C-PromptReco-v2/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 500000
config.JobType.pyCfgParams = ['isData=1']
config.Data.lumiMask = 'TOP_Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON_UnprescaledPaths.txt'

