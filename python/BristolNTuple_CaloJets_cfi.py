import FWCore.ParameterSet.Config as cms

rootTupleCaloJets = cms.EDProducer("BristolNTuple_CaloJets",
    InputTag = cms.InputTag('cleanPatJets'),
    Prefix = cms.string('CaloJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    JECUncertainty = cms.string('AK5Calo'),
    ReadJECuncertainty = cms.bool(True)
)

rootTupleCaloJetSequence = cms.Sequence(rootTupleCaloJets)

