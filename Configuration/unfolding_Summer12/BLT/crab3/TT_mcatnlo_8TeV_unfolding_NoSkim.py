from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferOutputs = True
config.General.requestName = 'TT_8TeV_mcatnlo_BLTUnfold_NoSkim'
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

config.JobType.pyCfgParams = ['useData=0', 'dataType=TTJets', 'isTTbarMC=1', 'skim=NoSkim', 'storePDFWeights=0', 'applyType0METcorrection=1', 'applySysShiftCorrection=1', 'isMCatNLO=1']
config.section_('Data')
config.Data.inputDataset = '/TT_8TeV-mcatnlo/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM'
config.Data.unitsPerJob = 3
config.Data.splitting = 'FileBased'
config.section_('User')
config.section_('Site')
config.Site.storageSite = 'T2_UK_SGrid_Bristol'
