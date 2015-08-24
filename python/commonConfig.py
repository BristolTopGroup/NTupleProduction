from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
# config.General.requestName = 'TTJets_Madgraph_PU20bx25'
config.General.workArea = 'workdirCrab/v28/2015-08-23'
config.General.transferOutputs = True
# config.General.transferLogs = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'BristolAnalysis/NTupleTools/Configuration/makeTuplesFromMiniAOD_cfg.py'
# config.JobType.pyCfgParams = ['isTTbarMC=1']
config.JobType.allowUndistributedCMSSW = True
config.JobType.inputFiles = ['BristolAnalysis/NTupleTools/data/BTagSF/CSVv2.csv', 'Summer15_50nsV4_DATA.db', 'Summer15_50nsV4_MC.db']

config.section_("Data")
# config.Data.inputDataset = '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM'
config.Data.inputDBS = 'global'
# config.Data.splitting = 'FileBased'
# config.Data.unitsPerJob = 10
config.Data.outLFNDirBase = '/store/user/ejclemen/'
config.Data.publication = True
# config.Data.publishDataName = 'TTJets_Madgraph_PU20bx25'
# config.Data.ignoreLocality = True

config.section_("Site")
config.Site.storageSite = 'T2_UK_SGrid_Bristol'
