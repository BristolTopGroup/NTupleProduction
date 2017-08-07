import FWCore.ParameterSet.Config as cms

nTuplePFCands = cms.EDProducer("BristolNTuple_PFCandidates",
    pfCandidatesTag = cms.InputTag("packedPFCandidates"),
)