import FWCore.ParameterSet.Config as cms

# Define the CMSSW process
process = cms.Process("Ntuples")

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Message Logger settings
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Set the process options -- Display summary at the end, enable unscheduled execution
process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False),
)

# print event content
process.printEventContent = cms.EDAnalyzer("EventContentAnalyzer")


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
          # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/244/00000/084C9A66-9227-E511-91E0-02163E0133F0.root',
          # 'root://xrootd.unl.edu//store/data/Run2015B/SingleMuon/MINIAOD/17Jul2015-v1/30000/16B50792-172E-E511-B0C8-0025905C43EC.root',
          # '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/883/00000/00CD59FD-2B2D-E511-8DB2-02163E01267F.root'
#         '/store/data/Run2015B/SingleMuon/MINIAOD/PromptReco-v1/000/251/162/00000/160C08A3-4227-E511-B829-02163E01259F.root', #SingleMu via xrootd
#         '/store/data/Run2015B/SingleElectron/MINIAOD/PromptReco-v1/000/251/096/00000/22D22D7F-5626-E511-BDE3-02163E011FAB.root',
    )
)

# If you want to run with a json file
# import FWCore.PythonUtilities.LumiList as LumiList
# process.source.lumisToProcess = LumiList.LumiList(filename = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-251252_13TeV_PromptReco_Collisions15_JSON.txt').getVLuminosityBlockRange()
# process.source.lumisToProcess = LumiList.LumiList(filename = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-251883_13TeV_PromptReco_Collisions15_JSON_v2.txt').getVLuminosityBlockRange()

# Use to skip events e.g. to reach a problematic event quickly
# process.source.skipEvents = cms.untracked.uint32(4099)

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

# Rerun HBHE filter
from BristolAnalysis.NTupleTools.metFilters_cfi import *
setupMETFilters( process, cms )

# Custom JEC
from BristolAnalysis.NTupleTools.Jets_Setup_cff import setup_jets
setup_jets(process, cms, options)

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
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

from BristolAnalysis.NTupleTools.NTupler_cff import *
setup_ntupler(process, cms )

process.makingNTuples = cms.Path(
  process.HBHEFilterRerun *
  process.egmGsfElectronIDSequence *
  process.electronSelectionAnalyzerSequence *
  process.muonSelectionAnalyzerSequence *  
  process.qcdMuonSelectionAnalyzerSequence *
  process.qcdElectronSelectionAnalyzerSequence *
  process.ttGenEvent *
  process.selectionCriteriaAnalyzer *
  process.makePseudoTop *
  process.printEventContent *
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
  process.nTuples.remove( process.nTupleGenMET )
  process.nTuples.remove( process.nTupleGenJets )
  process.nTuples.remove( process.nTupleGenEventInfo )
  process.nTupleTree.outputCommands.append('drop *_nTuplePFJets_*Gen*_*')
  process.triggerSequence.remove( process.nTupleTriggerIsoMu24eta2p1MC )
  process.triggerSequence.remove( process.nTupleTriggerIsoMu20eta2p1MC )
  process.triggerSequence.remove( process.nTupleTriggerEle27WP75GsfMC )

if options.isData and options.isRereco:
  process.nTupleEvent.metFiltersInputTag = cms.InputTag('TriggerResults','','PAT')

if not options.isTTbarMC:
  process.makingNTuples.remove( process.ttGenEvent )
  process.selectionCriteriaAnalyzer.genSelectionCriteriaInput = cms.VInputTag()
else:
  process.nTupleGenEventInfo.isTTbarMC = cms.bool( True )
  process.topPairEPlusJetsSelectionTagging.bSelectionInTaggingMode = cms.bool( True )
  process.topPairMuPlusJetsSelectionTagging.bSelectionInTaggingMode = cms.bool( True )

if not options.printEventContent:
    process.makingNTuples.remove(process.printEventContent)

process.TFileService = cms.Service("TFileService",
                           fileName=cms.string('ntuple.root')
                           )

# process.out = cms.OutputModule("PoolOutputModule",
#                 fileName = cms.untracked.string("testOutput.root")
#         )
# process.outpath = cms.EndPath(process.out)


