import crab.base
from copy import deepcopy
NAME = __file__.split('/')[-1].replace('.pyc', '')
NAME = NAME.split('/')[-1].replace('.py', '')
CAMPAIGN = __file__.split('/')[-2]

config = deepcopy(crab.base.config)
config.General.requestName = NAME
config.Data.outputDatasetTag = NAME
config.Data.outLFNDirBase += '/' + CAMPAIGN
config.Data.inputDataset = '/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10


