import FWCore.ParameterSet.Config as cms

muonUserData = cms.EDProducer(
    'MuonUserData',
    vertexCollection=cms.InputTag('offlineSlimmedPrimaryVertices'),
    muonCollection=cms.InputTag("slimmedMuons"),
    beamSpotCollection=cms.InputTag('offlineBeamSpot'),
    # Top Object Definitions
    minSignalMuonPt=cms.double(26.),
    maxSignalMuonEta=cms.double(2.4),
    minLooseMuonPt=cms.double(15.),
    maxLooseMuonEta=cms.double(2.5),
    useBeamSpotCorrection=cms.bool(True),
    # Maximum isolation for signal region
    tightMuonIsolation=cms.double(0.15),
    # Minimum isolation for control region
    controlMuonIsolation1=cms.double(0.3),
    controlMuonIsolation2=cms.double(0.15),

    looseMuonIsolation=cms.double(0.25),
)
