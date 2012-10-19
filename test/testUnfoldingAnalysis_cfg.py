#import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *

#include analysers, filters and producers for UnfoldingAnalysis
from BristolAnalysis.NTupleTools.UnfoldingAnalysis_cff import *

if options.isTTbarMC:
    setup_UnfoldingAnalysis(process, cms, options)
    process.unfoldingAnalysis = cms.Path(
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      process.EventFilters * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix)*
                      process.eventWeightPU *
                      process.unfoldingAnalysisSequence 
                      )
else:
    print 'This analysis can only run on ttbar events'
