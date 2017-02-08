def setup_electrons(process, cms, options):
	print '=' * 60
	print "Setting up Electrons and ID"
	print '=' * 60
	isMC = not options.isData
	##########################################################
	### Applying the Electron Regression #####################
	##########################################################
	# TODO PROPERLY
	# Apply the regression from local sqlite file
	# from EgammaAnalysis.ElectronTools.regressionWeights_local_cfi import GBRDWrapperRcd
	# process.regressions           = GBRDWrapperRcd
	# process.es_prefer_regressions = cms.ESPrefer('PoolDBESSource','regressions')
	# process.load('EgammaAnalysis.ElectronTools.regressionApplication_cff')

	# Apply the regression from a remote database
	# from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights
	# process = regressionWeights(process)
	# process.load('EgammaAnalysis.ElectronTools.regressionApplication_cff')

	# Apply from GT
	process.load('EgammaAnalysis.ElectronTools.regressionApplication_cff')

	process.electronRegression = cms.Sequence(process.regressionApplication)

	##########################################################
	### Applying the Electron Smearer ########################
	##########################################################
	if isMC:
	    process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
	        calibratedPatElectrons  = cms.PSet(
	            initialSeed = cms.untracked.uint32(81),
	            engineName = cms.untracked.string('TRandom3'),
	        ),
	    )
	process.load('EgammaAnalysis.ElectronTools.calibratedElectronsRun2_cfi')
	process.selectedSlimmedElectrons = cms.EDFilter("PATElectronSelector", 
	    src = cms.InputTag("slimmedElectrons"), 
	    cut = cms.string("pt > 5 && abs(eta)<2.5") 
	)

	process.calibratedPatElectrons = cms.EDProducer("CalibratedPatElectronProducerRun2",
	    electrons = cms.InputTag("selectedSlimmedElectrons"),
	    gbrForestName = cms.string('gedelectron_p4combination_25ns'),
	    isMC = cms.bool(isMC),
	    isSynchronization = cms.bool(False),
	    correctionFile = cms.string("EgammaAnalysis/ElectronTools/data/ScalesSmearings/Winter_2016_reReco_v1_ele"),
	)
	# process.smearedElectrons = cms.Sequence( process.selectedSlimmedElectrons + process.calibratedPatElectrons)
	process.smearedElectrons = cms.Sequence( process.electronRegression + process.selectedSlimmedElectrons + process.calibratedPatElectrons)

	##########################################################
	### Applying the ID ######################################
	##########################################################
	from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
	# Switch ValueMap Producer to use calibrated Electrons
	process.load("RecoEgamma.ElectronIdentification.ElectronIDValueMapProducer_cfi")
	process.electronIDValueMapProducer.srcMiniAOD = cms.InputTag('calibratedPatElectrons')

	# turn on VID producer, indicate data format  to be
	# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
	dataFormat = DataFormat.MiniAOD
	switchOnVIDElectronIdProducer(process, dataFormat)

	# Switch egmGsfElectronIDs from switchOnVIDElectronIdProducer to use calibrated Electrons
	process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag("calibratedPatElectrons")

	# define which IDs we want to produce
	my_id_modules = [
		# 'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',
		# 'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',
		'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Summer16_80X_V1_cff',
		# 'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',
	]

	#add them to the VID producer
	for idmod in my_id_modules:
		setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
