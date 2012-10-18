#import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *
##########################################################################################
#            NTupleConfig
##########################################################################################
if not makePATTuple:
    #NTuple content
    from BristolAnalysis.NTupleTools.NTupler_cff import *
    setup_ntupler(process, cms, options, includeCA08Jets)
else:
    from BristolAnalysis.NTupleTools.PatTuple_cff import *
    setup_pattuple(process, cms, options)

process.makingNTuples = cms.Path(
                      process.pdfWeights * 
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix) * 
                      process.printEventContent * 
                      process.rootNTuples
                      )

if not options.printEventContent:
    process.makingNTuples.remove(process.printEventContent)
if options.useData or not options.storePDFWeights:
    process.makingNTuples.remove(process.pdfWeights)

process.out.SelectEvents.SelectEvents = cms.vstring('makingNTuples')

##########################################################################################
#            Unfolding Config
##########################################################################################
from BristolAnalysis.NTupleTools.UnfoldingAnalysis_cff import *
setup_UnfoldingAnalysis(process, cms, options)

process.unfoldingAnalysis = cms.Path(
                      process.pdfWeights *
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      process.EventFilters * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix)*
                      process.unfoldingAnalysisSequence 
                      )

if options.useData or not options.storePDFWeights:
    process.unfoldingAnalysis.remove(process.pdfWeights)
    
##########################################################################################
#            Selection Config
##########################################################################################
process.load('BristolAnalysis.NTupleTools.ttDecayChannelFilters_cff')
process.load('BristolAnalysis.NTupleTools.TopPairElectronPlusJets2012SelectionFilter_cfi')
process.load('BristolAnalysis.NTupleTools.TopPairMuonPlusJets2012SelectionFilter_cfi')
process.load('BristolAnalysis.NTupleTools.EventWeight_Producer_PU_cfi')
process.load('BristolAnalysis.NTupleTools.SelectionAnalyser_cfi')
#filters only in tagging mode
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
process.topPairEPlusJetsSelection.taggingMode = cms.bool(True)
process.topPairMuPlusJetsSelection.taggingMode = cms.bool(True)

process.MCFiltersInTaggingMode = cms.Sequence(process.ttFullHadronicFilter * 
#                                                     process.ttFullLeptonicFilter * 
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

process.selectionAnalysis = cms.Path(
                      process.pdfWeights * 
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
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
    process.selectionAnalysis.remove(process.ttbarDecayAnalyser)