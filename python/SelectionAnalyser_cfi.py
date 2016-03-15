import FWCore.ParameterSet.Config as cms
selectionPrefix = 'TopPairElectronPlusJetsSelection.'
selectionName = 'topPairEPlusJetsSelectionTagging'
selectionCuts = [
                "AllEvents",
                "EventCleaningAndTrigger",
                "ExactlyOneSignalElectron",
                "LooseMuonVeto",
                "LooseElectronVeto",
                "ConversionVeto",
                "AtLeastOneGoodJet",
                "AtLeastTwoGoodJets",
                "AtLeastThreeGoodJets",
                "AtLeastFourGoodJets",
                "AtLeastOneBtag",
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'Ntuples') for cut in selectionCuts]

topPairEPlusJetsSelectionAnalyser = cms.EDAnalyzer("SelectionAnalyser",
    # PUWeightInput=cms.InputTag('eventWeightPU'),
    genEvtInfoProduct = cms.InputTag("generator"),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

selectionPrefix = 'TopPairElectronPlusJetsQCDSelection.'
selectionName = 'topPairEPlusJetsQCDSelectionTagging'
selectionCuts = [
                "AllEvents",
                "EventCleaningAndTrigger",
                "ExactlyOneSignalElectron",
                "LooseMuonVeto",
                "LooseElectronVeto",
                "ConversionVeto",
                "AtLeastOneGoodJet",
                "AtLeastTwoGoodJets",
                "AtLeastThreeGoodJets",
                "AtLeastFourGoodJets",
                "AtLeastOneBtag",
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'Ntuples') for cut in selectionCuts]

topPairEPlusJetsQCDSelectionAnalyser = cms.EDAnalyzer("SelectionAnalyser",
    # PUWeightInput=cms.InputTag('eventWeightPU'),
    genEvtInfoProduct = cms.InputTag("generator"),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

selectionPrefix = 'TopPairElectronPlusJetsConversionSelection.'
selectionName = 'topPairEPlusJetsConversionSelectionTagging'
selectionCuts = [
                "AllEvents",
                "EventCleaningAndTrigger",
                "ExactlyOneSignalElectron",
                "LooseMuonVeto",
                "LooseElectronVeto",
                "ConversionVeto",
                "AtLeastOneGoodJet",
                "AtLeastTwoGoodJets",
                "AtLeastThreeGoodJets",
                "AtLeastFourGoodJets",
                "AtLeastOneBtag",
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'Ntuples') for cut in selectionCuts]

topPairEPlusJetsConversionSelectionAnalyser = cms.EDAnalyzer("SelectionAnalyser",
    # PUWeightInput=cms.InputTag('eventWeightPU'),
    genEvtInfoProduct = cms.InputTag("generator"),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

selectionPrefix = 'TopPairMuonPlusJetsSelection.'
selectionName = 'topPairMuPlusJetsSelectionTagging'
selectionCuts = [
               "AllEvents", 
                "EventCleaningAndTrigger", 
                "ExactlyOneSignalMuon", 
                "LooseMuonVeto", 
                "LooseElectronVeto", 
                "AtLeastOneGoodJet", 
                "AtLeastTwoGoodJets", 
                "AtLeastThreeGoodJets", 
                "AtLeastFourGoodJets", 
                "AtLeastOneBtag", 
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'Ntuples') for cut in selectionCuts]

topPairMuPlusJetsSelectionAnalyser = cms.EDAnalyzer("SelectionAnalyser",
    # PUWeightInput=cms.InputTag('eventWeightPU'),
    genEvtInfoProduct = cms.InputTag("generator"),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

selectionPrefix = 'TopPairMuonPlusJetsQCDSelection3toInf.'
selectionName = 'topPairMuPlusJetsQCDSelectionTagging1'
selectionCuts = [
               "AllEvents", 
                "EventCleaningAndTrigger", 
                "ExactlyOneSignalMuon", 
                "LooseMuonVeto", 
                "LooseElectronVeto", 
                "AtLeastOneGoodJet", 
                "AtLeastTwoGoodJets", 
                "AtLeastThreeGoodJets", 
                "AtLeastFourGoodJets", 
                "AtLeastOneBtag", 
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'Ntuples') for cut in selectionCuts]

topPairMuPlusJetsQCDSelectionAnalyser3toInf = cms.EDAnalyzer("SelectionAnalyser",
    # PUWeightInput=cms.InputTag('eventWeightPU'),
    genEvtInfoProduct = cms.InputTag("generator"),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

selectionPrefix = 'TopPairMuonPlusJetsQCDSelection1p5to3.'
selectionName = 'topPairMuPlusJetsQCDSelectionTagging2'
selectionCuts = [
               "AllEvents", 
                "EventCleaningAndTrigger", 
                "ExactlyOneSignalMuon", 
                "LooseMuonVeto", 
                "LooseElectronVeto", 
                "AtLeastOneGoodJet", 
                "AtLeastTwoGoodJets", 
                "AtLeastThreeGoodJets", 
                "AtLeastFourGoodJets", 
                "AtLeastOneBtag", 
                "AtLeastTwoBtags" 
                         ]
selectionProducts = [cms.InputTag(selectionName, selectionPrefix + cut, 'Ntuples') for cut in selectionCuts]

topPairMuPlusJetsQCDSelectionAnalyser1p5to3 = cms.EDAnalyzer("SelectionAnalyser",
    # PUWeightInput=cms.InputTag('eventWeightPU'),
    genEvtInfoProduct = cms.InputTag("generator"),
    selectionFlags=cms.VInputTag(selectionProducts),
    selectionNames=cms.vstring(selectionCuts),
)

# ttbarDecayAnalyser = cms.EDAnalyzer("SelectionAnalyser",
#     PUWeightInput=cms.InputTag('eventWeightPU'),
#     selectionFlags=cms.VInputTag(
#                 cms.InputTag( 'ttFullHadronicFilter' ),
#                 cms.InputTag( 'ttSemiLeptonicElectronFilter' ),
#                 cms.InputTag( 'ttSemiLeptonicMuonFilter' ),
#                 cms.InputTag( 'ttSemiLeptonicTauFilter' ),
#                 cms.InputTag( 'ttFullLeptonicEEFilter' ),
#                 cms.InputTag( 'ttFullLeptonicMuMuFilter' ),
#                 cms.InputTag( 'ttFullLeptonicTauTauFilter' ),
#                 cms.InputTag( 'ttFullLeptonicETauFilter' ),
#                 cms.InputTag( 'ttFullLeptonicEMuFilter' ),
#                 cms.InputTag( 'ttFullLeptonicMuTauFilter' ),
#                 ),
#     selectionNames=cms.vstring('fullHadronic',
#                                'SemiLeptonicElectron',
#                                'SemiLeptonicMuon',
#                                'SemiLeptonicTau',
#                                'FullLeptonicEE',
#                                'FullLeptonicMuMu',
#                                'FullLeptonicTauTau',
#                                'FullLeptonicETau',
#                                'FullLeptonicEMu',
#                                'FullLeptonicMuTau'),
# )

