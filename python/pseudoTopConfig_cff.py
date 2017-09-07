def setupPseudoTop( process, cms ):
	process.load('GeneratorInterface.RivetInterface.mergedGenParticles_cfi')

	process.load('GeneratorInterface.RivetInterface.genParticles2HepMC_cfi')
	process.genParticles2HepMC.genParticles = cms.InputTag("mergedGenParticles")
	process.genParticles2HepMC.genEventInfo = cms.InputTag("generator")

	process.load( "TopQuarkAnalysis.TopEventProducers.producers.pseudoTop_cfi" )
	process.pseudoTop.minJetPt = cms.double(20)
	process.pseudoTop.maxLeptonEta = cms.double(2.4)
	process.pseudoTop.runTopReconstruction = cms.bool(False)

	process.load('TopQuarkAnalysis.BFragmentationAnalyzer.bfragWgtProducer_cfi')
	process.makePseudoTop = cms.Sequence( process.mergedGenParticles * process.genParticles2HepMC * process.pseudoTop * process.bfragWgtProducer )
