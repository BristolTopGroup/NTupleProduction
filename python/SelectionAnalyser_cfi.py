import FWCore.ParameterSet.Config as cms

unfoldingAnalyser = cms.EDProducer("UnfoldingAnalyser",
    PUWeightInput = cms.InputTag( 'eventWeightPU' ),
#    BtagWeightInput = cms.InputTag( 'eventWeightBtag' ),
    genMetInput = cms.InputTag( 'genMetTrue' ),
    recoMetInput = cms.InputTag( 'patType1CorrectedPFMet' ),
    selectionFlagInput = cms.InputTag( 'TopPairElectronPlusJets2012Selection.FullSelection' ),
    isFullyHadronicTtbarFlag = cms.InputTag( 'ttFullyHadronicFilter' ),
    isDiLeptonicTtbarFlag = cms.InputTag( 'ttFullyLeptonicFilter' ),
    isSemiLeptonicTauFlag = cms.InputTag( 'ttSemiLeptonicTauFilter' ),
    isSemiLeptonicElectronFlag = cms.InputTag( 'ttSemiLeptonicElectronFilter' ),
    isSemiLeptonicMuonFlag = cms.InputTag( 'ttSemiLeptonicMuonFilter' ),
    doElectronChannel = cms.untracked.bool(False)
)

