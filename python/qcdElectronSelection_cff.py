import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import *
from BristolAnalysis.NTupleTools.TopPairElectronPlusJetsSelectionFilter_cfi import *

topPairEPlusJetsConversionSelectionTagging = topPairEPlusJetsSelection.clone( taggingMode = cms.bool(True),
																		prefix=cms.untracked.string('TopPairElectronPlusJetsConversionSelection.'),
																		invertedConversionSelection=cms.bool(True) )

topPairEPlusJetsQCDSelectionTagging = topPairEPlusJetsSelection.clone( taggingMode = cms.bool(True),
																		prefix=cms.untracked.string('TopPairElectronPlusJetsQCDSelection.'),
																		nonIsolatedElectronSelection=cms.bool(True) )

qcdElectronSelectionAnalyzerSequence = cms.Sequence( topPairEPlusJetsQCDSelectionTagging * topPairEPlusJetsQCDSelectionAnalyser * 
													 topPairEPlusJetsConversionSelectionTagging * topPairEPlusJetsConversionSelectionAnalyser )
