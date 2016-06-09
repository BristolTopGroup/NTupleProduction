import FWCore.ParameterSet.Config as cms

topPairEPlusJetsSelection = cms.EDFilter('TopPairElectronPlusJetsSelectionFilter',
    # Specify input collections
    jetInput=cms.InputTag("patJetsReapplyJEC"),
    electronInput=cms.InputTag("slimmedElectrons"),
    muonInput=cms.InputTag("slimmedMuons"),
    HLTInput=cms.InputTag('TriggerResults', '', 'HLT'),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),

    # Lepton cuts
    minSignalElectronPt=cms.double(23.),
    maxSignalElectronEta=cms.double(2.4),
    signalElectronIDMap=cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
    minSignalElectronID=cms.double(0),
    minLooseMuonPt=cms.double(10.),
    maxLooseMuonEta=cms.double(2.5),
    minLooseElectronPt=cms.double(15.),
    maxLooseElectronEta=cms.double(2.4),
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

    # Apply different JEC
    applyJEC = cms.bool(False),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),

    # B Jet Selection
    # Working points taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation74X50ns
    bJetDiscriminator=cms.string('pfCombinedInclusiveSecondaryVertexV2BJetTags'),
    minBJetDiscriminator=cms.double(0.800),
    tightBJetDiscriminator=cms.double(0.890),

    tightElectronIsolation_EB=cms.double(0.14),
    tightElectronIsolation_EE=cms.double(0.1649),

    controlElectronIsolation=cms.double(0.),

    looseMuonIsolation=cms.double(0.25),
   
    prefix=cms.untracked.string('TopPairElectronPlusJetsSelection.'),
    MCSampleTag = cms.string('Summer12'),#Fall11 or Summer12 or Summer11Leg

    #flags
    debug=cms.untracked.bool(False),
    taggingMode=cms.bool(False),

    tagAndProbeStudies = cms.bool(False),
    dropTriggerSelection = cms.bool(False),
    jetSelectionInTaggingMode = cms.bool(False),
    bSelectionInTaggingMode = cms.bool(True),
    nonIsolatedElectronSelection = cms.bool(False),
    invertedConversionSelection = cms.bool(False),
)

