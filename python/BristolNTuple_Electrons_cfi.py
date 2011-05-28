import FWCore.ParameterSet.Config as cms

rootTupleElectrons = cms.EDProducer("BristolNTuple_Electrons",
    TracksInputTag = cms.InputTag('generalTracks'),
    DCSInputTag = cms.InputTag('scalersRawToDigi'),
    InputTag = cms.InputTag('cleanPatElectrons'),
    Prefix = cms.string('Electron.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    VertexInputTag = cms.InputTag('offlinePrimaryVertices'),
    storePFIsolation = cms.bool(False)
    
)

rootTuplePFElectrons = rootTupleElectrons.clone(
    InputTag = cms.InputTag('selectedPatElectronsPF'),
    Prefix = cms.string('PFElectron.'),
    storePFIsolation = cms.bool(True))

rootTupleElectronSequence =  cms.Sequence(rootTupleElectrons + rootTuplePFElectrons)
