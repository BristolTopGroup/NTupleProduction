from makeTuples_cfg import *

from BristolAnalysis.NTupleTools.UnfoldingAnalysis_cff import *
setup_UnfoldingAnalysis(process, cms, options)

process.unfoldingAnalysis = cms.Path(
                      process.pdfWeights *
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix)*
                      process.unfoldingAnalysis 
                      )