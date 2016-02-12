from BristolAnalysis.NTupleTools.commonConfig import config

config.General.requestName = 'SingleMuon_16Dec2015'
config.JobType.pyCfgParams = ['isData=1','useJECFromFile=1']
config.Data.inputDataset = '/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 500000
config.Data.outputDatasetTag = 'SingleMuon_16Dec2015'
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions15/13TeV/Reprocessing/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON.txt'

