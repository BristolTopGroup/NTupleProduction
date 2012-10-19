import FWCore.ParameterSet.Config as cms

unfoldingAnalyserElectronChannel = cms.EDAnalyzer("UnfoldingAnalyser",
    PUWeightInput = cms.InputTag('eventWeightPU'),
    BtagWeightInput = cms.InputTag( 'eventWeightBtag' ),
    genMetInput = cms.InputTag( 'genMetTrue' ),
    recoMetInput = cms.InputTag( 'patType1CorrectedPFMet' ),
    selectionFlagInput = cms.InputTag("topPairEPlusJetsSelection",  'TopPairElectronPlusJets2012Selection.FullSelection', 'PAT' ),
    isFullyHadronicTtbarFlag = cms.InputTag( 'ttFullHadronicFilter' ),
    isDiLeptonicTtbarFlag = cms.InputTag( 'ttFullLeptonicFilter' ),
    isSemiLeptonicElectronFlag = cms.InputTag( 'ttSemiLeptonicElectronFilter' ),
    isSemiLeptonicMuonFlag = cms.InputTag( 'ttSemiLeptonicMuonFilter' ),
    isSemiLeptonicTauFlag = cms.InputTag( 'ttSemiLeptonicTauFilter' ),
    doElectronChannel = cms.untracked.bool(True)
)

unfoldingAnalyserMuonChannel = unfoldingAnalyserElectronChannel.clone(
    doElectronChannel = cms.untracked.bool(False),
    selectionFlagInput = cms.InputTag("topPairMuPlusJetsSelection",  'TopPairMuonPlusJets2012Selection.FullSelection', 'PAT' ),
)

