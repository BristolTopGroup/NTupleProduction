import FWCore.ParameterSet.Config as cms

process = cms.Process("Ntuples")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('PHYS14_25_V3::All')

## Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/storage/ec6821/NTupleProd/CMSSW_7_3_0/src/TT_pythia8_PHYS14.root')
    # fileNames = cms.untracked.vstring('file:/storage/ec6821/NTupleProd/CMSSW_7_2_3/src/TT_madgraph_PHYS14.root')
    # fileNames = cms.untracked.vstring('file:/home/ec6821/CMSSW_7_2_2/src/WJetsPhys14.root')
)
# Use to skip events e.g. to reach a problematic event quickly
# process.source.skipEvents = cms.untracked.uint32(40960)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.FwkReport.reportEvery = 5000

# Get options from command line
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
from BristolAnalysis.NTupleTools.NTupleOptions_cff import *
getOptions( options )

# Load the selection filters and the selection analyzers
process.load( 'BristolAnalysis.NTupleTools.muonSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.electronSelection_cff')

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
  process.electronSelectionAnalyzerSequence *
  process.muonSelectionAnalyzerSequence *  
  process.selectionCriteriaAnalyzer *
  process.ttGenEvent *
  process.nTuples *
  process.nTupleTree
  )

process.nTupleTree.outputCommands.append( 'keep uint*_topPairMuPlusJetsSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairEPlusJetsSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairMuPlusJetsSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairEPlusJetsSelectionTagging_*_*' )


if options.selectionInTaggingMode:
  process.makingNTuples.remove( process.topPairMuPlusJetsSelection )

if not options.isTTbarMC:
  process.makingNTuples.remove( process.ttGenEvent )
else:
  process.nTupleGenEventInfo.isTTbarMC = cms.bool( True )


process.TFileService = cms.Service("TFileService",
                           fileName=cms.string('ntuple.root')
                           )

# process.out = cms.OutputModule("PoolOutputModule",
#                 fileName = cms.untracked.string("testOutput.root")
#         )
# process.outpath = cms.EndPath(process.out)


