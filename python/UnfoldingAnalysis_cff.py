def setup_UnfoldingAnalysis(process, cms, options):
    print '=' * 60
    print "Setting up UnfoldingAnalysis"
    print '=' * 60
    ######################################################################################################
    ################################## nTuple Configuration ##############################################
    ######################################################################################################
    process.load('BristolAnalysis.NTupleTools.ttDecayChannelFilters_cff')
    process.load('BristolAnalysis.NTupleTools.TopPairElectronPlusJets2012SelectionFilter_cfi')
    process.load('BristolAnalysis.NTupleTools.BTagWeight_Producer_cfi')
    process.load('TopAnalysis.TopUtils.EventWeightPU_cfi')
    process.load('BristolAnalysis.NTupleTools.UnfoldingAnalyser_cfi')
    
    #filters only in tagging mode
    process.ttFullHadronicFilter.taggingMode = cms.bool(True)
    process.ttFullLeptonicFilter.taggingMode = cms.bool(True)
    process.ttSemiLeptonicElectronFilter.taggingMode = cms.bool(True)
    process.ttSemiLeptonicMuonFilter.taggingMode = cms.bool(True)
    process.ttSemiLeptonicTauFilter.taggingMode = cms.bool(True)
    process.topPairEPlusJetsSelection.taggingMode = cms.bool(True)
    
    selectionPrefix = 'TopPairElectronPlusJets2012Selection.'
    process.topPairEPlusJetsSelection.prefix = cms.untracked.string(selectionPrefix)
    
    process.eventWeightBtag.numberOfTagsInput = cms.InputTag(selectionPrefix + 'NumberOfBtags')
    process.eventWeightBtag.jetInput = cms.InputTag(selectionPrefix + 'cleanedJets')
    process.eventWeightBtag.targetBtagMultiplicity = cms.uint32(2) #>=2
    process.eventWeightBtag.BJetSystematic = cms.int32(0)
    
    #PU event weight
    process.eventWeightPU.MCSampleTag = cms.string("Fall11") # valid identifier: Fall11, Summer11, Summer12                             
    process.eventWeightPU.MCSampleFile = cms.FileInPath("TopAnalysis/TopUtils/data/MC_PUDist_Default2011.root")
    #process.eventWeightPU.MCSampleFile = cms.FileInPath("TopAnalysis/TopUtils/data/MC_PUDist_Summer2012.root")
    process.eventWeightPU.MCSampleHistoName = cms.string("histo_Fall11_true")
    process.eventWeightPU.DataFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011_truth_finebin.root")
    process.eventWeightPU.DataHistoName = cms.string("pileup")
    process.eventWeightPU.CreateWeight3DHisto = cms.bool(False)
    process.eventWeightPU.Weight3DHistoFile = cms.FileInPath("Weight3D_Fall11.root")
    
    
    process.eventFiltersIntaggingMode = cms.Sequence(process.ttFullHadronicFilter*
                                                     process.ttFullLeptonicFilter*
                                                     process.ttSemiLeptonicElectronFilter*
                                                     process.ttSemiLeptonicMuonFilter*
                                                     process.ttSemiLeptonicTauFilter*
                                                     process.topPairEPlusJetsSelection )
    
    process.unfoldingAnalysisSequence = cms.Sequence(process.eventFiltersIntaggingMode*
                                                     process.eventWeightBtag*
                                                     process.eventWeightPU*
                                                     process.unfoldingAnalyserElectronChannel*
                                                     process.unfoldingAnalyserMuonChannel)
    
    
    
    #if not TTJet in options.dataType
    
