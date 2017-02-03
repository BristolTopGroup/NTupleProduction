import FWCore.ParameterSet.Config as cms

eventUserData = cms.EDProducer(
    'EventUserData',
    vertexCollection=cms.InputTag('offlineSlimmedPrimaryVertices'),
    electronCollection=cms.InputTag("goodElectrons"),
    muonCollection=cms.InputTag("goodMuons"),
    jetCollection=cms.InputTag("goodJets"),
    bJetCollection=cms.InputTag("goodBJets"),
    metInputTag=cms.InputTag('slimmedMETs'),

    # selection and similar
    isElectron=cms.bool(True),
    #
    prefix=cms.string('TopPairElectronPlusJetsSelection.'),
    suffix=cms.string(''),
)
