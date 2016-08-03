import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.TopPairMuonPlusJetsSelectionFilter_cfi import topPairMuPlusJetsSelection


topPairMuPlusJetsSelectionTagging = topPairMuPlusJetsSelection.clone(
    taggingMode=True,
)

###############################################################################
# control region 1
###############################################################################
topPairMuPlusJetsQCDSelectionTagging1 = topPairMuPlusJetsSelectionTagging.clone(
    prefix='TopPairMuonPlusJetsQCDSelection3toInf.',
    nonIsolatedMuonSelection1=True,
    goodMuons='goodNonIsoR1Muons',
    cleanedJets='goodJetsMuNonIsoR1Region',
    cleanedBJets='goodBJetsMuNonIsoR1Region',
)
###############################################################################
# control region 2
###############################################################################
topPairMuPlusJetsQCDSelectionTagging2 = topPairMuPlusJetsSelectionTagging.clone(
    prefix='TopPairMuonPlusJetsQCDSelection1p5to3.',
    nonIsolatedMuonSelection2=True,
    goodMuons='goodNonIsoR2Muons',
    cleanedJets='goodJetsMuNonIsoR2Region',
    cleanedBJets='goodBJetsMuNonIsoR2Region',
)
###############################################################################
# analysers for the selections
###############################################################################
from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import topPairMuPlusJetsSelectionAnalyser
from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import topPairMuPlusJetsQCDSelectionAnalyser3toInf
from BristolAnalysis.NTupleTools.SelectionAnalyser_cfi import topPairMuPlusJetsQCDSelectionAnalyser1p5to3

muonSelectionAnalyzerSequence = cms.Sequence(
    topPairMuPlusJetsSelectionTagging *
    topPairMuPlusJetsSelectionAnalyser
)

qcdMuonSelectionAnalyzerSequence = cms.Sequence(
    topPairMuPlusJetsQCDSelectionTagging1 *
    topPairMuPlusJetsQCDSelectionAnalyser3toInf *
    topPairMuPlusJetsQCDSelectionTagging2 *
    topPairMuPlusJetsQCDSelectionAnalyser1p5to3
)
