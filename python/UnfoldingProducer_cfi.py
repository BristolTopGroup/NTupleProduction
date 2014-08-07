import FWCore.ParameterSet.Config as cms

unfoldingProducerElectron = cms.EDProducer("UnfoldingProducer",
    pu_weight_input=cms.InputTag('eventWeightPU'),
    b_tag_weight_input=cms.InputTag('eventWeightBtag'),
    storePDFWeights=cms.bool(True),
    PDFWeightsInputTag=cms.InputTag('pdfWeights','cteq66'),
    gen_part_input=cms.InputTag('genParticles'), 
    gen_MET_input=cms.InputTag('genMetTrue'),
    reco_MET_Input=cms.InputTag('patType1CorrectedPFMet'),
    gen_jet_input=cms.InputTag('ak5GenJetsNoNu'),
    reco_jet_input=cms.InputTag('selectedPatJetsPFlow'),
    electron_input=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJetsSelection.signalElectron', 'PAT'),
    muon_input=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJetsSelection.signalMuon', 'PAT'),
    vertex_input=cms.InputTag('goodOfflinePrimaryVertices'),
    gen_event_input=cms.InputTag('genEvt'),
    selection_flag_input=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJetsSelection.FullSelection', 'PAT'),
    is_semileptonic_electron_flag=cms.InputTag('ttSemiLeptonicElectronFilter'),
    is_semileptonic_muon_flag=cms.InputTag('ttSemiLeptonicMuonFilter'),
    do_electron_channel=cms.untracked.bool(True),
    Prefix = cms.string('unfolding.'),
    Suffix = cms.string(''),
)

unfoldingProducerMuon = unfoldingProducerElectron.clone( 
                                                        do_electron_channel=cms.untracked.bool(False),
                                                        )
