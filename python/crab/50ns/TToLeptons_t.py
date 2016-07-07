import crab.base
from copy import deepcopy
NAME = __file__.split('/')[-1].replace('.pyc', '')
NAME = NAME.split('/')[-1].replace('.py', '')
CAMPAIGN = __file__.split('/')[-2]

config = deepcopy(crab.base.config)
config.General.requestName = NAME
config.Data.outputDatasetTag = NAME
config.Data.outLFNDirBase += '/' + CAMPAIGN
config.Data.inputDataset = '/ST_t-channel_5f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10


