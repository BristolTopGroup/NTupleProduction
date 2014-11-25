import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import *
from BristolAnalysis.NTupleTools.TopPairElectronPlusJetsSelectionFilter_cfi import *

topPairEPlusJetsSelectionTagging = topPairEPlusJetsSelection.clone( taggingMode = cms.bool(True) )

electronSelectionAnalyzerSequence = cms.Sequence( topPairEPlusJetsSelectionTagging * topPairEPlusJetsSelectionAnalyser )