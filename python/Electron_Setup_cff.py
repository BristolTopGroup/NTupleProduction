def setup_electrons(process, cms, options):
	print '=' * 60
	print "Setting up Electrons and ID"
	print '=' * 60
	isMC = not options.isData
	##########################################################
	### Applying the Electron Regression #####################
	##########################################################

	from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights
	process = regressionWeights(process)
	process.load('EgammaAnalysis.ElectronTools.regressionApplication_cff')

	##########################################################
	### Applying the Electron Smearer ########################
	##########################################################
	process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
		calibratedPatElectrons  = cms.PSet(
			initialSeed = cms.untracked.uint32(81),
			engineName = cms.untracked.string('TRandom3'),
		),
	)
	process.load('EgammaAnalysis.ElectronTools.calibratedPatElectronsRun2_cfi')
	process.calibratedPatElectrons.isMC = cms.bool(isMC)

	##########################################################
	### Applying the ID ######################################
	##########################################################
	process.load("RecoEgamma.ElectronIdentification.ElectronIDValueMapProducer_cfi")

	from PhysicsTools.SelectorUtils.tools.vid_id_tools import *

	dataFormat = DataFormat.MiniAOD
	switchOnVIDElectronIdProducer(process, dataFormat)

	# define which IDs we want to produce
	my_id_modules = [
		'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
		'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff',
	]

	#add them to the VID producer
	for idmod in my_id_modules:
		setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
	
	process.selectedElectrons = cms.EDFilter("PATElectronSelector", 
	    src = cms.InputTag("calibratedPatElectrons"), 
	    cut = cms.string("pt > 5 && abs(eta)<2.5") 
	)

	process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag("selectedElectrons")
	process.electronIDValueMapProducer.srcMiniAOD = cms.InputTag('selectedElectrons')
	process.electronRegressionValueMapProducer.srcMiniAOD = cms.InputTag('selectedElectrons')

	process.processedElectrons = cms.Sequence( process.regressionApplication + process.calibratedPatElectrons + process.selectedElectrons + process.egmGsfElectronIDSequence + process.electronIDValueMapProducer)



