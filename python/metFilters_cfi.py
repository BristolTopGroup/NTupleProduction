def setupMETFilters(process, cms):
	process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
	process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)

	process.ApplyBaselineHBHENoiseFilter = cms.EDFilter('BooleanFlagFilter',
	   inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
	   reverseDecision = cms.bool(False)
	)

	process.HBHEFilterRerun = cms.Sequence(process.HBHENoiseFilterResultProducer * process.ApplyBaselineHBHENoiseFilter)