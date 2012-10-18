def setup_ntupler(process, cms, options, includeCA08Jets = False):
    print '=' * 60
    print "Setting up NTupler"
    print '=' * 60
    ######################################################################################################
    ################################## nTuple Configuration ##############################################
    ######################################################################################################
    process.load('BristolAnalysis.NTupleTools.Ntuple_cff')
    #vertices
    process.rootTupleVertex.InputTag = cms.InputTag('goodOfflinePrimaryVertices')
    process.rootTupleVertex.Prefix = cms.string('goodOfflinePrimaryVertices.')
    #calo jets
    process.rootTupleCaloJets.InputTag = cms.InputTag('goodPatJets')
    process.rootTupleCaloJets.Prefix = cms.string('goodPatJets.')
    #PF2PAT jets
    process.rootTuplePF2PATJets.InputTag = cms.InputTag('goodPatJetsPFlow')
    process.rootTuplePF2PATJets.Prefix = cms.string('goodPatJetsPFlow.')
    #Cambridge-Aachen cone 0.8 jets
    process.rootTupleCA8PFJets = process.rootTuplePF2PATJets.clone()
    process.rootTupleCA8PFJets.InputTag = cms.InputTag('goodPatJetsCA8PF')
    process.rootTupleCA8PFJets.Prefix = cms.string('goodPatJetsCA8PF.')
    #selection on GenParticles
    process.rootTupleGenParticles.minPt = cms.double(-1)
    process.rootTupleGenParticles.maxAbsoluteEta = cms.double(100)
    #GSF Electrons
    process.rootTupleElectrons.InputTag = cms.InputTag('selectedPatElectrons')
    process.rootTupleElectrons.Prefix = cms.string('selectedPatElectrons.')
    #isolated PF Electrons
    process.rootTuplePFElectrons.InputTag = cms.InputTag('selectedPatElectronsPFlow')
    process.rootTuplePFElectrons.Prefix = cms.string('selectedPatElectronsPFlow.')
    #non-isolated PF electrons
    process.rootTuplePFLooseElectrons.InputTag = cms.InputTag('selectedPatElectronsLoosePFlow')
    process.rootTuplePFLooseElectrons.Prefix = cms.string('selectedPatElectronsLoosePFlow.')
    #muons
    process.nTupleMuons.InputTag = cms.InputTag('selectedPatMuons')
    process.nTupleMuons.Prefix = cms.string('selectedPatMuons.')
    #standard PF muons
    process.nTuplePFMuons.InputTag = cms.InputTag('selectedPatMuonsPFlow')
    process.nTuplePFMuons.Prefix = cms.string('selectedPatMuonsPFlow.')
    #non isolated PF muons
    process.nTuplePFLooseMuons.InputTag = cms.InputTag('selectedPatMuonsLoosePFlow')
    process.nTuplePFLooseMuons.Prefix = cms.string('selectedPatMuonsLoosePFlow.')
    #PF taus
    process.rootTupleTaus.InputTag = cms.InputTag('selectedPatTausPFlow')
    process.rootTupleTaus.Prefix = cms.string('selectedPatTausPFlow.')
    #PF photons
    process.rootTuplePhotons.InputTag = cms.InputTag('patPhotons')
    process.rootTuplePhotons.Prefix = cms.string('patPhotons.')
    #trigger
    process.rootTupleTrigger.HLTInputTag = cms.InputTag('TriggerResults', '', options.hltProcess)
    #GEN event
    process.rootTupleGenEventInfo.StorePDFWeights = cms.bool(options.storePDFWeights)
    
    process.rootTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
        outputCommands=cms.untracked.vstring(
           'drop *',
           #beamspot
            'keep *_rootTupleBeamSpot_*_*',
            #EventContent
            'keep *_rootTupleEvent_*_*',
            #CaloJets
            'keep *_rootTupleCaloJets_*_*',
            #PF jets
            'keep *_rootTuplePF2PATJets_*_*',
            'keep *_rootTupleCA8PFJets_*_*',
            #electrons
            'keep *_rootTupleElectrons_*_*',
            'keep *_rootTuplePFElectrons_*_*',
            'keep *_rootTuplePFLooseElectrons_*_*',
            #MET
            'keep *_rootTupleCaloMET_*_*',
            'keep *_rootTuplePFMET_*_*',
            'keep *_rootTuplePFType1CorrectedMET_*_*',
            'keep *_rootTuplePFType1p2CorrectedMET_*_*',
            'keep *_rootTuplePFMet*_*_*',
            'keep *_rootTupleType1CorrectedPFMet*_*_*',
            'keep *_rootTupleType1p2CorrectedPFMet*_*_*',
            #muons
            'keep *_nTupleMuons_*_*',
            'keep *_nTuplePFMuons_*_*',
            'keep *_nTuplePFLooseMuons_*_*',
            #taus
            'keep *_rootTupleTaus_*_*',
            #photons
            'keep *_rootTuplePhotons_*_*',
            #trigger
            'keep *_rootTupleTrigger_*_*',
            #vertices (DA)
            'keep *_rootTupleVertex_*_*',
            #tracks
            'keep *_rootTupleTracks_*_*',
            #gen information
            'keep *_rootTupleGenEventInfo_*_*',
            'keep *_rootTupleGenParticles_*_*',
            'keep *_rootTupleGenJets_*_*',
            'keep *_rootTupleGenMETTrue_*_*',
            'kepp *_eventWeightPU_*_*'
        )
    )
    
    process.rootNTuples = cms.Sequence((
        #beamspot
        process.rootTupleBeamSpot + 
        #vertices
        process.rootTupleVertex + 
        #jets
        process.rootTupleCaloJets + 
        process.rootTuplePF2PATJets + 
        process.rootTupleCA8PFJets + 
    #    process.rootTupleCA8PFJetsPruned +
    #    process.rootTupleCA8PFJetsTopTag +
        #electrons
        process.rootTupleElectrons + 
        process.rootTuplePFElectrons + 
        process.rootTuplePFLooseElectrons + 
        #muons
        process.nTuplePFMuons + 
        process.nTuplePFLooseMuons + 
        process.nTupleMuons + 
        #taus
        process.rootTupleTaus + 
        #photons
        process.rootTuplePhotons + 
        #MET
        process.rootTupleCaloMET + 
        process.rootTuplePFMET + 
        process.rootTuplePFType1CorrectedMET +
        process.rootTuplePFType1p2CorrectedMET +
        #MET uncertainties
        process.rootTuplePFMetElectronEnUp +
        process.rootTuplePFMetElectronEnDown +
        process.rootTuplePFMetMuonEnUp +
        process.rootTuplePFMetMuonEnDown +
        process.rootTuplePFMetTauEnUp +
        process.rootTuplePFMetTauEnDown +
        process.rootTuplePFMetJetResUp +
        process.rootTuplePFMetJetResDown +
        process.rootTuplePFMetJetEnUp +
        process.rootTuplePFMetJetEnDown +
        process.rootTuplePFMetUnclusteredEnUp +
        process.rootTuplePFMetUnclusteredEnDown +
        #Type 1 MET uncertainties
        process.rootTupleType1CorrectedPFMetElectronEnUp +
        process.rootTupleType1CorrectedPFMetElectronEnDown +
        process.rootTupleType1CorrectedPFMetMuonEnUp +
        process.rootTupleType1CorrectedPFMetMuonEnDown +
        process.rootTupleType1CorrectedPFMetTauEnUp +
        process.rootTupleType1CorrectedPFMetTauEnDown +
        process.rootTupleType1CorrectedPFMetJetResUp +
        process.rootTupleType1CorrectedPFMetJetResDown +
        process.rootTupleType1CorrectedPFMetJetEnUp +
        process.rootTupleType1CorrectedPFMetJetEnDown +
        process.rootTupleType1CorrectedPFMetUnclusteredEnUp +
        process.rootTupleType1CorrectedPFMetUnclusteredEnDown +
        #Type 1 + 2 MET uncertainties
        process.rootTupleType1p2CorrectedPFMetElectronEnUp +
        process.rootTupleType1p2CorrectedPFMetElectronEnDown +
        process.rootTupleType1p2CorrectedPFMetMuonEnUp +
        process.rootTupleType1p2CorrectedPFMetMuonEnDown +
        process.rootTupleType1p2CorrectedPFMetTauEnUp +
        process.rootTupleType1p2CorrectedPFMetTauEnDown +
        process.rootTupleType1p2CorrectedPFMetJetResUp +
        process.rootTupleType1p2CorrectedPFMetJetResDown +
        process.rootTupleType1p2CorrectedPFMetJetEnUp +
        process.rootTupleType1p2CorrectedPFMetJetEnDown +
        process.rootTupleType1p2CorrectedPFMetUnclusteredEnUp +
        process.rootTupleType1p2CorrectedPFMetUnclusteredEnDown +
        #Event
        process.rootTupleEvent + 
        #trigger
        process.rootTupleTrigger + 
        #genEventInfos
        process.rootTupleGenEventInfo + 
        process.rootTupleGenParticles + 
        process.rootTupleGenJetSequence + 
        process.rootTupleGenMETTrue) * 
                                       
        process.rootTupleTree)
    
    
    if not includeCA08Jets:
        process.rootNTuples.remove(process.rootTupleCA8PFJets)
        
    if options.useData:
        process.rootNTuples.remove(process.rootTupleGenEventInfo)
        process.rootNTuples.remove(process.rootTupleGenParticles)
        process.rootNTuples.remove(process.rootTupleGenJetSequence)
        process.rootNTuples.remove(process.rootTupleGenMETTrue)
        process.rootNTuples.remove(process.rootTuplePFMetJetResUp)
        process.rootNTuples.remove(process.rootTuplePFMetJetResDown)
        process.rootNTuples.remove(process.rootTupleType1CorrectedPFMetJetResUp)
        process.rootNTuples.remove(process.rootTupleType1CorrectedPFMetJetResDown)
        process.rootNTuples.remove(process.rootTupleType1p2CorrectedPFMetJetResUp)
        process.rootNTuples.remove(process.rootTupleType1p2CorrectedPFMetJetResDown)
        process.rootNTuples.remove(process.eventWeightPU)
        
    if not options.writeFat:#write only PF particles
        process.rootNTuples.remove(process.rootTupleCaloJets)
        process.rootNTuples.remove(process.rootTupleCaloMET)
        process.rootNTuples.remove(process.rootTupleElectrons)
        process.rootNTuples.remove(process.nTupleMuons)
        
    if not options.writeFat and not options.writeIsolatedPFLeptons:#write only PF particles
        #isolated leptons
        process.rootNTuples.remove(process.rootTuplePFElectrons)
        process.rootNTuples.remove(process.nTuplePFMuons)