import FWCore.ParameterSet.Config as cms

nTupleGenEventInfo = cms.EDProducer("BristolNTuple_GenEventInfo",
    GenEventInfoInputTag = cms.InputTag('generator'),
    LHEEventInfoInputTag = cms.InputTag('externalLHEProducer'),
    GenJetsInputTag      = cms.InputTag('slimmedGenJets'),
    StorePDFWeights      = cms.bool(True),
    PUWeightsInputTag    = cms.InputTag('eventWeightPU'),
    PDFWeightsInputTag   = cms.InputTag('pdfWeights','cteq66'),
    pileupInfo           = cms.InputTag('slimmedAddPileupInfo'),
    Prefix               = cms.string('Event.'),
    Suffix               = cms.string(''),
    ttbarDecayFlags      = cms.VInputTag(
                                         cms.InputTag( 'ttFullHadronicFilter' ),
                                         cms.InputTag( 'ttSemiLeptonicElectronFilter' ),
                                         cms.InputTag( 'ttSemiLeptonicMuonFilter' ),
                                         cms.InputTag( 'ttSemiLeptonicTauFilter' ),
                                         cms.InputTag( 'ttFullLeptonicEEFilter' ),
                                         cms.InputTag( 'ttFullLeptonicMuMuFilter' ),
                                         cms.InputTag( 'ttFullLeptonicTauTauFilter' ),
                                         cms.InputTag( 'ttFullLeptonicETauFilter' ),
                                         cms.InputTag( 'ttFullLeptonicEMuFilter' ),
                                         cms.InputTag( 'ttFullLeptonicMuTauFilter' ),
                ),
    isTTbarMC = cms.bool(False),
    tt_gen_event_input=cms.InputTag('genEvt'),

    minGenJetPt = cms.double(20.),
    maxGenJetAbsoluteEta = cms.double(999.),

    NJettinessInputTags = cms.VInputTag(
                                        cms.InputTag('pseudoTop','tau1','Ntuples'),
                                        cms.InputTag('pseudoTop','tau2','Ntuples'),
                                        cms.InputTag('pseudoTop','tau3','Ntuples'),
                                        cms.InputTag('pseudoTop','tau4','Ntuples'),
                                        cms.InputTag('pseudoTop','tau5','Ntuples'),
                                        cms.InputTag('pseudoTop','tau6','Ntuples'),
                                        )


)
