#import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *

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
                      process.eventWeightPU *
                      process.rootNTuples
                      )

if not options.printEventContent:
    process.makingNTuples.remove(process.printEventContent)
if options.useData:
    process.makingNTuples.remove(process.eventWeightPU) 

if options.useData or not options.storePDFWeights:
        process.makingNTuples.remove(process.pdfWeights)
    

process.out.SelectEvents.SelectEvents = cms.vstring('makingNTuples')

#if not makePATTuple:
#    #do not write PAT-tuple information
#    del process.outpath

