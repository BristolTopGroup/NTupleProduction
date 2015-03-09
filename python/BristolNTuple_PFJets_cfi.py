import FWCore.ParameterSet.Config as cms

nTuplePFJets = cms.EDProducer("BristolNTuple_PFJets",
    InputTag = cms.InputTag('slimmedJets'),
    Prefix = cms.string('Jets.'),
    Suffix = cms.string(''),
    minJetPtToStore = cms.double(30),
    MaxSize = cms.uint32(99),
    JECUncertainty = cms.string('AK4PF'),
    ReadJECuncertainty = cms.bool(False),
    ReadJEC = cms.bool(True),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),    
    DoVertexAssociation = cms.bool(True),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    isRealData = cms.bool(False)
)
