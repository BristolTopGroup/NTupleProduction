def setup_pattuple(process, cms, options):
    print '=' * 60
    print "Setting up PATTuple"
    print '=' * 60
    process.out.outputCommands = [
        'drop *_cleanPat*_*_*',
        'keep *_selectedPat*_*_*',
        'keep *_goodPat*_*_*',
        'drop patJets_selectedPat*_*_*',
        'drop *_selectedPatJets_*_*',
        'keep *_patMETs*_*_*',
    #    'keep *_offlinePrimaryVertices*_*_*',
    #    'keep *_kt6PFJets*_*_*',
        'keep *_goodOfflinePrimaryVertices*_*_*',
        'drop patPFParticles_*_*_*',
        'drop patTaus_*_*_*',
        'keep recoPFJets_caPruned*_*_*',
        'keep recoPFJets_caTopTag*_*_*',
        'keep patTriggerObjects_patTriggerPFlow_*_*',
        'keep patTriggerFilters_patTriggerPFlow_*_*',
        'keep patTriggerPaths_patTriggerPFlow_*_*',
        'keep patTriggerEvent_patTriggerEventPFlow_*_*',
        'keep *_cleanPatPhotonsTriggerMatch*_*_*',
        'keep *_cleanPatElectronsTriggerMatch*_*_*',
        'keep *_cleanPatMuonsTriggerMatch*_*_*',
        'keep *_cleanPatTausTriggerMatch*_*_*',
        'keep *_cleanPatJetsTriggerMatch*_*_*',
        'keep *_patMETsTriggerMatch*_*_*',
        'keep double_*_*_PAT',
        'keep *_TriggerResults_*_*',
        'keep *_hltTriggerSummaryAOD_*_*',
        'keep *_ak5GenJetsNoNu_*_*',
        'keep *_ca8GenJetsNoNu_*_*',
        'keep *_caPrunedGen_*_*',
        'keep *_caTopTagPFlow_*_*',
        'keep *_caPrunedPFlow_*_*',
        'keep *_CATopTagInfosPFlow_*_*',
        'keep *_prunedGenParticles_*_*',
        'drop recoPFCandidates_selectedPatJets*_*_*',
        'drop CaloTowers_selectedPatJets*_*_*'
        #'keep recoTracks_generalTracks_*_*'
        ]
    
    if options.useData :
        process.out.outputCommands += ['drop *_MEtoEDMConverter_*_*',
                                       'keep LumiSummary_lumiProducer_*_*'
                                       ]
    else :
        process.out.outputCommands += ['keep *_ca8GenJetsNoNu_*_*',
                                       'keep *_ak5GenJetsNoNu_*_*',
                                       'keep GenRunInfoProduct_generator_*_*',
                                       'keep GenEventInfoProduct_generator_*_*',
                                       'keep *_flavorHistoryFilter_*_*',
                                       'keep PileupSummaryInfos_*_*_*'
                                       ]
    
    if options.writeFat :
    
        process.out.outputCommands += [
            'keep *_pfNoElectron*_*_*',
            'keep recoTracks_generalTracks_*_*',
            'keep recoPFCandidates_selectedPatJets*_*_*',
            'keep recoBaseTagInfosOwned_selectedPatJets*_*_*',
            'keep CaloTowers_selectedPatJets*_*_*'
            ]
        if options.useData == False :
            process.out.outputCommands += [
                'keep *_genParticles_*_*'
                ]