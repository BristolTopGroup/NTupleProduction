import FWCore.ParameterSet.Config as cms
selectionPrefix = 'TopPairElectronPlusJets2012Selection.'
selectionName = 'topPairEPlusJetsSelection'
selectionCuts = [
                "AllEvents",
                "EventCleaningAndTrigger",
                "OneIsolatedElectron",
                "LooseMuonVeto",
                "DiLeptonVeto",
                "ConversionVeto",
                "AtLeastOneGoodJet",
                "AtLeastTwoGoodJets",
                "AtLeastThreeGoodJets",
                "AtLeastFourGoodJets",
                "AtLeastOneBtag",
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'PAT') for cut in selectionCuts]

topPairEPlusJetsSelectionAnalyser = cms.EDAnalyzer("SelectionAnalyser",
    PUWeightInput=cms.InputTag('eventWeightPU'),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

selectionPrefix = 'TopPairMuonPlusJets2012Selection.'
selectionName = 'topPairMuPlusJetsSelection'
selectionCuts = [
               "AllEvents", 
                "EventCleaningAndTrigger", 
                "OneIsolatedMuon", 
                "LooseMuonVeto", 
                "LooseElectronVeto", 
                "AtLeastOneGoodJet", 
                "AtLeastTwoGoodJets", 
                "AtLeastThreeGoodJets", 
                "AtLeastFourGoodJets", 
                "AtLeastOneBtag", 
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'PAT') for cut in selectionCuts]

topPairMuPlusJetsSelectionAnalyser = cms.EDAnalyzer("SelectionAnalyser",
    PUWeightInput=cms.InputTag('eventWeightPU'),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

ttbarDecayAnalyser = cms.EDAnalyzer("SelectionAnalyser",
    PUWeightInput=cms.InputTag('eventWeightPU'),
    selectionFlags=cms.VInputTag(
                cms.InputTag( 'ttFullHadronicFilter' ),
                cms.InputTag( 'ttSemiLeptonicElectronFilter' ),
                cms.InputTag( 'ttSemiLeptonicMuonFilter' ),
                cms.InputTag( 'ttSemiLeptonicTauFilter' ),
                cms.InputTag( 'ttFullLeptonicEEFilter' ),
                cms.InputTag( 'ttFullLeptonicMuMuFilter' ),
                cms.InputTag( 'ttFullLeptonicTauTauFilter' ),
                cms.InputTag( 'ttFullLeptonicETauFilter' ),
                cms.InputTag( 'ttFullLeptonicEMuFilter' ),
                cms.InputTag( 'ttFullLeptonicMuTauFilter' ),
                ),
    selectionNames=cms.vstring('fullHadronic',
                               'SemiLeptonicElectron',
                               'SemiLeptonicMuon',
                               'SemiLeptonicTau',
                               'FullLeptonicEE',
                               'FullLeptonicMuMu',
                               'FullLeptonicTauTau',
                               'FullLeptonicETau',
                               'FullLeptonicEMu',
                               'FullLeptonicMuTau'),
)

