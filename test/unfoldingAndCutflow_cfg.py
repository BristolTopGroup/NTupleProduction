#import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *
##########################################################################################
#            General
##########################################################################################
process.load('BristolAnalysis.NTupleTools.ttDecayChannelFilters_cff')
process.load('BristolAnalysis.NTupleTools.TopPairElectronPlusJets2012SelectionFilter_cfi')
process.load('BristolAnalysis.NTupleTools.TopPairMuonPlusJets2012SelectionFilter_cfi')
 #filters only in tagging mode
process.topPairEPlusJetsSelection.taggingMode = cms.bool(True)
process.topPairMuPlusJetsSelection.taggingMode = cms.bool(True)

process.ttFullHadronicFilter.taggingMode = cms.bool(True)
process.ttFullLeptonicFilter.taggingMode = cms.bool(True)
process.ttSemiLeptonicElectronFilter.taggingMode = cms.bool(True)
process.ttSemiLeptonicMuonFilter.taggingMode = cms.bool(True)
process.ttSemiLeptonicTauFilter.taggingMode = cms.bool(True)
process.ttFullLeptonicEEFilter.taggingMode = cms.bool(True)
process.ttFullLeptonicMuMuFilter.taggingMode = cms.bool(True)
process.ttFullLeptonicTauTauFilter.taggingMode = cms.bool(True)
process.ttFullLeptonicETauFilter.taggingMode = cms.bool(True)
process.ttFullLeptonicEMuFilter.taggingMode = cms.bool(True)
process.ttFullLeptonicMuTauFilter.taggingMode = cms.bool(True)

if options.CMSSW == '44X':
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string('Fall11')  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string('Fall11')  
else:
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string('Summer12')  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string('Summer12')

electronselectionPrefix = 'TopPairElectronPlusJets2012Selection.'
muonselectionPrefix = 'TopPairMuonPlusJets2012Selection.'
process.topPairEPlusJetsSelection.prefix = cms.untracked.string(electronselectionPrefix)
process.topPairMuPlusJetsSelection.prefix = cms.untracked.string(muonselectionPrefix)

process.MCFiltersInTaggingMode = cms.Sequence(process.ttFullHadronicFilter * 
                                                     process.ttFullLeptonicFilter * 
                                                     process.ttSemiLeptonicElectronFilter * 
                                                     process.ttSemiLeptonicMuonFilter * 
                                                     process.ttSemiLeptonicTauFilter * 
                                                     process.ttFullLeptonicEEFilter * 
                                                     process.ttFullLeptonicMuMuFilter * 
                                                     process.ttFullLeptonicTauTauFilter * 
                                                     process.ttFullLeptonicETauFilter * 
                                                     process.ttFullLeptonicEMuFilter * 
                                                     process.ttFullLeptonicMuTauFilter)

process.eventFiltersIntaggingMode = cms.Sequence(process.MCFiltersInTaggingMode * 
                                                     process.topPairEPlusJetsSelection *
                                                     process.topPairMuPlusJetsSelection)

##########################################################################################
#            Unfolding Config
##########################################################################################
process.load('BristolAnalysis.NTupleTools.BTagWeight_Producer_cfi')
process.load('BristolAnalysis.NTupleTools.UnfoldingAnalyser_cfi')
process.eventWeightBtagEPlusJets = process.eventWeightBtag.clone(
            numberOfTagsInput = cms.InputTag("topPairEPlusJetsSelection", electronselectionPrefix + 'NumberOfBtags', 'PAT'),
            jetInput = cms.InputTag("topPairEPlusJetsSelection", electronselectionPrefix + 'cleanedJets', 'PAT'),
            targetBtagMultiplicity = cms.uint32(2), #will calculate the weight for b-tag multiplicity >=2
            BJetSystematic = cms.int32(0)
            )
process.eventWeightBtagMuPlusJets = process.eventWeightBtagEPlusJets.clone(
            numberOfTagsInput = cms.InputTag("topPairMuPlusJetsSelection", muonselectionPrefix + 'NumberOfBtags', 'PAT')  ,  
            jetInput = cms.InputTag("topPairMuPlusJetsSelection", muonselectionPrefix + 'cleanedJets', 'PAT'),       
                                                              )
process.unfoldingAnalyserElectronChannel.selectionFlagInput = cms.InputTag("topPairEPlusJetsSelection", electronselectionPrefix + 'FullSelection', 'PAT')
process.unfoldingAnalyserElectronChannel.BtagWeightInput = cms.InputTag( 'eventWeightBtagEPlusJets' )
process.unfoldingAnalyserMuonChannel.selectionFlagInput = cms.InputTag("topPairMuPlusJetsSelection", muonselectionPrefix + 'FullSelection', 'PAT')
process.unfoldingAnalyserMuonChannel.BtagWeightInput = cms.InputTag( 'eventWeightBtagMuPlusJets' )
    
process.unfoldingAnalysisSequence = cms.Sequence(process.eventFiltersIntaggingMode * 
                                                     process.eventWeightBtagEPlusJets *
                                                     process.eventWeightBtagMuPlusJets *  
                                                     process.printEventContent * 
                                                     process.unfoldingAnalyserElectronChannel * 
                                                     process.unfoldingAnalyserMuonChannel)
    
    
if not options.printEventContent:
    process.unfoldingAnalysisSequence.remove(process.printEventContent)

if options.isTTbarMC:
    process.unfoldingAnalysis = cms.Path(
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.pfMEtSysShiftCorrSequence *
                      process.patseq * 
                      process.EventFilters * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix)*
                      process.eventWeightPU *
                      process.unfoldingAnalysisSequence 
                      )
    if not options.setupMETmanually:
        process.unfoldingAnalysis.remove(getattr(process, "producePatPFMETCorrections" + postfix))
        process.unfoldingAnalysis.remove(getattr(process, "patMETs" + postfix))

##########################################################################################
#            Selection Config
##########################################################################################
process.load('BristolAnalysis.NTupleTools.SelectionAnalyser_cfi')

process.selectionAnalysis = cms.Path(
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.pfMEtSysShiftCorrSequence *
                      process.patseq * 
                      process.EventFilters * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix) * 
                      process.eventFiltersIntaggingMode * 
                      process.eventWeightPU * 
                      process.ttbarDecayAnalyser * 
                      process.topPairEPlusJetsSelectionAnalyser *
                      process.topPairMuPlusJetsSelectionAnalyser
                      )

if options.useData:
    process.eventFiltersIntaggingMode.remove(process.MCFiltersInTaggingMode)
if options.useData or not options.isTTbarMC:
    process.selectionAnalysis.remove(process.ttbarDecayAnalyser)
if not options.setupMETmanually:
    process.selectionAnalysis.remove(getattr(process, "producePatPFMETCorrections" + postfix))
    process.selectionAnalysis.remove(getattr(process, "patMETs" + postfix))