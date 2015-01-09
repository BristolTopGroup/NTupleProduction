import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import *
from BristolAnalysis.NTupleTools.TopPairMuonPlusJetsSelectionFilter_cfi import *

topPairMuPlusJetsQCDSelectionTagging = topPairMuPlusJetsSelection.clone( taggingMode = cms.bool(True),
																		prefix=cms.untracked.string('TopPairMuonPlusJetsQCDSelection.'),
																		nonIsolatedMuonSelection=cms.bool(True) )

qcdMuonSelectionAnalyzerSequence = cms.Sequence( topPairMuPlusJetsQCDSelectionTagging * topPairMuPlusJetsQCDSelectionAnalyser )