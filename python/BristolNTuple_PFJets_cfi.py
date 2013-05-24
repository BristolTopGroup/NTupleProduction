import FWCore.ParameterSet.Config as cms

rootTuplePFJets = cms.EDProducer("BristolNTuple_PFJets",
    InputTag = cms.InputTag('cleanPatJetsAK5PF'),
    Prefix = cms.string('PFJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    JECUncertainty = cms.string('AK5PF'),
    ReadJECuncertainty = cms.bool(True),
    DoVertexAssociation = cms.bool(True),
    VertexInputTag = cms.InputTag('offlinePrimaryVertices'),
    isRealData = cms.bool(False)
)


rootTuplePF2PATJets = rootTuplePFJets.clone(InputTag = cms.InputTag('goodPatJetsPFlow'),
    Prefix = cms.string('goodPatJetsPFlow.'))
