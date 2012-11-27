import FWCore.ParameterSet.Config as cms

rootTupleRecoPFMET = cms.EDProducer("BristolNTuple_RecoMET",
    InputTag=cms.InputTag('pfMet'),
    Prefix=cms.string('recoMetPFlow.'),
    Suffix=cms.string(''),
)
