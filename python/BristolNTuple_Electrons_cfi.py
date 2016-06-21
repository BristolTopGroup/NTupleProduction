import FWCore.ParameterSet.Config as cms

nTupleElectrons = cms.EDProducer("BristolNTuple_Electrons",
    InputTag = cms.InputTag('slimmedElectrons'),
    Prefix = cms.string('Electrons.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    storePFIsolation = cms.bool(True),
    debugRelease = cms.bool(False),
    BeamSpotInputTag = cms.InputTag('offlineBeamSpot'),
    ConversionsInputTag = cms.InputTag('reducedEgamma','reducedConversions'),
    mediumElectronIDMap=cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
)
