def setup_UnfoldingAnalysis(process, cms, options):
    print '=' * 60
    print "Setting up UnfoldingAnalysis"
    print '=' * 60
    ######################################################################################################
    ################################## Configuration ##############################################
    ######################################################################################################
    process.load('BristolAnalysis.NTupleTools.ttDecayChannelFilters_cff')
    process.load('BristolAnalysis.NTupleTools.TopPairElectronPlusJets2012SelectionFilter_cfi')
    process.load('BristolAnalysis.NTupleTools.BTagWeight_Producer_cfi')
    
    process.load('BristolAnalysis.NTupleTools.UnfoldingAnalyser_cfi')
    
    #filters only in tagging mode
    process.ttFullHadronicFilter.taggingMode = cms.bool(True)
    process.ttFullLeptonicFilter.taggingMode = cms.bool(True)
    process.ttSemiLeptonicElectronFilter.taggingMode = cms.bool(True)
    process.ttSemiLeptonicMuonFilter.taggingMode = cms.bool(True)
    process.ttSemiLeptonicTauFilter.taggingMode = cms.bool(True)
    process.topPairEPlusJetsSelection.taggingMode = cms.bool(True)
    
    electronselectionPrefix = 'TopPairElectronPlusJets2012Selection.'
    process.topPairEPlusJetsSelection.prefix = cms.untracked.string(electronselectionPrefix)
    
    process.eventWeightBtag.numberOfTagsInput = cms.InputTag("topPairEPlusJetsSelection", electronselectionPrefix + 'NumberOfBtags', 'PAT')
    process.eventWeightBtag.jetInput = cms.InputTag("topPairEPlusJetsSelection", electronselectionPrefix + 'cleanedJets', 'PAT')
    process.eventWeightBtag.targetBtagMultiplicity = cms.uint32(2) #will calculate the weight for b-tag multiplicity >=2
    process.eventWeightBtag.BJetSystematic = cms.int32(0)
    process.unfoldingAnalyserElectronChannel.selectionFlagInput = cms.InputTag("topPairEPlusJetsSelection", electronselectionPrefix + 'FullSelection', 'PAT')
#TODO: change to muon selection
    process.unfoldingAnalyserMuonChannel.selectionFlagInput = cms.InputTag("topPairEPlusJetsSelection", electronselectionPrefix + 'FullSelection', 'PAT')
    
    #PU event weight
    if options.CMSSW == '44X':
#        process.eventWeightPU.MCSampleTag = cms.string("Fall11") # valid identifier: Fall11, Summer12
        process.topPairEPlusJetsSelection.MCSampleTag = cms.string('Fall11')    
    else:
#        process.eventWeightPU.MCSampleTag = cms.string("Summer12")
#        process.eventWeightPU.MCSampleFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Summer2012.root")
        #need to figure that one out
#        process.eventWeightPU.DataFile = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Summer2012.root")
        process.topPairEPlusJetsSelection.MCSampleTag = cms.string('Summer12')  
    
    process.MCFiltersInTaggingMode = cms.Sequence(process.ttFullHadronicFilter * 
                                                   process.ttFullLeptonicFilter * 
                                                     process.ttSemiLeptonicElectronFilter * 
                                                     process.ttSemiLeptonicMuonFilter * 
                                                     process.ttSemiLeptonicTauFilter)
    
    process.eventFiltersIntaggingMode = cms.Sequence(process.MCFiltersInTaggingMode * 
                                                     process.topPairEPlusJetsSelection)
    
    process.unfoldingAnalysisSequence = cms.Sequence(process.eventFiltersIntaggingMode * 
                                                     process.eventWeightBtag * 
						                             process.printEventContent * 
                                                     process.unfoldingAnalyserElectronChannel * 
                                                     process.unfoldingAnalyserMuonChannel)
    
    
    if not options.printEventContent:
        process.unfoldingAnalysisSequence.remove(process.printEventContent)
        

    if options.useData or not options.isTTbarMC:
        process.eventFiltersIntaggingMode.remove(process.MCFiltersInTaggingMode)
    #if not TTJet in options.dataType
    
