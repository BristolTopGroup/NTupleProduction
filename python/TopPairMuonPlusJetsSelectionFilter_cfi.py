import FWCore.ParameterSet.Config as cms

topPairMuPlusJetsSelection = cms.EDFilter('TopPairMuonPlusJetsSelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("patJetsReapplyJEC"),
    electronInput=cms.InputTag("slimmedElectrons"),
    muonInput=cms.InputTag("slimmedMuons"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),
    VertexInput=cms.InputTag('offlineSlimmedPrimaryVertices'),

    # Signal muon cuts
    minSignalMuonPt=cms.double(18.),
    maxSignalMuonEta=cms.double(2.1),
    minLooseMuonPt=cms.double(15.),
    maxLooseMuonEta=cms.double(2.1),
    minLooseElectronPt=cms.double(15.),
    maxLooseElectronEta=cms.double(2.1),
    looseElectronIDMap=cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'),
    minLooseElectronID=cms.double(0),

    #jet cuts
    min1JetPt=cms.double(20.),
    min2JetPt=cms.double(20.),
    min3JetPt=cms.double(20.),
    min4JetPt=cms.double(20.),
    minBJetPt=cms.double(20.),
    minJetPtInNtuples=cms.double(20.),

    # Jet cleaning delta R
    cleaningDeltaR=cms.double(0.4),

    # Maximum isolation for signal region
    tightMuonIsolation=cms.double(0.12),
    # Minimum isolation for control region
    controlMuonIsolation1=cms.double(0.3),
    controlMuonIsolation2=cms.double(0.15),

    looseMuonIsolation=cms.double(0.2),

    # Apply different JEC
    applyJEC = cms.bool(False),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),

    # B Jet Selection
    # Working points taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation74X50ns
    bJetDiscriminator=cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minBJetDiscriminator=cms.double(0.890),

    prefix=cms.untracked.string('TopPairMuonPlusJetsSelection.'),

    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.bool(False),

    tagAndProbeStudies = cms.bool(False),
    dropTriggerSelection = cms.bool(False),
    bSelectionInTaggingMode = cms.bool(True),
    nonIsolatedMuonSelection1 = cms.bool(False),
    nonIsolatedMuonSelection2 = cms.bool(False),
)

