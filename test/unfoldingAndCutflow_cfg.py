# import default nTuple stub
from BristolAnalysis.NTupleTools.NTupleTools_cff import *

##########################################################################################
#            General
##########################################################################################
process.load( 'TopQuarkAnalysis.TopSkimming.TtFullyHadronicFilter_cfi' )
process.load( 'TopQuarkAnalysis.TopSkimming.TtFullyLeptonicFilter_cfi' )
process.load( 'TopQuarkAnalysis.TopSkimming.TtSemiLeptonicFilter_cfi' )

process.load( 'BristolAnalysis.NTupleTools.TopPairElectronPlusJetsSelectionFilter_cfi' )
process.load( 'BristolAnalysis.NTupleTools.TopPairMuonPlusJetsSelectionFilter_cfi' )
 # filters only in tagging mode
process.topPairEPlusJetsSelection.taggingMode = cms.bool( True )
process.topPairMuPlusJetsSelection.taggingMode = cms.bool( True )

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
elif options.CMSSW == '53X' and options.centreOfMassEnergy == 8:
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string( 'Summer12' )  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string( 'Summer12' )
elif options.CMSSW == '53X' and options.centreOfMassEnergy == 7:
    process.topPairEPlusJetsSelection.MCSampleTag = cms.string( 'Summer11Leg' )  
    process.topPairMuPlusJetsSelection.MCSampleTag = cms.string( 'Summer11Leg' )

if options.applyZselection:
    process.topPairEPlusJetsSelection.tagAndProbeStudies = cms.bool( True )
    process.topPairMuPlusJetsSelection.tagAndProbeStudies = cms.bool( True )

if options.dropTriggerSelection:
    process.topPairEPlusJetsSelection.dropTriggerSelection = cms.bool( True )
    process.topPairMuPlusJetsSelection.dropTriggerSelection = cms.bool( True )

electronselectionPrefix = 'TopPairElectronPlusJetsSelection.'
muonselectionPrefix = 'TopPairMuonPlusJetsSelection.'

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

process.eventFiltersIntaggingMode = cms.Sequence( process.MCFiltersInTaggingMode * 
                                                     process.topPairEPlusJetsSelection * 
                                                     process.topPairMuPlusJetsSelection )

##########################################################################################
#            Unfolding Config
##########################################################################################
process.load( 'BristolAnalysis.NTupleTools.BTagWeight_Producer_cfi' )
process.load( 'BristolAnalysis.NTupleTools.UnfoldingAnalyser_cfi' )
process.eventWeightBtagEPlusJets = process.eventWeightBtag.clone( 
            numberOfTagsInput = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'NumberOfBtags', 'PAT' ),
            jetInput = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'cleanedJets', 'PAT' ),
            targetBtagMultiplicity = cms.uint32( 2 ),  # will calculate the weight for b-tag multiplicity >=2
            BTagSystematic = cms.int32( 0 )
            )
process.eventWeightBtagMuPlusJets = process.eventWeightBtagEPlusJets.clone( 
            numberOfTagsInput = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'NumberOfBtags', 'PAT' )  ,
            jetInput = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'cleanedJets', 'PAT' ),
                                                              )
if options.CMSSW == '44X':
    process.eventWeightBtagEPlusJets.MCSampleTag = cms.string( 'Fall11')
    process.eventWeightBtagMuPlusJets.MCSampleTag = cms.string( 'Fall11')
elif options.CMSSW == '53X' and options.centreOfMassEnergy == 8:
    process.eventWeightBtagEPlusJets.MCSampleTag = cms.string( 'Summer12')
    process.eventWeightBtagMuPlusJets.MCSampleTag = cms.string( 'Summer12')
elif options.CMSSW == '53X' and options.centreOfMassEnergy == 7:
    process.eventWeightBtagEPlusJets.MCSampleTag = cms.string( 'Summer11Leg')
    process.eventWeightBtagMuPlusJets.MCSampleTag = cms.string( 'Summer11Leg')

electron_unfolding_analysers = [
    process.unfolding_MET_analyser_electron_channel_patMETsPFlow,
    process.unfolding_MET_nu_analyser_electron_channel_patMETsPFlow,
    process.unfolding_ST_analyser_electron_channel_patMETsPFlow,
    process.unfolding_ST_nocuts_analyser_electron_channel_patMETsPFlow,
    process.unfolding_ST_parton_analyser_electron_channel_patMETsPFlow,
    process.unfolding_MT_analyser_electron_channel_patMETsPFlow,
    process.unfolding_MT_nu_analyser_electron_channel_patMETsPFlow,
    process.unfolding_WPT_analyser_electron_channel_patMETsPFlow,
    process.unfolding_WPT_nu_analyser_electron_channel_patMETsPFlow,
    process.unfolding_MET_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_MET_nu_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_ST_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_ST_nocuts_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_ST_parton_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_MT_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_MT_nu_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_WPT_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_WPT_nu_analyser_electron_channel_patType1CorrectedPFMet,
    process.unfolding_HT_analyser_electron_channel,
    process.unfolding_HT_nocuts_analyser_electron_channel,
    process.unfolding_HT_parton_analyser_electron_channel
]

for analyser in electron_unfolding_analysers:
    analyser.selection_flag_input = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'FullSelection', 'PAT' )
    analyser.b_tag_weight_input = cms.InputTag( 'eventWeightBtagEPlusJets' )
    analyser.reco_jet_input = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'cleanedJets', 'PAT' )
    analyser.electron_input = cms.InputTag( "topPairEPlusJetsSelection", electronselectionPrefix + 'signalElectron', 'PAT' )
    analyser.centre_of_mass_energy = cms.double( options.centreOfMassEnergy )

muon_unfolding_analysers = [
    process.unfolding_MET_analyser_muon_channel_patMETsPFlow,
    process.unfolding_MET_nu_analyser_muon_channel_patMETsPFlow,
    process.unfolding_ST_analyser_muon_channel_patMETsPFlow,
    process.unfolding_ST_nocuts_analyser_muon_channel_patMETsPFlow,
    process.unfolding_ST_parton_analyser_muon_channel_patMETsPFlow,
    process.unfolding_MT_analyser_muon_channel_patMETsPFlow,
    process.unfolding_MT_nu_analyser_muon_channel_patMETsPFlow,
    process.unfolding_WPT_analyser_muon_channel_patMETsPFlow,
    process.unfolding_WPT_nu_analyser_muon_channel_patMETsPFlow,
    process.unfolding_MET_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_MET_nu_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_ST_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_ST_nocuts_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_ST_parton_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_MT_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_MT_nu_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_WPT_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_WPT_nu_analyser_muon_channel_patType1CorrectedPFMet,
    process.unfolding_HT_analyser_muon_channel,
    process.unfolding_HT_nocuts_analyser_muon_channel,
    process.unfolding_HT_parton_analyser_muon_channel
]

for analyser in muon_unfolding_analysers:
    analyser.selection_flag_input = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'FullSelection', 'PAT' )
    analyser.b_tag_weight_input = cms.InputTag( 'eventWeightBtagMuPlusJets' )
    analyser.reco_jet_input = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'cleanedJets', 'PAT' )
    analyser.muon_input = cms.InputTag( "topPairMuPlusJetsSelection", muonselectionPrefix + 'signalMuon', 'PAT' )
    analyser.centre_of_mass_energy = cms.double( options.centreOfMassEnergy )

process.unfoldingAnalysisSequence = cms.Sequence( process.eventFiltersIntaggingMode * 
                                                 process.eventWeightBtagEPlusJets * 
                                                 process.eventWeightBtagMuPlusJets * 
                                                 process.printEventContent * 
#                                                 process.unfolding_MET_analyser_electron_channel_patMETsPFlow * 
#                                                 process.unfolding_MET_analyser_muon_channel_patMETsPFlow * 
#						 process.unfolding_MET_nu_analyser_electron_channel_patMETsPFlow * 
#                                                 process.unfolding_MET_nu_analyser_muon_channel_patMETsPFlow * 
#                                                 process.unfolding_ST_analyser_electron_channel_patMETsPFlow * 
#                                                 process.unfolding_ST_analyser_muon_channel_patMETsPFlow * 
#						 process.unfolding_ST_nocuts_analyser_electron_channel_patMETsPFlow * 
#                                                 process.unfolding_ST_nocuts_analyser_muon_channel_patMETsPFlow * 
#						 process.unfolding_ST_parton_analyser_electron_channel_patMETsPFlow * 
#                                                 process.unfolding_ST_parton_analyser_muon_channel_patMETsPFlow * 
#                                                 process.unfolding_MT_analyser_electron_channel_patMETsPFlow * 
#                                                 process.unfolding_MT_analyser_muon_channel_patMETsPFlow * 
#						 process.unfolding_MT_nu_analyser_electron_channel_patMETsPFlow * 
#                                                process.unfolding_MT_nu_analyser_muon_channel_patMETsPFlow * 
#						 process.unfolding_WPT_analyser_electron_channel_patMETsPFlow * 
#                                                process.unfolding_WPT_analyser_muon_channel_patMETsPFlow * 
#						 process.unfolding_WPT_nu_analyser_electron_channel_patMETsPFlow * 
#                                                 process.unfolding_WPT_nu_analyser_muon_channel_patMETsPFlow * 
                                                 process.unfolding_MET_analyser_electron_channel_patType1CorrectedPFMet * 
                                                 process.unfolding_MET_analyser_muon_channel_patType1CorrectedPFMet * 
#						 process.unfolding_MET_nu_analyser_electron_channel_patType1CorrectedPFMet * 
#                                                 process.unfolding_MET_nu_analyser_muon_channel_patType1CorrectedPFMet * 
                                                 process.unfolding_ST_analyser_electron_channel_patType1CorrectedPFMet * 
                                                 process.unfolding_ST_analyser_muon_channel_patType1CorrectedPFMet * 
#						 process.unfolding_ST_nocuts_analyser_electron_channel_patType1CorrectedPFMet * 
#                                                 process.unfolding_ST_nocuts_analyser_muon_channel_patType1CorrectedPFMet * 
#                                                 process.unfolding_ST_parton_analyser_electron_channel_patType1CorrectedPFMet * 
#                                                 process.unfolding_ST_parton_analyser_muon_channel_patType1CorrectedPFMet * 
						 process.unfolding_MT_analyser_electron_channel_patType1CorrectedPFMet * 
                                                 process.unfolding_MT_analyser_muon_channel_patType1CorrectedPFMet * 
#						 process.unfolding_MT_nu_analyser_electron_channel_patType1CorrectedPFMet * 
#                                                 process.unfolding_MT_nu_analyser_muon_channel_patType1CorrectedPFMet * 
						 process.unfolding_WPT_analyser_electron_channel_patType1CorrectedPFMet * 
                                                 process.unfolding_WPT_analyser_muon_channel_patType1CorrectedPFMet * 
#						 process.unfolding_WPT_nu_analyser_electron_channel_patType1CorrectedPFMet * 
#                                                 process.unfolding_WPT_nu_analyser_muon_channel_patType1CorrectedPFMet * 
                                                 process.unfolding_HT_analyser_electron_channel * 
                                                 process.unfolding_HT_analyser_muon_channel)
#						 process.unfolding_HT_nocuts_analyser_electron_channel * 
#                                                 process.unfolding_HT_nocuts_analyser_muon_channel * 
#						 process.unfolding_HT_parton_analyser_electron_channel * 
#						 process.unfolding_HT_parton_analyser_muon_channel )
						 
    
if not options.printEventContent:
    process.unfoldingAnalysisSequence.remove( process.printEventContent )

# if options.isTTbarMC:
process.unfoldingAnalysis = cms.Path( 
		  process.hlTrigReport * 
		  process.egammaIDLikelihood * 
		  process.pfMEtSysShiftCorrSequence * 
		  process.patseq * 
		  process.EventFilters * 
		  getattr( process, "producePatPFMETCorrections" + postfix ) * 
		  getattr( process, "patMETs" + postfix ) * 
		  process.eventWeightPU * 
		  process.unfoldingAnalysisSequence 
		  )
if not options.setupMETmanually:
    process.unfoldingAnalysis.remove( getattr( process, "producePatPFMETCorrections" + postfix ) )
    process.unfoldingAnalysis.remove( getattr( process, "patMETs" + postfix ) )

##########################################################################################
#            Selection Config
##########################################################################################
process.load( 'BristolAnalysis.NTupleTools.SelectionAnalyser_cfi' )

process.selectionAnalysis = cms.Path( 
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.pfMEtSysShiftCorrSequence * 
                      process.patseq * 
                      process.EventFilters * 
                      getattr( process, "producePatPFMETCorrections" + postfix ) * 
                      getattr( process, "patMETs" + postfix ) * 
                      process.eventFiltersIntaggingMode * 
                      process.eventWeightPU * 
                      process.ttbarDecayAnalyser * 
                      process.topPairEPlusJetsSelectionAnalyser * 
                      process.topPairMuPlusJetsSelectionAnalyser
                      )

if options.useData:
    process.eventFiltersIntaggingMode.remove( process.MCFiltersInTaggingMode )
if options.useData or not options.isTTbarMC:
    process.selectionAnalysis.remove( process.ttbarDecayAnalyser )
if not options.setupMETmanually:
    process.selectionAnalysis.remove( getattr( process, "producePatPFMETCorrections" + postfix ) )
    process.selectionAnalysis.remove( getattr( process, "patMETs" + postfix ) )
