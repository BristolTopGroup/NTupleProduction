def setupPseudoTop( process, cms ):
	process.load( "TopQuarkAnalysis.TopEventProducers.producers.pseudoTop_cfi" )

	# Default in CMSSW is 0.5 (relic from run 1)
	process.pseudoTop.jetConeSize = cms.double(0.4)
	# Current default is 80.2
	process.pseudoTop.wMass = cms.double(80.4)

	process.makePseudoTop = cms.Sequence( process.pseudoTop )
