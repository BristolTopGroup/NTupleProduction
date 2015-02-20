def setupPseudoTop( process, cms ):
	process.load( "TopQuarkAnalysis.TopEventProducers.producers.pseudoTop_cfi" )

	process.makePseudoTop = cms.Sequence( process.pseudoTop )
