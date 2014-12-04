def setupHitFit( process, cms ):
	process.load("TopQuarkAnalysis.TopHitFit.TtSemiLepHitFitProducer_Muons_cfi")
	process.hitFitTtSemiLepEventMuon = process.hitFitTtSemiLepEvent.clone()
	process.hitFitTtSemiLepEventMuon.jets = cms.InputTag( 'slimmedJets' )
	process.hitFitTtSemiLepEventMuon.leps = cms.InputTag( 'slimmedMuons' )
	process.hitFitTtSemiLepEventMuon.mets = cms.InputTag( 'slimmedMETs' )
	process.hitFitTtSemiLepEventMuon.bTagAlgo = cms.string( 'combinedInclusiveSecondaryVertexV2BJetTags' )

	process.load("TopQuarkAnalysis.TopHitFit.TtSemiLepHitFitProducer_Electrons_cfi")
	process.hitFitTtSemiLepEventElectron = process.hitFitTtSemiLepEvent.clone()
	process.hitFitTtSemiLepEventElectron.jets = cms.InputTag( 'slimmedJets' )
	process.hitFitTtSemiLepEventElectron.leps = cms.InputTag( 'slimmedElectrons' )
	process.hitFitTtSemiLepEventElectron.mets = cms.InputTag( 'slimmedMETs' )
	process.hitFitTtSemiLepEventElectron.bTagAlgo = cms.string( 'combinedInclusiveSecondaryVertexV2BJetTags' )