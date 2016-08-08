import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import *
from BristolAnalysis.NTupleTools.TopPairElectronPlusJetsSelectionFilter_cfi import topPairEPlusJetsSelection

topPairEPlusJetsSelectionTagging = topPairEPlusJetsSelection.clone(
    taggingMode=True,
)

topPairEPlusJetsConversionSelectionTagging = topPairEPlusJetsSelectionTagging.clone(
    prefix='TopPairElectronPlusJetsConversionSelection.',
    invertedConversionSelection=True,
    goodElectrons='goodConversionElectrons',
    cleanedJets='goodJetsEConversionRegion',
    cleanedBJets='goodBJetsEConversionRegion',
)

topPairEPlusJetsQCDSelectionTagging = topPairEPlusJetsSelectionTagging.clone(
    prefix='TopPairElectronPlusJetsQCDSelection.',
    nonIsolatedElectronSelection=True,
    goodElectrons='goodNonIsoElectrons',
    cleanedJets='goodJetsENonIsoRegion',
    cleanedBJets='goodBJetsENonIsoRegion',
)
###############################################################################
# analysers for the selections
###############################################################################
from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import topPairEPlusJetsSelectionAnalyser
from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import topPairEPlusJetsConversionSelectionAnalyser
from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import topPairEPlusJetsQCDSelectionAnalyser

electronSelectionAnalyzerSequence = cms.Sequence(
    topPairEPlusJetsSelectionTagging * topPairEPlusJetsSelectionAnalyser)

qcdElectronSelectionAnalyzerSequence = cms.Sequence(
    topPairEPlusJetsQCDSelectionTagging *
    topPairEPlusJetsQCDSelectionAnalyser *
    topPairEPlusJetsConversionSelectionTagging *
    topPairEPlusJetsConversionSelectionAnalyser
)