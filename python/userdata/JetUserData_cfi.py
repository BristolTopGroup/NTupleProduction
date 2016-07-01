import FWCore.ParameterSet.Config as cms

jetUserData = cms.EDProducer(
    'JetUserData',
    vertexCollection=cms.InputTag('offlineSlimmedPrimaryVertices'),
    jetCollection=cms.InputTag("patJetsReapplyJEC"),
    beamSpotCollection=cms.InputTag('offlineBeamSpot'),
    # Top Object Definitions
    minSignalJetPt=cms.double(25.),
    maxSignalJetEta=cms.double(2.4),
    
    jecUncertainty = cms.string('AK4PFchs'),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),    
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    isRealData = cms.bool(False),
    looseBTagWP = cms.double(0.460),
    mediumBTagWP = cms.double(0.800),
    tightBTagWP = cms.double(0.935),    
    btagCalibrationFile = cms.string('CSVv2.csv')
)
