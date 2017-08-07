import FWCore.ParameterSet.Config as cms

selectionCriteriaAnalyzer = cms.EDFilter(
    'SelectionCriteriaAnalyzer',
    # Specify input collections
    offlineSelectionCriteriaInput=cms.VInputTag(
        cms.InputTag('topPairMuPlusJetsSelectionTagging',
                     'TopPairMuonPlusJetsSelection.FullSelectionNoB', 'Ntuples'),
        cms.InputTag('topPairEPlusJetsSelectionTagging',
                     'TopPairElectronPlusJetsSelection.FullSelectionNoB', 'Ntuples'),
        cms.InputTag('topPairMuPlusJetsQCDSelectionTagging2',
                     'TopPairMuonPlusJetsQCDSelection1p5to3.FullSelectionNoB', 'Ntuples'),
        cms.InputTag('topPairMuPlusJetsQCDSelectionTagging1',
                     'TopPairMuonPlusJetsQCDSelection3toInf.FullSelectionNoB', 'Ntuples'),
        cms.InputTag('topPairEPlusJetsQCDSelectionTagging',
                     'TopPairElectronPlusJetsQCDSelection.FullSelectionNoB', 'Ntuples'),
        cms.InputTag('topPairEPlusJetsConversionSelectionTagging',
                     'TopPairElectronPlusJetsConversionSelection.FullSelectionNoB', 'Ntuples'),
    ),
    genSelectionCriteriaInput=cms.VInputTag(
        # cms.InputTag('ttFullHadronicFilter',       	 '', 'Ntuples'),
        # cms.InputTag('ttFullLeptonicEEFilter',     	 '', 'Ntuples'),
        # cms.InputTag('ttFullLeptonicEMuFilter',    	 '', 'Ntuples'),
        # cms.InputTag('ttFullLeptonicETauFilter',     '', 'Ntuples'),
        # cms.InputTag('ttFullLeptonicFilter',       	 '', 'Ntuples'),
        # cms.InputTag('ttFullLeptonicMuMuFilter',     '', 'Ntuples'),
        # cms.InputTag('ttFullLeptonicMuTauFilter',    '', 'Ntuples'),
        # cms.InputTag('ttFullLeptonicTauTauFilter',   '', 'Ntuples'),
        # cms.InputTag('ttSemiLeptonicTauFilter',    	 '', 'Ntuples'),
        # Only interested in these two decay channels for filtering
        # events
        cms.InputTag('ttSemiLeptonicMuonFilter',     '', 'Ntuples'),
        cms.InputTag('ttSemiLeptonicElectronFilter', '', 'Ntuples'),
    ),
    particleLevelLeptonSelectionInput=cms.InputTag('genLeptonFilter', 'Event.OneParticleLepton', 'Ntuples'),
    isTTbarMC = cms.bool(False),
)
