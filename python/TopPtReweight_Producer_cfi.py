import FWCore.ParameterSet.Config as cms

eventWeightTopPt = cms.EDProducer("TopPtReweight_Producer",
    gen_event_input = cms.InputTag( 'genEvt'),
    genParticles = cms.InputTag( 'genParticles'),
    prefix = cms.string( 'TopPtReweights.'),
#    TopPtSystematic = cms.int32(0),
)