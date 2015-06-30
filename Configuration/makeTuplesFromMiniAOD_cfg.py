import FWCore.ParameterSet.Config as cms

process = cms.Process("Ntuples")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
# Most recent JEC not available in V3
# process.GlobalTag.globaltag = cms.string('PHYS14_25_V3::All')
process.GlobalTag.globaltag = cms.string('PHYS14_25_V2::All')

process.load('JetMETCorrections.Configuration.DefaultJEC_cff')

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_amcatnlo_25ns.root')  
    # fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_pythia8_PHYS14.root')
    # fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_madgraph_PHYS14.root')
    # fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/WJets_PHYS14.root')
)
# Use to skip events e.g. to reach a problematic event quickly
# process.source.skipEvents = cms.untracked.uint32(40960)

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


