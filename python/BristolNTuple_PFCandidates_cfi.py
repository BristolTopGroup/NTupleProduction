import FWCore.ParameterSet.Config as cms

from CommonTools.PileupAlgos.Puppi_cff import puppi
## e.g. to run on miniAOD
puppi.candName = cms.InputTag('packedPFCandidates')
puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices')

nTuplePFCands = cms.EDProducer("BristolNTuple_PFCandidates",
    # pfCandidatesTag = cms.InputTag("packedPFCandidates"),
    pfCandidatesTag = cms.InputTag("puppi"),

    electrons=cms.InputTag("goodElectrons"),
    muons=cms.InputTag("goodMuons"),

)