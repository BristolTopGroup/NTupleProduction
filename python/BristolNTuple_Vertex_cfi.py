import FWCore.ParameterSet.Config as cms

rootTupleVertex = cms.EDProducer("BristolNTuple_Vertex",
    InputTag = cms.InputTag('offlinePrimaryVertices'),
    Prefix = cms.string('Vertex.'),
    Suffix = cms.string('')
)

rootTupleVertexWithBS = cms.EDProducer("BristolNTuple_Vertex",
    InputTag = cms.InputTag('offlinePrimaryVerticesWithBS'),
    Prefix = cms.string('VertexWRTBeamSpot.'),
    Suffix = cms.string('')
)

