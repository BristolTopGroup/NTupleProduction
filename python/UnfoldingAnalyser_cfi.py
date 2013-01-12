import FWCore.ParameterSet.Config as cms

unfolding_MET_analyser_electron_channel = cms.EDAnalyzer("UnfoldingAnalyser",
    PUWeightInput=cms.InputTag('eventWeightPU'),
    BtagWeightInput=cms.InputTag('eventWeightBtag'),
    genMetInput=cms.InputTag('genMetTrue'),
    recoMetInput=cms.InputTag('patType1CorrectedPFMet'),
    selectionFlagInput=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.FullSelection', 'PAT'),
    isFullyHadronicTtbarFlag=cms.InputTag('ttFullHadronicFilter'),
    isDiLeptonicTtbarFlag=cms.InputTag('ttFullLeptonicFilter'),
    isSemiLeptonicElectronFlag=cms.InputTag('ttSemiLeptonicElectronFilter'),
    isSemiLeptonicMuonFlag=cms.InputTag('ttSemiLeptonicMuonFilter'),
    isSemiLeptonicTauFlag=cms.InputTag('ttSemiLeptonicTauFilter'),
    doElectronChannel=cms.untracked.bool(True),
    gen_jet_input=cms.InputTag('ak5GenJets'),
    jet_input=cms.InputTag('selectedPatJetsPFlow'),
    electron_input=cms.InputTag('selectedPatElectronsPFlow'),
    muon_input=cms.InputTag('selectedPatMuonsPFlow'),
    vertex_input=cms.InputTag('goodOfflinePrimaryVertices'),
    gen_event_input=cms.InputTag('genEvt'),
    variable_under_analysis=cms.string('MET'),
    variable_min=cms.double(0.),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(2000),
    bin_edges=cms.vdouble([0, 25, 45, 70, 100, 150, 2000])
)

unfolding_MET_analyser_muon_channel = unfolding_MET_analyser_electron_channel.clone(
    doElectronChannel=cms.untracked.bool(False),
    selectionFlagInput=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.FullSelection', 'PAT'),
)

unfolding_HT_analyser_electron_channel = unfolding_MET_analyser_electron_channel.clone(
    variable_under_analysis=cms.string('HT'),
    variable_min=cms.double(50),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(1950),
    bin_edges=cms.vdouble([50, 150, 250, 350, 450, 650, 1100, 2000])
)

unfolding_HT_analyser_muon_channel = unfolding_HT_analyser_electron_channel.clone(
    doElectronChannel=cms.untracked.bool(False),
    selectionFlagInput=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.FullSelection', 'PAT'),
)

unfolding_ST_analyser_electron_channel = unfolding_MET_analyser_electron_channel.clone(
    variable_under_analysis=cms.string('ST'),
    variable_min=cms.double(150),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(1850),
    bin_edges=cms.vdouble([150, 250, 350, 450, 550, 750, 1250, 2000])
)

unfolding_ST_analyser_muon_channel = unfolding_HT_analyser_electron_channel.clone(
    doElectronChannel=cms.untracked.bool(False),
    selectionFlagInput=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.FullSelection', 'PAT'),
)

unfolding_MT_analyser_electron_channel = unfolding_MET_analyser_electron_channel.clone(
    variable_under_analysis=cms.string('MT'),
    variable_min=cms.double(0),
    variable_max=cms.double(1000.),
    variable_n_bins=cms.uint32(1000),
    bin_edges=cms.vdouble([0, 40, 65, 85, 150, 1000])
)

unfolding_MT_analyser_muon_channel = unfolding_HT_analyser_electron_channel.clone(
    doElectronChannel=cms.untracked.bool(False),
    selectionFlagInput=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.FullSelection', 'PAT'),
)
