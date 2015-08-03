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
#     fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_amcatnlo_25ns.root')
#     fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_PowhegPythia8_50ns.root')
#     fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/SingleMuon.root')
    fileNames = cms.untracked.vstring(
#         'file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_amcatnlo_25ns.root',
        'file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_PowhegPythia8_50ns.root',
#         'file:/hdfs/TopQuarkGroup/run2/miniAOD/SingleMuon.root',
#         '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/162/00000/160C08A3-4227-E511-B829-02163E01259F.root', #SingleMu via xrootd
#         '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/096/00000/22D22D7F-5626-E511-BDE3-02163E011FAB.root',
    )
)

# If you want to run with a json file
# import FWCore.PythonUtilities.LumiList as LumiList
# process.source.lumisToProcess = LumiList.LumiList(filename = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-251252_13TeV_PromptReco_Collisions15_JSON.txt').getVLuminosityBlockRange()
# process.source.lumisToProcess = LumiList.LumiList(filename = '/hdfs/TopQuarkGroup/run2/json/json_DCSONLY_Run2015B.txt').getVLuminosityBlockRange()

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
  process.triggerSequence.remove( process.nTupleTriggerIsoMu24eta2p1 )
  process.triggerSequence.remove( process.nTupleTriggerIsoMu20eta2p1 )
  process.triggerSequence.remove( process.nTupleTriggerEle27WPTightGsf )
  process.triggerSequence.remove( process.nTupleTriggerEle27WPLooseGsf )
else :
  process.makingNTuples.remove( process.makePseudoTop )
  process.nTuples.remove( process.pseudoTopSequence )
  process.nTupleTree.outputCommands.append('drop *_nTuplePFJets_*Gen*_*')
  process.triggerSequence.remove( process.nTupleTriggerIsoMu24eta2p1MC )
  process.triggerSequence.remove( process.nTupleTriggerIsoMu20eta2p1MC )
  process.triggerSequence.remove( process.nTupleTriggerEle27WP75GsfMC )

if not options.isTTbarMC:
  process.makingNTuples.remove( process.ttGenEvent )
  process.selectionCriteriaAnalyzer.genSelectionCriteriaInput = cms.VInputTag()
else:
  process.nTupleGenEventInfo.isTTbarMC = cms.bool( True )
  process.topPairEPlusJetsSelectionTagging.bSelectionInTaggingMode = cms.bool( True )
  process.topPairMuPlusJetsSelectionTagging.bSelectionInTaggingMode = cms.bool( True )

process.TFileService = cms.Service("TFileService",
                           fileName=cms.string('ntuple.root')
                           )

# process.out = cms.OutputModule("PoolOutputModule",
#                 fileName = cms.untracked.string("testOutput.root")
#         )
# process.outpath = cms.EndPath(process.out)


