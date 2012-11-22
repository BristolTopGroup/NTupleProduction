#import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *
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

if options.CMSSW == '44X':
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string('Fall11')  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string('Fall11')  
else:
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string('Summer12')  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string('Summer12')

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

if not options.CMSSW == '44X':
    process.selectionAnalysis.remove(getattr(process, "producePatPFMETCorrections" + postfix))
    process.selectionAnalysis.remove(getattr(process, "patMETs" + postfix))

if options.useData or not options.storePDFWeights:
    process.selectionAnalysis.remove(process.pdfWeights)

if options.useData or not options.isTTbarMC:   
    process.eventFiltersIntaggingMode.remove(process.MCFiltersInTaggingMode) 
    
if options.useData:
    process.selectionAnalysis.remove(process.ttbarDecayAnalyser)
    
