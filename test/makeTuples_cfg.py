#import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *

if not makePATTuple:
    #NTuple content
    from BristolAnalysis.NTupleTools.NTupler_cff import *
    setup_ntupler(process, cms, options, includeCA08Jets)
else:
    from BristolAnalysis.NTupleTools.PatTuple_cff import *
    setup_pattuple(process, cms, options)
process.load('BristolAnalysis.NTupleTools.ttDecayChannelFilters_cff')
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

process.makingNTuples = cms.Path(
                      process.pdfWeights * 
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix) * 
                      process.printEventContent * 
                      process.eventWeightPU *
                      process.MCFiltersInTaggingMode *
                      process.rootNTuples
                      )

if not options.CMSSW == '44X':
    process.makingNTuples.remove(getattr(process, "producePatPFMETCorrections" + postfix))
    process.makingNTuples.remove(getattr(process, "patMETs" + postfix))

if not options.printEventContent:
    process.makingNTuples.remove(process.printEventContent)
    
if options.useData:
    process.makingNTuples.remove(process.eventWeightPU) 
    
if options.useData or not options.isTTbarMC:   
    process.makingNTuples.remove(process.MCFiltersInTaggingMode) 

if options.useData or not options.storePDFWeights:
        process.makingNTuples.remove(process.pdfWeights)
    

process.out.SelectEvents.SelectEvents = cms.vstring('makingNTuples')

#if not makePATTuple:
#    #do not write PAT-tuple information
#    del process.outpath

