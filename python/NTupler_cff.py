def setup_ntupler(process, cms):
    print '=' * 60
    print "Setting up NTupler"
    print '=' * 60
    ######################################################################################################
    ################################## nTuple Configuration ##############################################
    ######################################################################################################
    process.load('BristolAnalysis.NTupleTools.Ntuple_cff')

    process.nTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
            treeName = cms.string('tree'),
            outputCommands=cms.untracked.vstring(
               'drop *',
               # Event
               'keep *_nTupleEvent_*_*',
               # Trigger
               'keep *_nTupleTrigger*_*_*',
               # Trigger Objects
               'keep *_nTupleTriggerObjects*_*_*',
               # Vertices
               'keep *_nTupleVertex_*_*',
               # muons
               'keep *_nTupleMuons_*_*',
               # electrons
               'keep *_nTupleElectrons_*_*',
               # jets
               'keep *_nTuplePFJets_*_*',
               # MET
               'keep *_nTupleMET_*_*',
               # Gen Event
               'keep *_nTupleGenEventInfo_*_*',
               # Gen Particles
               'keep *_nTupleGenParticles_*_*',
               # Gen Jets
               'keep *_nTupleGenJets_*_*',
               # Gen MET
               'keep *_nTupleGenMET_*_*',
               # Pseudo Top
               'keep *_nTuplePseudoTop*_*_*',

               'keep *_selectionCriteriaAnalyzer_*_*'
            )
        )

    process.nTupleTreeMuon = process.nTupleTree.clone( treeName = cms.string('muonTree') )
    process.nTupleTreeMuon.outputCommands.append( 'keep uint*_topPairMuPlusJetsSelectionTagging_*_*' )
    process.nTupleTreeElectron = process.nTupleTree.clone( treeName = cms.string('electronTree') )
    process.nTupleTreeElectron.outputCommands.append( 'keep uint*_topPairEPlusJetsSelectionTagging_*_*' )

    process.nTuples = cms.Sequence(
        # Event
        process.nTupleEvent +

        # Trigger
        process.triggerSequence +

        # Trigger Objects
        # process.triggerObjectSequence +

        # Vertices
        process.nTupleVertex + 

        # muons
        process.nTupleMuons +

        # Electron
        process.nTupleElectrons +

        # Jets
        process.nTuplePFJets +

        # MET
        process.nTupleMET +

        # Gen Event
        process.nTupleGenEventInfo +

        # Gen Particles
        process.nTupleGenParticles +

        # Gen MET
        process.nTupleGenMET +

        # Gen Jets
        process.nTupleGenJets +

        # Pseudo Top
        process.pseudoTopSequence
    )

    process.muonNTuples = cms.Sequence( process.nTuples * process.nTupleTreeMuon )
    process.electronNTuples = cms.Sequence( process.nTuples * process.nTupleTreeElectron )

