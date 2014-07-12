import FWCore.ParameterSet.Config as cms
bin_edges = {
             'MET':[0, 25, 45, 70, 100, 150, 250],
             'HT':[80, 240, 280, 330, 380, 450, 600, 1000],
             'ST':[106, 350, 400, 450, 500, 580, 700, 1000],
             'MT':[0, 30, 50, 80, 100, 200],
             'WPT':[0, 40, 70, 100, 130, 170, 250]
             }

variable_bins = {
             'MET':{'min':0, 'max':1000, 'n_bins':1000},
             'HT':{'min':0, 'max':2000, 'n_bins':2000},
             'ST':{'min':0, 'max':2500, 'n_bins':2500},
             'MT':{'min':0, 'max':1000, 'n_bins':1000},
             'WPT':{'min':0, 'max':1000, 'n_bins':1000},
             }

do_variations = ['normal', 'parton', 'no_cuts']

unfolding_MET_analyser_electron_channel_patMETsPFlow = cms.EDAnalyzer("UnfoldingAnalyser",
    pu_weight_input=cms.InputTag('eventWeightPU'),
    b_tag_weight_input=cms.InputTag('eventWeightBtag'),
    gen_part_input=cms.InputTag('genParticles'), 
    gen_MET_input=cms.InputTag('genMetTrue'),
    reco_MET_Input=cms.InputTag('patMETsPFlow'),
    gen_jet_input=cms.InputTag('ak5GenJetsNoNu'),
    reco_jet_input=cms.InputTag('selectedPatJetsPFlow'),
    electron_input=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJetsSelection.signalElectron', 'PAT'),
    muon_input=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJetsSelection.signalMuon', 'PAT'),
    vertex_input=cms.InputTag('goodOfflinePrimaryVertices'),
    gen_event_input=cms.InputTag('genEvt'),
    selection_flag_input=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJetsSelection.FullSelection', 'PAT'),
    is_fully_hadronic_flag=cms.InputTag('ttFullHadronicFilter'),
    is_dileptonic_flag=cms.InputTag('ttFullLeptonicFilter'),
    is_semileptonic_tau_flag=cms.InputTag('ttSemiLeptonicTauFilter'),
    is_semileptonic_electron_flag=cms.InputTag('ttSemiLeptonicElectronFilter'),
    is_semileptonic_muon_flag=cms.InputTag('ttSemiLeptonicMuonFilter'),
    do_electron_channel=cms.untracked.bool(True),
    variable_under_analysis=cms.string('MET'),
    variable_min=cms.double(variable_bins['MET']['min']),
    variable_max=cms.double(variable_bins['MET']['max']),
    variable_n_bins=cms.uint32(variable_bins['MET']['n_bins']),
    bin_edges=cms.vdouble([0, 25, 45, 70, 100, 150, 2000]),
    centre_of_mass_energy = cms.double( 8 ),
)

unfolding_MET_analyser_muon_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_MET_nu_analyser_electron_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('MET_nu'),
)

unfolding_MET_nu_analyser_muon_channel_patMETsPFlow = unfolding_MET_nu_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_HT_analyser_electron_channel = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('HT'),
    variable_min=cms.double(variable_bins['HT']['min']),
    variable_max=cms.double(variable_bins['ST']['max']),
    variable_n_bins=cms.uint32(variable_bins['MET']['n_bins']),
    bin_edges=cms.vdouble([0,240,280,330,380,450,600,2000])
)

unfolding_HT_analyser_muon_channel = unfolding_HT_analyser_electron_channel.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_HT_nocuts_analyser_electron_channel = unfolding_HT_analyser_electron_channel.clone(
    variable_under_analysis=cms.string('HT_nocuts'),
)

unfolding_HT_nocuts_analyser_muon_channel = unfolding_HT_nocuts_analyser_electron_channel.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_HT_parton_analyser_electron_channel = unfolding_HT_analyser_electron_channel.clone(
    variable_under_analysis=cms.string('HT_parton'),
)

unfolding_HT_parton_analyser_muon_channel = unfolding_HT_parton_analyser_electron_channel.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_ST_analyser_electron_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('ST'),
    variable_min=cms.double(variable_bins['ST']['min']),
    variable_max=cms.double(variable_bins['ST']['max']),
    variable_n_bins=cms.uint32(variable_bins['ST']['n_bins']),
    bin_edges=cms.vdouble([0, 350 , 400 , 450 , 500 , 580 , 700 , 2000])
)

unfolding_ST_analyser_muon_channel_patMETsPFlow = unfolding_ST_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_ST_nocuts_analyser_electron_channel_patMETsPFlow = unfolding_ST_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('ST_nocuts'),
)

unfolding_ST_nocuts_analyser_muon_channel_patMETsPFlow = unfolding_ST_nocuts_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_ST_parton_analyser_electron_channel_patMETsPFlow = unfolding_ST_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('ST_parton'),
)

unfolding_ST_parton_analyser_muon_channel_patMETsPFlow = unfolding_ST_parton_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_MT_analyser_electron_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('MT'),
    variable_min=cms.double(variable_bins['MT']['min']),
    variable_max=cms.double(variable_bins['MT']['max']),
    variable_n_bins=cms.uint32(variable_bins['MT']['n_bins']),
    bin_edges=cms.vdouble([0, 30, 50, 80, 100, 1000])
)

unfolding_MT_analyser_muon_channel_patMETsPFlow = unfolding_MT_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_MT_nu_analyser_electron_channel_patMETsPFlow = unfolding_MT_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('MT_nu'),
)

unfolding_MT_nu_analyser_muon_channel_patMETsPFlow = unfolding_MT_nu_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_WPT_analyser_electron_channel_patMETsPFlow = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('WPT'),
    variable_min=cms.double(variable_bins['WPT']['min']),
    variable_max=cms.double(variable_bins['WPT']['max']),
    variable_n_bins=cms.uint32(variable_bins['WPT']['n_bins']),
    bin_edges=cms.vdouble([0, 40, 70, 100, 130, 170, 1000])
)

unfolding_WPT_analyser_muon_channel_patMETsPFlow = unfolding_WPT_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_WPT_nu_analyser_electron_channel_patMETsPFlow = unfolding_WPT_analyser_electron_channel_patMETsPFlow.clone(
    variable_under_analysis=cms.string('WPT_nu'),
)

unfolding_WPT_nu_analyser_muon_channel_patMETsPFlow = unfolding_WPT_nu_analyser_electron_channel_patMETsPFlow.clone(
    do_electron_channel=cms.untracked.bool(False),
)

unfolding_MET_analyser_electron_channel_patType1CorrectedPFMet = unfolding_MET_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MET_analyser_muon_channel_patType1CorrectedPFMet = unfolding_MET_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MET_nu_analyser_electron_channel_patType1CorrectedPFMet = unfolding_MET_nu_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MET_nu_analyser_muon_channel_patType1CorrectedPFMet = unfolding_MET_nu_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_analyser_electron_channel_patType1CorrectedPFMet = unfolding_ST_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_analyser_muon_channel_patType1CorrectedPFMet = unfolding_ST_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_nocuts_analyser_electron_channel_patType1CorrectedPFMet = unfolding_ST_nocuts_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_nocuts_analyser_muon_channel_patType1CorrectedPFMet = unfolding_ST_nocuts_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_parton_analyser_electron_channel_patType1CorrectedPFMet = unfolding_ST_parton_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_ST_parton_analyser_muon_channel_patType1CorrectedPFMet = unfolding_ST_parton_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MT_analyser_electron_channel_patType1CorrectedPFMet = unfolding_MT_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MT_analyser_muon_channel_patType1CorrectedPFMet = unfolding_MT_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MT_nu_analyser_electron_channel_patType1CorrectedPFMet = unfolding_MT_nu_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_MT_nu_analyser_muon_channel_patType1CorrectedPFMet = unfolding_MT_nu_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_WPT_analyser_electron_channel_patType1CorrectedPFMet = unfolding_WPT_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_WPT_analyser_muon_channel_patType1CorrectedPFMet = unfolding_WPT_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_WPT_nu_analyser_electron_channel_patType1CorrectedPFMet = unfolding_WPT_nu_analyser_electron_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)

unfolding_WPT_nu_analyser_muon_channel_patType1CorrectedPFMet = unfolding_WPT_nu_analyser_muon_channel_patMETsPFlow.clone(
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
)
