import FWCore.ParameterSet.Config as cms

jetUserData = cms.EDProducer(
    'JetUserData',
    vertexCollection=cms.InputTag('offlineSlimmedPrimaryVertices'),
    jetCollection=cms.InputTag("patJetsReapplyJEC"),
    beamSpotCollection=cms.InputTag('offlineBeamSpot'),
    # Top Object Definitions
    minSignalJetPt=cms.double(20.),
    maxSignalJetEta=cms.double(2.4),

    jecUncertainty=cms.string('AK4PFchs'),
    JetCorrectionService=cms.string('ak4PFCHSL1FastL2L3'),
    VertexInputTag=cms.InputTag('offlineSlimmedPrimaryVertices'),
    # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80X
    bJetDiscriminator=cms.string(
        'pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minBtagDiscLooseWP=cms.double(0.460),
    minBtagDiscMediumWP=cms.double(0.800),
    minBtagDiscTightWP=cms.double(0.935),
    btagCalibrationFile=cms.string('CSVv2.csv'),
)
