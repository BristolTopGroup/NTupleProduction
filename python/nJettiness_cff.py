import FWCore.ParameterSet.Config as cms
from BristolAnalysis.NTupleTools.BristolNTuple_PFCandidates_cfi import nTuplePFCands, puppi
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

njettiness = Njettiness.clone(
    src = cms.InputTag('nTuplePFCands', 'OneJet'),
	measureDefinition = cms.uint32(4),
	beta = cms.double(2.0),
	R0 = cms.double( 0.4 ),
	Rcutoff = cms.double( 0.4 ),
	Njets=cms.vuint32(1,2,3,4,5,6),
)

addNJettiness = cms.Sequence( puppi * nTuplePFCands * njettiness )

# addNJettiness = cms.Sequence( njettiness  )
