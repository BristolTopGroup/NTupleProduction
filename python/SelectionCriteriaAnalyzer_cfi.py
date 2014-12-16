import FWCore.ParameterSet.Config as cms

selectionCriteriaAnalyzer = cms.EDFilter('SelectionCriteriaAnalyzer',
    # Specify input collections
    selectionCriteriaInput      = cms.VInputTag(
                                     cms.InputTag('topPairMuPlusJetsSelectionTagging', 'TopPairMuonPlusJetsSelection.FullSelection', 'Ntuples'),
                                     cms.InputTag('topPairEPlusJetsSelectionTagging', 'TopPairElectronPlusJetsSelection.FullSelection', 'Ntuples'),
            ),
)

