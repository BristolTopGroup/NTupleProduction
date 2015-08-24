import FWCore.ParameterSet.Config as cms

nTupleElectrons = cms.EDProducer("BristolNTuple_Electrons",
    TracksInputTag = cms.InputTag('generalTracks'),
    DCSInputTag = cms.InputTag('scalersRawToDigi'),
    InputTag = cms.InputTag('slimmedElectrons'),
    Prefix = cms.string('Electrons.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    storePFIsolation = cms.bool(True),
    debugRelease = cms.bool(False),
    BeamSpotInputTag = cms.InputTag('offlineBeamSpot'),
    ConversionsInputTag = cms.InputTag('reducedEgamma','reducedConversions'),
    tightElectronIDMap=cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight'),
    tightElectronIDMap_bitmap=cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tightBitmap'),
)
