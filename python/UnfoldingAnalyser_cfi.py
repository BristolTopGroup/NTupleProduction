import FWCore.ParameterSet.Config as cms

unfolding_MET_analyser_electron_channel_patMETsPFlow = cms.EDAnalyzer("UnfoldingAnalyser",
    pu_weight_input=cms.InputTag('eventWeightPU'),
    b_tag_weight_input=cms.InputTag('eventWeightBtag'),
    gen_MET_input=cms.InputTag('genMetTrue'),
    reco_MET_Input=cms.InputTag('patMETsPFlow'),
    gen_jet_input=cms.InputTag('ak5GenJets'),
    reco_jet_input=cms.InputTag('selectedPatJetsPFlow'),
    electron_input=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.signalElectron', 'PAT'),
    muon_input=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.signalMuon', 'PAT'),
    vertex_input=cms.InputTag('goodOfflinePrimaryVertices'),
    gen_event_input=cms.InputTag('genEvt'),
    selection_flag_input=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.FullSelection', 'PAT'),
    is_fully_hadronic_flag=cms.InputTag('ttFullHadronicFilter'),
    is_dileptonic_flag=cms.InputTag('ttFullLeptonicFilter'),
    is_semileptonic_tau_flag=cms.InputTag('ttSemiLeptonicTauFilter'),
    is_semileptonic_electron_flag=cms.InputTag('ttSemiLeptonicElectronFilter'),
    is_semileptonic_muon_flag=cms.InputTag('ttSemiLeptonicMuonFilter'),
    do_electron_channel=cms.untracked.bool(True),
    variable_under_analysis=cms.string('MET'),
    variable_min=cms.double(0.),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(2000),
    bin_edges=cms.vdouble([0, 25, 45, 70, 100, 150, 2000])
)

unfolding_MET_analyser_muon_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_HT_analyser_electron_channel = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('HT'),
    variable_min=cms.double(50),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(1950),
    bin_edges=cms.vdouble([50, 150, 250, 350, 450, 650, 1100, 2000])
)

unfolding_HT_analyser_muon_channel = unfolding_HT_analyser_electron_channel.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_ST_analyser_electron_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('ST'),
    variable_min=cms.double(150),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(1850),
    bin_edges=cms.vdouble([150, 250, 350, 450, 550, 750, 1250, 2000])
)

unfolding_ST_analyser_muon_channel_patMETsPFlow = unfolding_ST_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_MT_analyser_electron_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('MT'),
    variable_min=cms.double(0),
    variable_max=cms.double(1000.),
    variable_n_bins=cms.uint32(1000),
    bin_edges=cms.vdouble([0, 40, 65, 85, 150, 1000])
)

unfolding_MT_analyser_muon_channel_patMETsPFlow = unfolding_MT_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_MET_analyser_electron_channel_patType1CorrectedPFMet = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MET_analyser_muon_channel_patType1CorrectedPFMet = unfolding_MET_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_analyser_electron_channel_patType1CorrectedPFMet = unfolding_ST_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_analyser_muon_channel_patType1CorrectedPFMet = unfolding_ST_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MT_analyser_electron_channel_patType1CorrectedPFMet = unfolding_MT_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MT_analyser_muon_channel_patType1CorrectedPFMet = unfolding_MT_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)