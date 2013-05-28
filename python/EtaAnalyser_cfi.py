import FWCore.ParameterSet.Config as cms

eta_MET_analyser_electron_channel_patMETsPFlow = cms.EDAnalyzer("EtaAnalyser",
    pu_weight_input=cms.InputTag('eventWeightPU'),
    b_tag_weight_input=cms.InputTag('eventWeightBtag'),
    gen_part_input=cms.InputTag('genParticles'), 
    reco_MET_Input=cms.InputTag('patMETsPFlow'),
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
    bin_edges=cms.vdouble([0, 25, 45, 70, 100, 150, 2000]),
    bin_edge_names=cms.vstring('_bin_0-25', '_bin_25-45', '_bin_45-70', '_bin_70-100', '_bin_100-150', '_bin_150-inf')
)

eta_MET_analyser_muon_channel_patMETsPFlow = eta_MET_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

eta_HT_analyser_electron_channel = eta_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('HT'),
    variable_min=cms.double(0.),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(2000),
    bin_edges=cms.vdouble([0,240,280,330,380,450,600,2000]),
    bin_edge_names=cms.vstring('_bin_0-240', '_bin_240-280', '_bin_280-330', '_bin_330-380', '_bin_380-450', '_bin_450-600', '_bin_600-inf')
)

eta_HT_analyser_muon_channel = eta_HT_analyser_electron_channel.clone(
    do_electron_channel=cms.untracked.bool(False),
)

eta_ST_analyser_electron_channel_patMETsPFlow = eta_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('ST'),
    variable_min=cms.double(0.),
    variable_max=cms.double(2000.),
    variable_n_bins=cms.uint32(2000),
    bin_edges=cms.vdouble([0, 350 , 400 , 450 , 500 , 570 , 650 , 2000]),
    bin_edge_names=cms.vstring('_bin_0-350','_bin_350-400', '_bin_400-450', '_bin_450-500', '_bin_500-580', '_bin_580-700', '_bin_700-inf')    
)

eta_ST_analyser_muon_channel_patMETsPFlow = eta_ST_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

eta_MT_analyser_electron_channel_patMETsPFlow = eta_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('MT'),
    variable_min=cms.double(0),
    variable_max=cms.double(1000.),
    variable_n_bins=cms.uint32(1000),
    bin_edges=cms.vdouble([0, 30, 50, 80, 100, 1000]),
    bin_edge_names=cms.vstring('_bin_0-30', '_bin_30-50', '_bin_50-80', '_bin_80-100', '_bin_100-inf')
)


eta_MT_analyser_muon_channel_patMETsPFlow = eta_MT_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

eta_WPT_analyser_electron_channel_patMETsPFlow = eta_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('WPT'),
    variable_min=cms.double(0),
    variable_max=cms.double(1000.),
    variable_n_bins=cms.uint32(1000),
    bin_edges=cms.vdouble([0, 40, 70, 100, 130, 170, 1000]),
    bin_edge_names=cms.vstring('_bin_0-40', '_bin_40-70', '_bin_70-100', '_bin_100-130', '_bin_130-170', '_bin_170-inf')
)

eta_WPT_analyser_muon_channel_patMETsPFlow = eta_WPT_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

eta_MET_analyser_electron_channel_patType1CorrectedPFMet = eta_MET_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

eta_MET_analyser_muon_channel_patType1CorrectedPFMet = eta_MET_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

eta_ST_analyser_electron_channel_patType1CorrectedPFMet = eta_ST_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

eta_ST_analyser_muon_channel_patType1CorrectedPFMet = eta_ST_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

eta_MT_analyser_electron_channel_patType1CorrectedPFMet = eta_MT_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

eta_MT_analyser_muon_channel_patType1CorrectedPFMet = eta_MT_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

eta_WPT_analyser_electron_channel_patType1CorrectedPFMet = eta_WPT_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

eta_WPT_analyser_muon_channel_patType1CorrectedPFMet = eta_WPT_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)
