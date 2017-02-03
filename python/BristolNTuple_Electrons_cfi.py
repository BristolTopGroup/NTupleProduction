import FWCore.ParameterSet.Config as cms

nTupleElectrons = cms.EDProducer("BristolNTuple_Electrons",
    InputTag = cms.InputTag('calibratedPatElectrons'),
    Prefix = cms.string('Electrons.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    minPtToStore = cms.double(10.),
    storePFIsolation = cms.bool(True),
    debugRelease = cms.bool(False),
)
