import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import *
from BristolAnalysis.NTupleTools.TopPairMuonPlusJetsSelectionFilter_cfi import *

topPairMuPlusJetsSelectionTagging = topPairMuPlusJetsSelection.clone( taggingMode = cms.bool(True) )

muonSelectionAnalyzerSequence = cms.Sequence( topPairMuPlusJetsSelectionTagging * topPairMuPlusJetsSelectionAnalyser )