import FWCore.ParameterSet.Config as cms

topPairMuPlusJetsSelection = cms.EDFilter('TopPairMuonPlusJetsSelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("slimmedJets"),
    electronInput=cms.InputTag("slimmedElectrons"),
    muonInput=cms.InputTag("slimmedMuons"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),
    VertexInput=cms.InputTag('offlineSlimmedPrimaryVertices'),

    # Signal muon cuts
    minSignalMuonPt=cms.double(23.),
    maxSignalMuonEta=cms.double(2.1),
    minLooseMuonPt=cms.double(10.),
    maxLooseMuonEta=cms.double(2.5),
    minLooseElectronPt=cms.double(20.),
    maxLooseElectronEta=cms.double(2.5),
    looseElectronIDMap=cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto'),
    minLooseElectronID=cms.double(0),

    #jet cuts
    min1JetPt=cms.double(20.),
    min2JetPt=cms.double(20.),
    min3JetPt=cms.double(20.),
    min4JetPt=cms.double(20.),
    minBJetPt=cms.double(20.),
    minJetPtInNtuples=cms.double(20.),

    # Jet cleaning delta R
    cleaningDeltaR=cms.double(0.3),

    # Maximum isolation for signal region
    tightMuonIsolation=cms.double(0.12),
    # Minimum isolation for control region
    controlMuonIsolation=cms.double(0.),

    # Apply different JEC
    applyJEC = cms.bool(False),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),

    # B Jet Selection
    # Working points taken from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideBTagging#Preliminary_working_or_operating
    bJetDiscriminator=cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minBJetDiscriminator=cms.double(0.814),

    prefix=cms.untracked.string('TopPairMuonPlusJetsSelection.'),

    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.bool(False),

    tagAndProbeStudies = cms.bool(False),
    dropTriggerSelection = cms.bool(False),
    bSelectionInTaggingMode = cms.bool(False),
    nonIsolatedMuonSelection = cms.bool(False),
)

