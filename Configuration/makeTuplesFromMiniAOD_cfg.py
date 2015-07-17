import FWCore.ParameterSet.Config as cms

process = cms.Process("Ntuples")

# If you would like to change the Global Tag e.g. for JEC
# process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
# Most recent JEC not available in V3
# process.GlobalTag.globaltag = cms.string('PHYS14_25_V3::All')
# process.GlobalTag.globaltag = cms.string('PHYS14_25_V2::All')
# process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

## Source
process.source = cms.Source("PoolSource",
    # fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_amcatnlo_25ns.root')
    fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_PowhegPythia8_50ns.root')
    # fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/SingleElectron.root')
    # fileNames = cms.untracked.vstring(
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/162/00000/160C08A3-4227-E511-B829-02163E01259F.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/164/00000/544E58CD-A226-E511-834E-02163E0134D6.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/167/00000/EE9594B8-A826-E511-A18B-02163E011A7D.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/168/00000/4E8E390B-EA26-E511-9EDA-02163E013567.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/168/00000/60FF8405-EA26-E511-A892-02163E01387D.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/244/00000/68275270-7C27-E511-B1F0-02163E011A46.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/244/00000/B6304C6F-7C27-E511-9C77-02163E01250E.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/251/00000/EEBF2AF4-8D27-E511-91F7-02163E014527.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/252/00000/0438FA5A-A127-E511-BA6F-02163E013414.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/252/00000/7E4A8F57-A127-E511-9BF5-02163E014629.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/493/00000/6A4D2AB2-E828-E511-B82B-02163E0121E9.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/497/00000/668C5130-FE28-E511-8F78-02163E0133B0.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/498/00000/50CD6709-0C29-E511-8F8B-02163E0134FD.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/499/00000/402D1C6D-1729-E511-ABF5-02163E011DFF.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/500/00000/62310AED-3729-E511-AC61-02163E012712.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/500/00000/A2A303EC-3729-E511-9ECE-02163E011A29.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/521/00000/425B1189-6729-E511-AF38-02163E013728.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/522/00000/F6930521-5D29-E511-B517-02163E011D37.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/548/00000/44CE0650-EF29-E511-BA0D-02163E012601.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/560/00000/A886DB09-E029-E511-8A06-02163E0125C8.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/561/00000/F6A7CE0F-132A-E511-A423-02163E011D88.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/562/00000/7CC342FD-A02A-E511-BE8D-02163E01182A.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/562/00000/96297F29-862A-E511-85C1-02163E013901.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/562/00000/C6637305-A12A-E511-AD71-02163E0138F6.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/562/00000/E0561625-7C2A-E511-9016-02163E0133D1.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/562/00000/EA8BA8F7-A02A-E511-A45F-02163E013473.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/604/00000/1606A3BF-972A-E511-86A7-02163E013515.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/612/00000/7A0CE8FF-A72A-E511-B7DC-02163E011D1C.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/638/00000/10C07DF0-FA2A-E511-846A-02163E01474A.root',
    # '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/642/00000/D20F8A8A-DE2A-E511-9D16-02163E0133FF.root',

      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/096/00000/22D22D7F-5626-E511-BDE3-02163E011FAB.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/161/00000/7019DC27-9C26-E511-84FF-02163E011CC2.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/162/00000/9CC606D8-4127-E511-8F35-02163E013830.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/163/00000/9C435096-9F26-E511-A1D7-02163E012AB6.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/164/00000/4633CC68-A326-E511-95D0-02163E0124EA.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/167/00000/E661FBF2-A726-E511-8B8B-02163E01207C.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/168/00000/FCB6CB61-BC26-E511-8858-02163E01375B.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/244/00000/084C9A66-9227-E511-91E0-02163E0133F0.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/244/00000/12EE24E2-8F27-E511-80D1-02163E013793.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/251/00000/3A0E6309-8827-E511-B96D-02163E013432.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/252/00000/36D5A4A8-A227-E511-9AAA-02163E0135F3.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/252/00000/6258DF96-A227-E511-BE8A-02163E01259F.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/491/00000/4A5A5D00-C628-E511-ACC7-02163E01414A.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/493/00000/0C69AF3D-CF28-E511-B56A-02163E01414A.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/497/00000/607EA0EA-E028-E511-BD54-02163E0133FF.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/498/00000/8064CCF6-ED28-E511-87D2-02163E014437.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/499/00000/70310B47-F728-E511-B2EF-02163E0118A2.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/500/00000/0273C876-0E29-E511-8B38-02163E012712.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/521/00000/D28AB765-6629-E511-8AAD-02163E0133D1.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/522/00000/805EB9CD-6129-E511-BF1C-02163E0129A3.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/548/00000/B6D08898-232A-E511-A833-02163E011DDE.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/560/00000/BA599BB8-E129-E511-B26A-02163E0134CC.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/561/00000/5ACDA1DE-FB29-E511-8D8C-02163E0133B5.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/561/00000/CA80E14E-1E2A-E511-8C7D-02163E0122C2.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/30DDF910-5E2A-E511-9F4D-02163E01206A.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/3CE07240-742A-E511-BA88-02163E01258B.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/5CF006D1-602A-E511-95CE-02163E0126E1.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/8EE9BBAA-7E2A-E511-AEF7-02163E0143C0.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/B41B8802-672A-E511-A9EA-02163E012787.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/DCC900B5-972A-E511-9785-02163E012283.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/F0A7C9F3-6B2A-E511-A73B-02163E0126A0.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/562/00000/FE5AD795-6E2A-E511-9C40-02163E012787.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/604/00000/AE22AF42-902A-E511-8A22-02163E012B30.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/612/00000/50DA7894-932A-E511-801E-02163E0136A2.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/628/00000/40EF63A0-B52A-E511-8B57-02163E0133F0.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/638/00000/0CDDB666-E72A-E511-9BFD-02163E011DE5.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/638/00000/B2FC1038-372B-E511-AA94-02163E013481.root',
      # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/642/00000/2C622272-D02A-E511-9F20-02163E013645.root',
    # )
)

# If you want to run with a json file
# import FWCore.PythonUtilities.LumiList as LumiList
# process.source.lumisToProcess = LumiList.LumiList(filename = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-251252_13TeV_PromptReco_Collisions15_JSON.txt').getVLuminosityBlockRange()

# Use to skip events e.g. to reach a problematic event quickly
# process.source.skipEvents = cms.untracked.uint32(4099)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Get options from command line
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
from BristolAnalysis.NTupleTools.NTupleOptions_cff import *
getOptions( options )

# TT Gen Event configuration
from BristolAnalysis.NTupleTools.ttGenConfig_cff import *
setupTTGenEvent( process, cms )

# Particle level definitions
from BristolAnalysis.NTupleTools.pseudoTopConfig_cff import *
setupPseudoTop( process, cms )

# Electron VID
from BristolAnalysis.NTupleTools.ElectronID_cff import *
setup_electronID( process, cms )

# Load the selection filters and the selection analyzers
process.load( 'BristolAnalysis.NTupleTools.muonSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.qcdMuonSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.qcdElectronSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.electronSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.SelectionCriteriaAnalyzer_cfi')

if options.tagAndProbe:
  process.topPairEPlusJetsSelection.tagAndProbeStudies = cms.bool( True )
  process.topPairEPlusJetsSelectionTagging.tagAndProbeStudies = cms.bool( True )
  process.topPairEPlusJetsSelection.jetSelectionInTaggingMode = cms.bool( True )
  process.topPairEPlusJetsSelectionTagging.jetSelectionInTaggingMode = cms.bool( True )

 
## Maximum Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

from BristolAnalysis.NTupleTools.NTupler_cff import *
setup_ntupler(process, cms )

process.makingNTuples = cms.Path(
  process.egmGsfElectronIDSequence *
  process.electronSelectionAnalyzerSequence *
  process.muonSelectionAnalyzerSequence *  
  process.qcdMuonSelectionAnalyzerSequence *
  process.qcdElectronSelectionAnalyzerSequence *
  process.ttGenEvent *
  process.selectionCriteriaAnalyzer *
  process.makePseudoTop *
  process.nTuples *
  process.nTupleTree
  )

process.nTupleTree.outputCommands.append( 'keep uint*_topPairMuPlusJetsSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairMuPlusJetsQCDSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairEPlusJetsSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairEPlusJetsQCDSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairEPlusJetsConversionSelectionTagging_*_*' )

process.nTupleTree.outputCommands.append( 'keep bool_topPairMuPlusJetsSelectionTagging_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairMuPlusJetsQCDSelectionTagging_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairEPlusJetsSelectionTagging_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairEPlusJetsQCDSelectionTagging_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairEPlusJetsConversionSelectionTagging_*FullSelection*_*' )

if not options.isData:
  process.makingNTuples.remove( process.triggerSequence )
else :
  process.makingNTuples.remove( process.makePseudoTop )
  process.nTuples.remove( process.pseudoTopSequence )
  process.nTupleTree.outputCommands.append('drop *_nTuplePFJets_*Gen*_*')
  
if not options.isTTbarMC:
  process.makingNTuples.remove( process.ttGenEvent )
  process.selectionCriteriaAnalyzer.genSelectionCriteriaInput = cms.VInputTag()  
else:
  process.nTupleGenEventInfo.isTTbarMC = cms.bool( True )

process.TFileService = cms.Service("TFileService",
                           fileName=cms.string('ntuple.root')
                           )

# process.out = cms.OutputModule("PoolOutputModule",
#                 fileName = cms.untracked.string("testOutput.root")
#         )
# process.outpath = cms.EndPath(process.out)


