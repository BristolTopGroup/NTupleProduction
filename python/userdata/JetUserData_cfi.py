import FWCore.ParameterSet.Config as cms

jetUserData = cms.EDProducer(
    'JetUserData',
    vertexCollection=cms.InputTag('offlineSlimmedPrimaryVertices'),
    jetCollection=cms.InputTag("slimmedJets"),
    beamSpotCollection=cms.InputTag('offlineBeamSpot'),
    # Top Object Definitions
    minSignalJetPt=cms.double(30.),
    maxSignalJetEta=cms.double(2.4),

    jecUncertainty=cms.string('AK4PFchs'),
    jetCorrectionService=cms.string('ak4PFCHSL1FastL2L3'),
#     jetCorrectorInputTag=cms.InputTag("ak4PFCHSL1FastL2L3CorrectorChain"),
    # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80X
    bJetDiscriminator=cms.string(
        'pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minBtagDiscLooseWP=cms.double(0.5426),
    minBtagDiscMediumWP=cms.double(0.8484),
    minBtagDiscTightWP=cms.double(0.9535),
    btagCalibrationFile=cms.string('CSVv2Moriond17_2017_1_26_BtoH.csv'),
)
