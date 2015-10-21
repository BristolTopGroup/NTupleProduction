def setupMETFilters(process, cms):

	print '=' * 60
	print "Setting up MET filters"
	print '=' * 60

	# HBHE and HBHE Iso filters
	process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
	process.HBHENoiseFilterResultProducer.minZeros = cms.int32(99999)
	process.HBHENoiseFilterResultProducer.IgnoreTS4TS5ifJetInLowBVRegion=cms.bool(False) 
	process.HBHENoiseFilterResultProducer.defaultDecision = cms.string("HBHENoiseFilterResultRun2Loose")

	process.ApplyBaselineHBHENoiseFilter = cms.EDFilter('BooleanFlagFilter',
		inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHENoiseFilterResult'),
		reverseDecision = cms.bool(False)
	)
	process.ApplyBaselineHBHEIsoNoiseFilter = cms.EDFilter('BooleanFlagFilter',
		inputLabel = cms.InputTag('HBHENoiseFilterResultProducer','HBHEIsoNoiseFilterResult'),
		reverseDecision = cms.bool(False)
	)
	process.HBHEFilterRerun = cms.Sequence(process.HBHENoiseFilterResultProducer * process.ApplyBaselineHBHENoiseFilter) # * process.ApplyBaselineHBHEIsoNoiseFilter)

	# PV filter
	process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
		vertexCollection = cms.InputTag('offlineSlimmedPrimaryVertices'),
		minimumNDOF = cms.uint32(4) ,
		maxAbsZ = cms.double(24),
		maxd0 = cms.double(2)
	)

	# Bad EE Supercrystal filter
	process.load('RecoMET.METFilters.eeBadScFilter_cfi')
	process.eeBadScFilterv2 = process.eeBadScFilter.clone(
		EERecHitSource = cms.InputTag('reducedEgamma','reducedEERecHits',''),
		)

	# Run II Beam Halo ID filter
	# Beam Halo ID filter requires
	process.load('RecoMET.METProducers.CSCHaloData_cfi')
	process.load('RecoMET.METProducers.EcalHaloData_cfi')
	process.load('RecoMET.METProducers.HcalHaloData_cfi')
	process.load('RecoMET.METProducers.GlobalHaloData_cfi')
	process.load('RecoMET.METProducers.BeamHaloSummary_cfi')
	process.BeamHaloId = cms.Sequence(process.CSCHaloData*process.EcalHaloData*process.HcalHaloData*process.GlobalHaloData*process.BeamHaloSummary)

	process.load('RecoMET.METFilters.CSCTightHalo2015Filter_cfi')
	process.CSCTightHalo2015Filter.taggingMode = cms.bool(True)


	process.metFilters = cms.Sequence( process.primaryVertexFilter + process.HBHEFilterRerun + process.BeamHaloId + process.CSCTightHalo2015Filter + process.eeBadScFilterv2)