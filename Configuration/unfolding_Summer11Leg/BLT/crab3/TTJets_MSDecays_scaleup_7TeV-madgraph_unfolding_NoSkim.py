from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'TTJets_scaleup_7TeV_madgraph_BLTUnfold_NoSkim_TEST'
config.General.transferLogs = True
config.section_('JobType')
config.JobType.psetName = 'BristolAnalysis/NTupleTools/test/unfoldingBLT_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = [
'BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2011Full.root',
'BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2011Full_64600mb_June2014.root',
'BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2011Full_71400mb_June2014.root',
'BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2011Full_central_68000mb_June2014.root',
'BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2012Full.root',
'BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2012Full_65835mb.root',
'BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2012Full_72765mb.root',
'BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Default2011.root',
'BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Default2012.root',
'BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_DefaultSummer11Leg.root',
'BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Summer2012.root',
'BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011.root',
'BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011_truth.root',
'BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011_truth_finebin.root',
'BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011_truth_finebin_64600microbarn.root',
'BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011_truth_finebin_68000microbarn.root',
'BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011_truth_finebin_71400microbarn.root',
'BristolAnalysis/NTupleTools/data/PileUp/Weight3D_Fall11.root',
'BristolAnalysis/NTupleTools/data/PileUp/Weight3D_Summer11.root',
'BristolAnalysis/NTupleTools/data/ScaleFactors/MuonEfficiencies_SF_2011_53X_DataMC.root',
'BristolAnalysis/NTupleTools/data/ScaleFactors/hadronLegEfficiencies_electron.root',
'BristolAnalysis/NTupleTools/data/ScaleFactors/scaleFactors_electron_id_iso.root',
'BristolAnalysis/NTupleTools/data/ScaleFactors/scaleFactors_electron_trigger.root'
]

config.JobType.pyCfgParams = ['useData=0', 'dataType=TTJets-scaleup', 'isTTbarMC=1', 'skim=NoSkim', 'CMSSW=53X', 'centreOfMassEnergy=7', 'storePDFWeights=0', 'applyType0METcorrection=1', 'applySysShiftCorrection=1']
config.section_('Data')
config.Data.inputDataset = '/TTJets_MSDecays_scaleup_TuneZ2star_7TeV-madgraph-tauola/Summer11LegDR-PU_S13_START53_LV6-v2/AODSIM'
config.Data.unitsPerJob = 3
config.Data.splitting = 'FileBased'
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_UK_SGrid_Bristol'
