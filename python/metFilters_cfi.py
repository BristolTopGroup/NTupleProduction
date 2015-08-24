def setupMETFilters(process, cms):
	process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
	process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)

	process.ApplyBaselineHBHENoiseFilter = cms.EDFilter('BooleanFlagFilter',
	   inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
	   reverseDecision = cms.bool(False)
	)

	process.HBHEFilterRerun = cms.Sequence(process.HBHENoiseFilterResultProducer * process.ApplyBaselineHBHENoiseFilter)

	process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag('offlineSlimmedPrimaryVertices'),
                                           minimumNDOF = cms.uint32(4) ,
                                           maxAbsZ = cms.double(24),
                                           maxd0 = cms.double(2)
                                           )

	process.metFilters = cms.Sequence( process.primaryVertexFilter + process.HBHEFilterRerun )