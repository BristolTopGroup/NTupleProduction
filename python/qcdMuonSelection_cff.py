import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import *
from BristolAnalysis.NTupleTools.TopPairMuonPlusJetsSelectionFilter_cfi import *

topPairMuPlusJetsQCDSelectionTagging1 = topPairMuPlusJetsSelection.clone( taggingMode = cms.bool(True),
																		prefix=cms.untracked.string('TopPairMuonPlusJetsQCDSelection3toInf.'),
																		nonIsolatedMuonSelection1=cms.bool(True) )

topPairMuPlusJetsQCDSelectionTagging2 = topPairMuPlusJetsSelection.clone( taggingMode = cms.bool(True),
																		prefix=cms.untracked.string('TopPairMuonPlusJetsQCDSelection1p5to3.'),
																		nonIsolatedMuonSelection2=cms.bool(True) )

qcdMuonSelectionAnalyzerSequence = cms.Sequence( topPairMuPlusJetsQCDSelectionTagging1 * topPairMuPlusJetsQCDSelectionAnalyser3toInf * 
												topPairMuPlusJetsQCDSelectionTagging2 * topPairMuPlusJetsQCDSelectionAnalyser1p5to3 )
