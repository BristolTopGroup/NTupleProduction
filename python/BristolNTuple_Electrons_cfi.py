import FWCore.ParameterSet.Config as cms

rootTupleElectrons = cms.EDProducer("BristolNTuple_Electrons",
    TracksInputTag = cms.InputTag('generalTracks'),
    DCSInputTag = cms.InputTag('scalersRawToDigi'),
    InputTag = cms.InputTag('cleanPatElectrons'),
    Prefix = cms.string('Electron.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    VertexInputTag = cms.InputTag('goodOfflinePrimaryVertices'),
    storePFIsolation = cms.bool(False),
    BeamSpotInputTag = cms.InputTag('offlineBeamSpot'),
    ConversionsInputTag = cms.InputTag('allConversions'),
    LikelihoodInputTag = cms.InputTag('egammaIDLikelihood'),
)

rootTuplePFLooseElectrons = rootTupleElectrons.clone(
    InputTag = cms.InputTag('selectedPatElectronsPF'),
    Prefix = cms.string('PFElectron.'),
    storePFIsolation = cms.bool(True)
)

rootTuplePFElectrons = rootTupleElectrons.clone(
    InputTag = cms.InputTag('selectedPatElectronsPF'),
    Prefix = cms.string('PFElectron.'),
    storePFIsolation = cms.bool(True)
)

rootTupleElectronSequence =  cms.Sequence(rootTupleElectrons + rootTuplePFElectrons)
