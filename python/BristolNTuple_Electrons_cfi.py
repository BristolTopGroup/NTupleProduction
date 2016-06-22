import FWCore.ParameterSet.Config as cms

nTupleElectrons = cms.EDProducer("BristolNTuple_Electrons",
    InputTag = cms.InputTag('slimmedElectrons'),
    Prefix = cms.string('Electrons.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    storePFIsolation = cms.bool(True),
    debugRelease = cms.bool(False),
)
