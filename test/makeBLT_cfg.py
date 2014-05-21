# import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *
#NTuple content
from BristolAnalysis.NTupleTools.NTupler_cff import *
setup_ntupler(process, cms, options)

##########################################################################################
#            General
##########################################################################################
process.load( 'TopQuarkAnalysis.TopSkimming.TtFullyHadronicFilter_cfi' )
process.load( 'TopQuarkAnalysis.TopSkimming.TtFullyLeptonicFilter_cfi' )
process.load( 'TopQuarkAnalysis.TopSkimming.TtSemiLeptonicFilter_cfi' )

process.load( 'BristolAnalysis.NTupleTools.TopPairElectronPlusJets2012SelectionFilter_cfi' )
process.load( 'BristolAnalysis.NTupleTools.TopPairMuonPlusJets2012SelectionFilter_cfi' )

# Selection filters in tagging mode for monitoring cut flow
process.topPairEPlusJetsSelection.taggingMode = cms.bool( True )
process.topPairMuPlusJetsSelection.taggingMode = cms.bool( True )
# Selection filters that will actually apply selection
process.topPairEPlusJetsSelectionApply = process.topPairEPlusJetsSelection.clone( taggingMode = cms.bool(False) )
process.topPairMuPlusJetsSelectionApply = process.topPairMuPlusJetsSelection.clone( taggingMode = cms.bool(False) )

# Filters characterizing tt decay in tagging mode
process.ttFullHadronicFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicFilter.taggingMode = cms.bool( True )
process.ttSemiLeptonicElectronFilter.taggingMode = cms.bool( True )
process.ttSemiLeptonicMuonFilter.taggingMode = cms.bool( True )
process.ttSemiLeptonicTauFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicEEFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicMuMuFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicTauTauFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicETauFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicEMuFilter.taggingMode = cms.bool( True )
process.ttFullLeptonicMuTauFilter.taggingMode = cms.bool( True )

if options.isMCatNLO:
    process.ttFullHadronicFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicFilter.useMCATNLO = cms.bool( True )
    process.ttSemiLeptonicElectronFilter.useMCATNLO = cms.bool( True )
    process.ttSemiLeptonicMuonFilter.useMCATNLO = cms.bool( True )
    process.ttSemiLeptonicTauFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicEEFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicMuMuFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicTauTauFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicETauFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicEMuFilter.useMCATNLO = cms.bool( True )
    process.ttFullLeptonicMuTauFilter.useMCATNLO = cms.bool( True )

if options.CMSSW == '44X':
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string( 'Fall11' )  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string( 'Fall11' )  
else:
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string( 'Summer12' )  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string( 'Summer12' )

electronselectionPrefix = 'TopPairElectronPlusJets2012Selection.'
muonselectionPrefix = 'TopPairMuonPlusJets2012Selection.'
process.topPairEPlusJetsSelection.prefix = cms.untracked.string( electronselectionPrefix )
process.topPairMuPlusJetsSelection.prefix = cms.untracked.string( muonselectionPrefix )

process.load( "TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff" )

process.MCFiltersInTaggingMode = cms.Sequence( process.makeGenEvt * 
                                                     process.ttFullHadronicFilter * 
                                                     process.ttFullLeptonicFilter * 
                                                     process.ttSemiLeptonicElectronFilter * 
                                                     process.ttSemiLeptonicMuonFilter * 
                                                     process.ttSemiLeptonicTauFilter * 
                                                     process.ttFullLeptonicEEFilter * 
                                                     process.ttFullLeptonicMuMuFilter * 
                                                     process.ttFullLeptonicTauTauFilter * 
                                                     process.ttFullLeptonicETauFilter * 
                                                     process.ttFullLeptonicEMuFilter * 
                                                     process.ttFullLeptonicMuTauFilter )

process.eventFiltersIntaggingMode = cms.Sequence( process.MCFiltersInTaggingMode )

##########################################################################################
#            Selection Config
##########################################################################################
process.load( 'BristolAnalysis.NTupleTools.SelectionAnalyser_cfi' )

# Common things you want to run on all events
process.commonSequence = cms.Sequence(
                      process.pdfWeights * 
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.pfMEtSysShiftCorrSequence * 
                      process.patseq * 
                      process.EventFilters * 
                      getattr( process, "producePatPFMETCorrections" + postfix ) * 
                      getattr( process, "patMETs" + postfix ) * 
                      process.eventFiltersIntaggingMode *
                      process.eventWeightPU *
                      process.ttbarDecayAnalyser
                      )

#===============================================================================
# Electron channel
#===============================================================================

# Copy ntuple config so we can change some of the inputs
# And also have different input collections for the two channels
process.rootNTuplesEPlusJets = copy.copy( process.rootNTuples )
process.rootTupleTreeEPlusJets = process.rootTupleTree.clone( treeName='ePlusJetsTree' )
process.rootTupleTreeEPlusJets.outputCommands.append('keep *_rootTupleGlobalEventVarsEPlusJets*_*_*')
process.rootTupleTreeEPlusJets.outputCommands.append('keep *_rootTuplePF2PATJetsEPlusJets_*_*')
process.rootTupleTreeEPlusJets.outputCommands.append('drop *_rootTupleVertex_*_*')
process.rootTupleTreeEPlusJets.outputCommands.append('drop *_nTuplePFMuons_*_*')
process.rootTupleTreeEPlusJets.outputCommands.append('drop *_rootTuplePFElectrons_*_*')
process.rootNTuplesEPlusJets.remove( process.rootTupleTree )
# Add global event variables to ntuple
process.rootTupleGlobalEventVarsEPlusJets = process.rootTupleGlobalEventVars.clone( 
                                                                                   signalLeptonInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.signalElectron'), 
                                                                                   Channel='EPlusJets', 
                                                                                   metInputTag=cms.InputTag('patMETsPFlow'),
                                                                                   Prefix='Event.',
                                                                                   signalLeptonIndexInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.signalElectronIndex'),
                                                                                   Suffix='.patMETsPFlow',
                                                                                   )
process.rootTupleGlobalEventVarsEPlusJetsPatType1CorrectedPFMet = process.rootTupleGlobalEventVars.clone( 
                                                                                   signalLeptonInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.signalElectron'), 
                                                                                   metInputTag=cms.InputTag('patType1CorrectedPFMet'),
                                                                                   Channel='EPlusJets', 
                                                                                   Prefix='Event.',
                                                                                   signalLeptonIndexInputTag=cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.signalElectronIndex'),
                                                                                   Suffix='.patType1CorrectedPFMet',
                                                                                   )
process.rootNTuplesEPlusJets *= process.rootTupleGlobalEventVarsEPlusJets
process.rootNTuplesEPlusJets *= process.rootTupleGlobalEventVarsEPlusJetsPatType1CorrectedPFMet
process.rootNTuplesEPlusJets *= process.rootTupleTreeEPlusJets

# Use the jet collection produced by the selection filter in tagging mode for calculation of HT etc.
process.rootTupleGlobalEventVarsEPlusJets.jetInputTag = cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.cleanedJets')
# Use signal electrons for ST etc,
process.rootTupleGlobalEventVarsEPlusJets.signalLeptonIndexInputTag = cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.signalElectron')
process.rootTupleGlobalEventVarsEPlusJets.signalLeptonIndexInputTag = cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.signalElectronIndex')

# Same for global variables calculated with other MET
process.rootTupleGlobalEventVarsEPlusJetsPatType1CorrectedPFMet.jetInputTag = cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.cleanedJets')
process.rootTupleGlobalEventVarsEPlusJetsPatType1CorrectedPFMet.signalLeptonIndexInputTag = cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.signalElectron')
process.rootTupleGlobalEventVarsEPlusJetsPatType1CorrectedPFMet.signalLeptonIndexInputTag = cms.InputTag('topPairEPlusJetsSelection', 'TopPairElectronPlusJets2012Selection.signalElectronIndex')

# Replace jet collection that ends up in ntuple to cleaned collection
process.rootTuplePF2PATJetsEPlusJets = process.rootTuplePF2PATJets.clone( 
                                                                         InputTag=cms.InputTag("topPairEPlusJetsSelection", 'TopPairElectronPlusJets2012Selection.cleanedJets'), 
                                                                         Prefix='cleanedJetsPFlowEPlusJets.' )
process.rootNTuplesEPlusJets.replace( process.rootTuplePF2PATJets, process.rootTuplePF2PATJetsEPlusJets )

# Run selection twice.  First time in tagging mode so we can run the selection analyser
# and get meaningful results.
# Then run selection and reject events
process.ePlusJetsSelection = cms.Path( 
                      process.commonSequence *
                      process.topPairEPlusJetsSelection *
                      process.topPairEPlusJetsSelectionAnalyser *
                      process.topPairEPlusJetsSelectionApply *
                      process.rootNTuplesEPlusJets
                      )

#===============================================================================
# Muon channel
#===============================================================================
# Same as above
process.rootNTuplesMuPlusJets = copy.copy( process.rootNTuples )
process.rootTupleTreeMuPlusJets = process.rootTupleTree.clone( treeName='muPlusJetsTree' )
process.rootTupleTreeMuPlusJets.outputCommands.append('keep *_rootTupleGlobalEventVarsMuPlusJets*_*_*')
process.rootTupleTreeMuPlusJets.outputCommands.append('keep *_rootTuplePF2PATJetsMuPlusJets_*_*')
process.rootTupleTreeMuPlusJets.outputCommands.append('drop *_rootTupleVertex_*_*')
process.rootTupleTreeMuPlusJets.outputCommands.append('drop *_nTuplePFMuons_*_*')
process.rootTupleTreeMuPlusJets.outputCommands.append('drop *_rootTuplePFElectrons_*_*')
process.rootNTuplesMuPlusJets.remove( process.rootTupleTree )
process.rootTupleGlobalEventVarsMuPlusJets = process.rootTupleGlobalEventVars.clone( 
                                                                                    signalLeptonInputTag=cms.InputTag('topPairMuPlusJetsSelection', 'TopPairMuonPlusJets2012Selection.signalMuon'), 
                                                                                    Channel='MuPlusJets',
                                                                                    metInputTag=cms.InputTag('patMETsPFlow'),
                                                                                    Prefix='Event.',
                                                                                    signalLeptonIndexInputTag=cms.InputTag('topPairMuPlusJetsSelection', 'TopPairMuonPlusJets2012Selection.signalMuonIndex'),
                                                                                    Suffix='.patMETsPFlow',
                                                                                    )
process.rootTupleGlobalEventVarsMuPlusJetsPatType1CorrectedPFMet = process.rootTupleGlobalEventVars.clone( 
                                                                                    signalLeptonInputTag=cms.InputTag('topPairMuPlusJetsSelection', 'TopPairMuonPlusJets2012Selection.signalMuon'), 
                                                                                    Channel='MuPlusJets',
                                                                                    metInputTag=cms.InputTag('patType1CorrectedPFMet'),
                                                                                    Prefix='Event.',
                                                                                    signalLeptonIndexInputTag=cms.InputTag('topPairMuPlusJetsSelection', 'TopPairMuonPlusJets2012Selection.signalMuonIndex'),
                                                                                    Suffix='.patType1CorrectedPFMet',
                                                                                    )
process.rootNTuplesMuPlusJets *= process.rootTupleGlobalEventVarsMuPlusJets
process.rootNTuplesMuPlusJets *= process.rootTupleGlobalEventVarsMuPlusJetsPatType1CorrectedPFMet
process.rootNTuplesMuPlusJets *= process.rootTupleTreeMuPlusJets
process.rootTupleGlobalEventVarsMuPlusJets.jetInputTag = cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.cleanedJets')
process.rootTupleGlobalEventVarsMuPlusJets.signalLeptonInputTag = cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.signalMuon')
process.rootTupleGlobalEventVarsMuPlusJets.signalLeptonIndexInputTag = cms.InputTag('topPairMuPlusJetsSelection', 'TopPairMuonPlusJets2012Selection.signalMuonIndex')
process.rootTupleGlobalEventVarsMuPlusJetsPatType1CorrectedPFMet.jetInputTag = cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.cleanedJets')
process.rootTupleGlobalEventVarsMuPlusJetsPatType1CorrectedPFMet.signalLeptonInputTag = cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.signalMuon')
process.rootTupleGlobalEventVarsMuPlusJetsPatType1CorrectedPFMet.signalLeptonIndexInputTag = cms.InputTag('topPairMuPlusJetsSelection', 'TopPairMuonPlusJets2012Selection.signalMuonIndex')

process.rootTuplePF2PATJetsMuPlusJets = process.rootTuplePF2PATJets.clone( 
                                                                          InputTag=cms.InputTag("topPairMuPlusJetsSelection", 'TopPairMuonPlusJets2012Selection.cleanedJets'), 
                                                                          Prefix='cleanedJetsPFlowMuPlusJets.' )
process.rootNTuplesMuPlusJets.replace( process.rootTuplePF2PATJets, process.rootTuplePF2PATJetsMuPlusJets )

process.muPlusJetsSelection = cms.Path( 
                      process.commonSequence *
                      process.topPairMuPlusJetsSelection *
                      process.topPairMuPlusJetsSelectionAnalyser *
                      process.topPairMuPlusJetsSelectionApply *
                      process.rootNTuplesMuPlusJets
                      )

if options.useData or not options.isTTbarMC:
    process.eventFiltersIntaggingMode.remove( process.MCFiltersInTaggingMode )
    
if options.useData or not options.isTTbarMC:
    process.commonSequence.remove( process.ttbarDecayAnalyser )

if not options.setupMETmanually:
    process.commonSequence.remove( getattr( process, "producePatPFMETCorrections" + postfix ) )
    process.commonSequence.remove( getattr( process, "patMETs" + postfix ) )

if not options.printEventContent:
    process.commonSequence.remove(process.printEventContent)
    
if options.useData or not options.storePDFWeights:
        process.commonSequence.remove(process.pdfWeights)

# Keep pu weights for data, so 
# if options.useData:
#     process.commonSequence.remove(process.eventWeightPU) 