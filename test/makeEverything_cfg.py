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