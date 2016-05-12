from crab.base import config
NAME = __file__.split('/')[-1].replace('.py', '')

config.General.requestName = NAME
config.Data.outputDatasetTag = NAME
config.Data.inputDataset = '/TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/MINIAODSIM'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.outLFNDirBase += '/' + __file__.split('/')[-2]
config.JobType.pyCfgParams = ['isTTbarMC=1']

