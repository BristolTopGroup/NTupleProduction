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
    jerFromFile=cms.bool(False),
    resolutionFile=cms.string('data/JER/Spring16_25nsV6_MC_PtResolution_AK4PFchs.txt'),
    resolutionSFFile=cms.string('data/JER/Spring16_25nsV6_MC_SF_AK4PFchs.txt'),
    bJetDiscriminator=cms.string(
        'pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minBtagDiscLooseWP=cms.double(0.5426),
    minBtagDiscMediumWP=cms.double(0.8484),
    minBtagDiscTightWP=cms.double(0.9535),
    btagCalibrationFile=cms.string('CSVv2_ichep.csv'),
    rho=cms.InputTag('fixedGridRhoFastjetAll'),
)
