import FWCore.ParameterSet.Config as cms

nTuplePFJets = cms.EDProducer("BristolNTuple_PFJets",
    InputTag = cms.InputTag('slimmedJets'),
    Prefix = cms.string('Jets.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    JECUncertainty = cms.string('AK5PF'),
    ReadJECuncertainty = cms.bool(False),
    DoVertexAssociation = cms.bool(True),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    isRealData = cms.bool(False)
)
