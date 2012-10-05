#import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *

#include analysers, filters and producers for UnfoldingAnalysis
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