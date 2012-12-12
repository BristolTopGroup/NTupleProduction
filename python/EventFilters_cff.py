#better if the function would return a cms.Sequence

def setup_eventfilters(process, cms, options, useTrackingFailureFilter=False):
    print '=' * 60
    print "Setting up Event Filters"
    print '=' * 60
    process.scrapingVeto = setup_scrapingveto(process, cms)
    process.HBHENoiseFilter = setup_HBHENoiseFilter(process, cms)
    process.HBHENoiseFilterResultProducer = setup_HBHENoiseFilterResultProducer(process, cms)
    process.HcalLaserEventFilter = setup_HcalLaserFilter(process, cms)
    process.EcalDeadCellBoundaryEnergyFilter = setup_ECALDeadCellFilter(process, cms)
    process.EcalDeadCellTriggerPrimitiveFilter = setup_ECALDeadCellTriggerPrimitiveFilter(process, cms)
    process.trackingFailureFilter = setup_trackingFailureFilter(process, cms)
    process.eeBadScFilter = setup_eeBadScFilter(process, cms)
    process.ecalLaserCorrFilter = setup_ecalLaserCorrFilter(process, cms)
    #setting up tracking POG filters                                                                                                                                                                                                      
    setup_trackingPOGfilters(process, cms)
    
    process.EventFilter = setup_skim(process, cms, options)
    process.EventFilter.HBHENoiseFilterInput = cms.InputTag('HBHENoiseFilterResultProducer', 'HBHENoiseFilterResult')
    process.EventFilter.HCALLaserFilterInput = cms.InputTag('HcalLaserEventFilter')
    process.EventFilter.ECALDeadCellFilterInput = cms.InputTag('EcalDeadCellBoundaryEnergyFilter')
    process.EventFilter.ECALDeadCellTriggerPrimitiveFilterInput = cms.InputTag('EcalDeadCellTriggerPrimitiveFilter')
    process.EventFilter.TrackingFailureFilterInput = cms.InputTag('trackingFailureFilter')
    process.EventFilter.EEBadSCFilterInput = cms.InputTag('eeBadScFilter')
    process.EventFilter.ECALLaserCorrFilterInput = cms.InputTag('ecalLaserCorrFilter')
    #tracking POG filters
    process.EventFilter.manystripclus53XInput = cms.InputTag('manystripclus53X')
    process.EventFilter.toomanystripclus53XInput = cms.InputTag('toomanystripclus53X')
    process.EventFilter.logErrorTooManyClustersInput = cms.InputTag('logErrorTooManyClusters')
    process.EventFilter.useTrackingPOGFilters = cms.bool(True)
    process.EventFilter.useTrackingFailureFilter = cms.bool(True)
    #disable optional MET filters for now
    process.EventFilter.useOptionalMETFilters = cms.bool(False)
    
    print "Creating event filter sequence (merging all previous)."
    EventFilters = cms.Sequence(
                process.HBHENoiseFilterResultProducer *
                process.trackingFailureFilter * 
                process.scrapingVeto * 
                process.HcalLaserEventFilter * 
                process.EcalDeadCellBoundaryEnergyFilter *
                process.EcalDeadCellTriggerPrimitiveFilter *
                process.eeBadScFilter *
                process.ecalLaserCorrFilter *
                ~process.manystripclus53X *
                ~process.toomanystripclus53X *
                ~process.logErrorTooManyClusters *
                process.EventFilter
                )
    return EventFilters
    
def setup_HBHENoiseFilter(process, cms):
    print '=' * 60
    print "Setting up HBHE Noise Filter"
    print '=' * 60
    # HB + HE noise filtering
    #following https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFilters prescription
    #this filter is applied before the PAT sequence
    from CommonTools.RecoAlgos.HBHENoiseFilter_cfi import HBHENoiseFilter
    return HBHENoiseFilter

def setup_HBHENoiseFilterResultProducer(process, cms):
    #EDProducer to keep track of in the AnalysisTools
    #values kept identical to the ones from HBHENoiseFilter
    HBHENoiseFilterResultProducer = cms.EDProducer(
        'HBHENoiseFilterResultProducer',
        noiselabel=cms.InputTag('hcalnoise'),
        minRatio=cms.double(-999),
        maxRatio=cms.double(999),
        minHPDHits=cms.int32(17),
        minRBXHits=cms.int32(999),
        minHPDNoOtherHits=cms.int32(10),
        minZeros=cms.int32(10),
        minHighEHitTime=cms.double(-9999.0),
        maxHighEHitTime=cms.double(9999.0),
        maxRBXEMF=cms.double(-999.0),
        minNumIsolatedNoiseChannels = cms.int32(10),
        minIsolatedNoiseSumE = cms.double(50.0),
        minIsolatedNoiseSumEt = cms.double(25.0),
        useTS4TS5=cms.bool(True),
        IgnoreTS4TS5ifJetInLowBVRegion=cms.bool(False),
        jetlabel = cms.InputTag('ak5PFJets'),
        maxjetindex = cms.int32(0), # maximum jet index that will be checked for 'IgnoreTS4TS5ifJetInLowBVRegion'
        maxNHF = cms.double(0.9) # maximum allowed jet->neutralHadronEnergyFraction()
        )
    return HBHENoiseFilterResultProducer
    
def setup_scrapingveto(process, cms):
    print '=' * 60
    print "Setting up scraping Filter"
    print '=' * 60
    scrapingVeto = cms.EDFilter("FilterOutScraping",
     applyfilter=cms.untracked.bool(False),
     debugOn=cms.untracked.bool(False),
     numtrack=cms.untracked.uint32(10),
     thresh=cms.untracked.double(0.25)
     )
    return scrapingVeto

def setup_HcalLaserFilter(process, cms):
    print '=' * 60
    print "Setting up HcalLaser Filter"
    print '=' * 60
    
    from RecoMET.METFilters.hcalLaserEventFilter_cfi import hcalLaserEventFilter
    hcalLaserEventFilter.taggingMode = cms.bool(True)
    
    return hcalLaserEventFilter

def setup_ECALDeadCellFilter(process, cms):
    print '=' * 60
    print "Setting up ECALDeadCell Filter"
    print '=' * 60
    #https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
    from RecoMET.METFilters.EcalDeadCellBoundaryEnergyFilter_cfi import EcalDeadCellBoundaryEnergyFilter
    EcalDeadCellBoundaryEnergyFilter.taggingMode = cms.bool(True)
    EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEB = cms.untracked.double(10)
    EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEE = cms.untracked.double(10)
    EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEB = cms.untracked.double(100)
    EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEE = cms.untracked.double(100)
    EcalDeadCellBoundaryEnergyFilter.enableGap = cms.untracked.bool(False)
    EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEB = cms.vint32(12, 14)
    EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEE = cms.vint32(12, 14)

    return EcalDeadCellBoundaryEnergyFilter

def setup_ECALDeadCellTriggerPrimitiveFilter(process, cms):
    print '=' * 60
    print "Setting up ECALDeadCell TriggerPrimitive Filter"
    print '=' * 60    
    #https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFilters#ECAL_dead_cell_filter
    from RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi import EcalDeadCellTriggerPrimitiveFilter
    EcalDeadCellTriggerPrimitiveFilter.taggingMode = cms.bool(True)
    EcalDeadCellTriggerPrimitiveFilter.tpDigiCollection = cms.InputTag("ecalTPSkimNA")
    return EcalDeadCellTriggerPrimitiveFilter   


def setup_trackingFailureFilter(process, cms):
    from RecoMET.METFilters.trackingFailureFilter_cfi import trackingFailureFilter
    trackingFailureFilter.JetSource = cms.InputTag('ak5PFJets')
    trackingFailureFilter.TrackSource = cms.InputTag('generalTracks')
    trackingFailureFilter.VertexSource = cms.InputTag('goodOfflinePrimaryVertices')
    trackingFailureFilter.taggingMode = cms.bool(True)
    return trackingFailureFilter

def setup_eeBadScFilter(process, cms):
    from RecoMET.METFilters.eeBadScFilter_cfi import eeBadScFilter
    eeBadScFilter.taggingMode = cms.bool (True)
    return eeBadScFilter

def setup_ecalLaserCorrFilter(process, cms):
    from RecoMET.METFilters.ecalLaserCorrFilter_cfi import ecalLaserCorrFilter
    ecalLaserCorrFilter.taggingMode = cms.bool (True)
    ecalLaserCorrFilter.Debug = cms.bool (False)
    return ecalLaserCorrFilter

def setup_trackingPOGfilters(process, cms):
    from RecoMET.METFilters.trackingPOGFilters_cfi import manystripclus53X
    from RecoMET.METFilters.trackingPOGFilters_cfi import toomanystripclus53X
    from RecoMET.METFilters.trackingPOGFilters_cfi import logErrorTooManyClusters
    manystripclus53X.taggedMode = cms.untracked.bool(True)
    manystripclus53X.forcedValue = cms.untracked.bool(False)
    toomanystripclus53X.taggedMode = cms.untracked.bool(True)
    toomanystripclus53X.forcedValue = cms.untracked.bool(False)
    logErrorTooManyClusters.taggedMode = cms.untracked.bool(True)
    logErrorTooManyClusters.forcedValue = cms.untracked.bool(False)
    process.manystripclus53X = manystripclus53X
    process.toomanystripclus53X = toomanystripclus53X
    process.logErrorTooManyClusters = logErrorTooManyClusters

    
def setup_skim(process, cms, options):
    print '=' * 60
    print "Setting up skim"
    print '=' * 60
    skim = options.skim
    process.load("BristolAnalysis.NTupleTools.EventFilter_cfi")
    from BristolAnalysis.NTupleTools.EventFilter_cfi import EventFilter
    #at least one good primary vertex
    EventFilter.VertexInput = cms.InputTag('goodOfflinePrimaryVertices')
    #reset to 0 skim
    EventFilter.minNElectrons = cms.int32(-1)
    EventFilter.minNMuons = cms.int32(-1)
    EventFilter.minNJets = cms.int32(-1)
    EventFilter.counteitherleptontype = cms.bool(False)
    
    skim = skim.lower()
    if 'electron' in skim or 'lepton' in skim:
        EventFilter.maxAbsElectronEta = cms.double(2.5)#within tracker volume
        #electron multiplicity
        if 'di' in skim:
            EventFilter.minNElectrons = cms.int32(2)
        else:
            EventFilter.minNElectrons = cms.int32(1)
        
        if 'loose' in skim:#loose Pt cut
            EventFilter.minElectronPt = cms.double(20.)
            EventFilter.electronInput = cms.InputTag("selectedPatElectrons")#GSF electrons
        else:
            EventFilter.minElectronPt = cms.double(30.)
            EventFilter.electronInput = cms.InputTag("selectedPatElectronsLoosePFlow")
    
    if 'muon'  in skim or 'lepton' in skim:
        #muon multiplicity
        if 'di' in skim:
            EventFilter.minNMuons = cms.int32(2)
        else:
            EventFilter.minNMuons = cms.int32(1)
        if 'loose' in skim:#loose Pt cut and eta cut
            EventFilter.maxAbsMuonEta = cms.double(2.5)#within tracker volume
            EventFilter.minMuonPt = cms.double(10.)
            EventFilter.muonInput = cms.InputTag("selectedPatMuons")
        else:
            EventFilter.minMuonPt = cms.double(20.)#triggers are 17GeV
            EventFilter.maxAbsMuonEta = cms.double(2.1)#new triggers have this restriction anyway
            EventFilter.muonInput = cms.InputTag("selectedPatMuonsLoosePFlow")
    
    if 'lepton' in skim:
        EventFilter.counteitherleptontype = cms.bool(True)
 
    #jet skim
    #unprescaled triggers are >=3/>=2 jets for electron/muon triggers
    if 'jet' in skim:
        find = skim.find('jet')
        nJets = int(skim[find - 1])
        EventFilter.jetInput = cms.InputTag("selectedPatJetsPFlow")
        EventFilter.minNJets = cms.int32(nJets)
        EventFilter.minJetPt = cms.double(30.)# identical (within JEC) to trigger
        EventFilter.maxAbsJetEta = cms.double(2.6)# identical to trigger
    
    
    if not (skim == '' or skim == 'noskim'):
        print '=' * 10, 'Skim definition', '=' * 10
        print 'Electron skim:'
        print '\t >=', str(EventFilter.minNMuons), ' electron with ',
        print 'p_T > ', str(EventFilter.minElectronPt),
        print '|eta| < ' , str(EventFilter.maxAbsElectronEta)
        print '\t input collection:', str(EventFilter.electronInput)
        print
        print 'Muon skim:'
        print '\t >=', str(EventFilter.minNElectrons), ' muon with ',
        print 'p_T > ', str(EventFilter.minMuonPt),
        print '|eta| < ' , str(EventFilter.maxAbsMuonEta)
        print '\t input collection:', str(EventFilter.muonInput)
        print
        print 'Use either lepton type:', str(EventFilter.counteitherleptontype)
        print
        print 'Jet skim:'
        print '\t >=', str(EventFilter.minNJets), ' jet with ',
        print 'p_T > ', str(EventFilter.minJetPt),
        print '|eta| < ' , str(EventFilter.maxAbsJetEta)
        print '\t input collection:', str(EventFilter.jetInput)
    else:
        print 'No skim used.'
    return EventFilter
