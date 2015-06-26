#include "BristolAnalysis/NTupleTools/plugins/TopPairElectronPlusJetsSelectionFilter.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
// system include files
#include <memory>
#include <iostream>
// user include files
#include "DataFormats/RecoCandidate/interface/IsoDepositDirection.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EgammaAnalysis/ElectronTools/interface/ElectronEffectiveArea.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;

TopPairElectronPlusJetsSelectionFilter::TopPairElectronPlusJetsSelectionFilter(const edm::ParameterSet& iConfig) :
		jetInput_(iConfig.getParameter < edm::InputTag > ("jetInput")), //
		electronInput_(iConfig.getParameter < edm::InputTag > ("electronInput")), //
		muonInput_(iConfig.getParameter < edm::InputTag > ("muonInput")), //
		hltInputTag_(iConfig.getParameter < edm::InputTag > ("HLTInput")), //
		vertexInputTag_(iConfig.getParameter < edm::InputTag > ("VertexInputTag")), //

		// Selection criteria
		minSignalElectronPt_(iConfig.getParameter<double>("minSignalElectronPt")), //
		maxSignalElectronEta_(iConfig.getParameter<double>("maxSignalElectronEta")), //
  		signalElectronIDMapToken_(consumes<ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("signalElectronIDMap"))),
  		signalElectronIDMapToken_bitmap_(consumes<ValueMap<unsigned int> >(iConfig.getParameter<edm::InputTag>("signalElectronIDMap_bitmap"))),
		minSignalElectronID_(iConfig.getParameter<double>("minSignalElectronID")), //
		minLooseMuonPt_(iConfig.getParameter<double>("minLooseMuonPt")), //
		maxLooseMuonEta_(iConfig.getParameter<double>("maxLooseMuonEta")), //
		minLooseElectronPt_(iConfig.getParameter<double>("minLooseElectronPt")), //
		maxLooseElectronEta_(iConfig.getParameter<double>("maxLooseElectronEta")), //
  		looseElectronIDMapToken_(consumes<ValueMap<bool> >(iConfig.getParameter<edm::InputTag>("looseElectronIDMap"))),

		minLooseElectronID_(iConfig.getParameter<double>("minLooseElectronID")), //

		min1JetPt_(iConfig.getParameter<double>("min1JetPt")), //
		min2JetPt_(iConfig.getParameter<double>("min2JetPt")), //
		min3JetPt_(iConfig.getParameter<double>("min3JetPt")), //
		min4JetPt_(iConfig.getParameter<double>("min4JetPt")), //
		minBJetPt_(iConfig.getParameter<double>("minBJetPt")), //
		minJetPtInNtuples_(iConfig.getParameter<double>("minJetPtInNtuples")), //

		cleaningDeltaR_(iConfig.getParameter<double>("cleaningDeltaR")), //

		applyJEC_(iConfig.getParameter < bool > ("applyJEC")), //
		jetCorrectionService_(iConfig.getParameter<std::string> ("JetCorrectionService")), //
		corrector_(0), //

		bJetDiscriminator_(iConfig.getParameter<std::string>("bJetDiscriminator")), //
		minBJetDiscriminator_(iConfig.getParameter<double>("minBJetDiscriminator")), //

		tightElectronIso_EB_(iConfig.getParameter<double>("tightElectronIsolation_EB")), //
		tightElectronIso_EE_(iConfig.getParameter<double>("tightElectronIsolation_EE")), //
		controlElectronIso_(iConfig.getParameter<double>("controlElectronIsolation")), //

		tagAndProbeStudies_(iConfig.getParameter<bool>("tagAndProbeStudies")), //
		dropTriggerSelection_(iConfig.getParameter<bool>("dropTriggerSelection")), //
		prefix_(iConfig.getUntrackedParameter < std::string > ("prefix")), //
		MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
		debug_(iConfig.getUntrackedParameter<bool>("debug")), //
		taggingMode_(iConfig.getParameter<bool>("taggingMode")), //
		jetSelectionInTaggingMode_(iConfig.getParameter<bool>("jetSelectionInTaggingMode")), //
		bSelectionInTaggingMode_(iConfig.getParameter<bool>("bSelectionInTaggingMode")), //

		nonIsolatedElectronSelection_(iConfig.getParameter<bool>("nonIsolatedElectronSelection")), //
		invertedConversionSelection_(iConfig.getParameter<bool>("invertedConversionSelection")), //
		passes_(), //
		runNumber_(0), //
		signalElectronIndex_(999), //
		isRealData_(false), //
		hasSignalElectron_(false), //
		cleanedJetIndex_(),
		cleanedBJetIndex_(),
		jets_(), //,
		cleanedJets_(), //
		cleanedBJets_(), //
		electrons_(), //
		goodIsolatedElectrons_(), //
		looseElectrons_(), //
		muons_(), //
		looseMuons_(), //
		signalElectron_(), //
		vertices_(), //
		hltConfig_(), //
		triggerResults_() {
	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		passes_.at(step) = 0;
		produces<bool>(prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	produces<bool>(prefix_ + "FullSelection");
	produces<unsigned int>(prefix_ + "NumberOfJets");
	produces<unsigned int>(prefix_ + "NumberOfBtags");
	produces<std::vector<unsigned int> >(prefix_ + "cleanedJetIndex");
	produces<std::vector<unsigned int> >(prefix_ + "cleanedBJetIndex");
	// produces < pat::JetCollection > (prefix_ + "cleanedJets");
	produces<unsigned int>(prefix_ + "signalElectronIndex");
}

void TopPairElectronPlusJetsSelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("jetInput");
	desc.add < InputTag > ("electronInput");
	desc.add < InputTag > ("muonInput");
	desc.add < InputTag > ("HLTInput");
	desc.add < InputTag > ("VertexInputTag");

	desc.add<double>("minSignalElectronPt",0.);
	desc.add<double>("maxSignalElectronEta",10.);
	desc.add<double>("minSignalElectronID",0);
	desc.add < InputTag > ("signalElectronIDMap");
	desc.add < InputTag > ("signalElectronIDMap_bitmap");
	desc.add < InputTag > ("looseElectronIDMap");
	desc.add<double>("minLooseMuonPt",0.);
	desc.add<double>("maxLooseMuonEta",10.);
	desc.add<double>("minLooseElectronPt",0.);
	desc.add<double>("maxLooseElectronEta",10.);
	desc.add<double>("minLooseElectronID",0);

	desc.add<double>("min1JetPt", 30.0);
	desc.add<double>("min2JetPt", 30.0);
	desc.add<double>("min3JetPt", 30.0);
	desc.add<double>("min4JetPt", 30.0);
	desc.add<double>("minBJetPt", 30.0);
	desc.add<double>("minJetPtInNtuples", 30.0);

	desc.add<double>("cleaningDeltaR", 0.3 );

	desc.add<bool>("applyJEC", false);
	desc.add<std::string>("JetCorrectionService", "");

	desc.add < std::string > ("bJetDiscriminator", "combinedSecondaryVertexBJetTags");
	desc.add<double>("minBJetDiscriminator", 0.679 );

	desc.add<double>("tightElectronIsolation_EB", 0.14);
	desc.add<double>("tightElectronIsolation_EE", 0.1649);

	desc.add<double>("controlElectronIsolation", 0.3);
	
	desc.add<bool>("tagAndProbeStudies", false);
	desc.add<bool>("dropTriggerSelection", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairElectronPlusJetsSelection.");
	desc.addUntracked<bool>("debug", false);
	desc.add<bool>("taggingMode", false);
	desc.add<bool>("bSelectionInTaggingMode", false);
	desc.add<bool>("jetSelectionInTaggingMode", false);
   	desc.add<bool>("nonIsolatedElectronSelection", false);
   	desc.add<bool>("invertedConversionSelection", false);
	descriptions.add("applyTopPairElectronPlusJetsSelection", desc);
}

TopPairElectronPlusJetsSelectionFilter::~TopPairElectronPlusJetsSelectionFilter() {

}

bool TopPairElectronPlusJetsSelectionFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	// Get content from event
	// Including selecting a signal electron, loose leptons, jets and bjets
	setupEventContent(iEvent, iSetup);
	
	bool passesSelection(true);
	bool passesSelectionExceptJetRequirements(true);
	bool passesSelectionExceptBtagging(true);

	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		TTbarEPlusJetsReferenceSelection::Step stepName = TTbarEPlusJetsReferenceSelection::Step(step);
		if (debug_)
			cout << "Doing selection step: " << TTbarEPlusJetsReferenceSelection::StringSteps[step] << endl;

		bool passesStep(passesSelectionStep(iEvent, step));

		// Require exactly zero b jets for QCD control region
		// Or exactly one b jet, as e.g. angle(b,l) only makes sense if there is at least one b jet
		if ( nonIsolatedElectronSelection_ || invertedConversionSelection_ ) {
			if ( stepName == TTbarEPlusJetsReferenceSelection::AtLeastOneBtag || stepName == TTbarEPlusJetsReferenceSelection::AtLeastTwoBtags ) {
				passesStep = hasExactlyZeroGoodBJet() || hasExactlyOneGoodBJet() ;
			}
		}

		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;

		if ( step < TTbarEPlusJetsReferenceSelection::AtLeastOneGoodJet )
			passesSelectionExceptJetRequirements = passesSelectionExceptJetRequirements && passesStep;

		if ( step < TTbarEPlusJetsReferenceSelection::AtLeastOneBtag )
			passesSelectionExceptBtagging = passesSelectionExceptBtagging && passesStep;

       // Require exactly zero b jets for QCD control region
       // Or exactly one b jet, as e.g. angle(b,l) only makes sense if there is at least one b jet
       if ( nonIsolatedElectronSelection_ || invertedConversionSelection_ ) {
            if ( step == TTbarEPlusJetsReferenceSelection::AtLeastOneBtag || step == TTbarEPlusJetsReferenceSelection::AtLeastTwoBtags ) {
                passesStep = hasExactlyZeroGoodBJet() || hasExactlyOneGoodBJet() ;
            }
       }

		// if doesn't pass selection and not in tagging mode, stop here to save CPU time
		if ( !(taggingMode_ || passesSelection) )
			break;
	}
	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");

	// Store number of cleaned jets in events
	unsigned int numberOfJets(cleanedJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfJets)), prefix_ + "NumberOfJets");

	// Store indices of cleaned jets in event
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedJetIndex_)), prefix_ + "cleanedJetIndex");
	
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedBJetIndex_)), prefix_ + "cleanedBJetIndex");

	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(signalElectronIndex_)),prefix_ + "signalElectronIndex");

	if ( bSelectionInTaggingMode_ )
		return taggingMode_ || passesSelectionExceptBtagging;
	else if ( jetSelectionInTaggingMode_ )
		return taggingMode_ || passesSelectionExceptJetRequirements;
	else
		return taggingMode_ || passesSelection;
}

void TopPairElectronPlusJetsSelectionFilter::setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	if (debug_)
		cout << "Setting up the event content" << endl;

	// Event info
	runNumber_ = iEvent.run();
	isRealData_ = iEvent.isRealData();

	// Vertices (for re calculating electron ID)
	if ( nonIsolatedElectronSelection_ || invertedConversionSelection_ ) {
		edm::Handle < reco::VertexCollection > verticesHandle;
	   	iEvent.getByLabel(vertexInputTag_, verticesHandle);
	   	vertices_ = *verticesHandle;
	}
	
	// Trigger info
	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByLabel(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	// Jets
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(jetInput_, jets);
	jets_ = *jets;

	if ( applyJEC_ ) {
		corrector_ = JetCorrector::getJetCorrector (jetCorrectionService_, iSetup);
		jets_ = applyNewJec( jets_, corrector_, iEvent, iSetup );
	}

	// Electrons
	iEvent.getByLabel(electronInput_, electrons_);

	// Electron VID Decisions
	Handle<edm::ValueMap<bool> > tight_id_decisions;
	iEvent.getByToken(signalElectronIDMapToken_,tight_id_decisions);
	signalElectronIDDecisions_ = *tight_id_decisions;

	Handle<edm::ValueMap<unsigned int> > tight_id_decisions_bitmap;
	iEvent.getByToken(signalElectronIDMapToken_bitmap_,tight_id_decisions_bitmap);
	signalElectronIDDecisions_bitmap_ = *tight_id_decisions_bitmap;

	Handle<edm::ValueMap<bool> > loose_id_decisions;
	iEvent.getByToken(looseElectronIDMapToken_,loose_id_decisions);
	looseElectronIDDecisions_ = *loose_id_decisions;

	// Muons (for veto)
	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByLabel(muonInput_, muons);
	muons_ = *muons;

	// Choose electrons that pass loose selection
	if (debug_)
		cout << "Getting loose electrons" << endl;
	getLooseElectrons();

	// Choose muons that pass loose selection
	if (debug_)
		cout << "Getting loose muons" << endl;
	getLooseMuons();

	// Choose electrons that pass full selection
	if (debug_)
		cout << "Getting isolated electrons" << endl;
	goodIsolatedElectrons();

	// Get the highest pt, signal electron
	if (debug_)
		cout << "Getting signal electron" << endl;
	hasSignalElectron_ = goodIsolatedElectrons_.size() > 0;
	if (hasSignalElectron_)
		signalElectron_ = goodIsolatedElectrons_.front();

	// Clean jets against signal electron
	if (debug_)
		cout << "Getting clean jets" << endl;
	cleanedJets();

	// Get b jets from cleaned jets
	if (debug_)
		cout << "Getting clean B jets" << endl;
	cleanedBJets();
}

void TopPairElectronPlusJetsSelectionFilter::getLooseElectrons() {
	looseElectrons_.clear();

	// Loop through electrons and store those that pass a loose selection
	for (size_t index = 0; index < electrons_->size(); ++index){
		const auto electron = electrons_->ptrAt(index);		
		if (isLooseElectron(electron))
			looseElectrons_.push_back(*electron);
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isLooseElectron(const edm::Ptr<pat::Electron>& electron) const {
	bool passesPtAndEta = electron->pt() > minLooseElectronPt_ && fabs(electron->eta()) < maxLooseElectronEta_;
	//		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	// bool passesID = electron.electronID("mvaTrigV0") > 0.5;
	// bool passesIso = getRelativeIsolation(electron, 0.3, rho_, isRealData_, useDeltaBetaCorrectionsForElectrons_,
	// 		useRhoActiveAreaCorrections_) < looseElectronIso_;
	bool passesID = looseElectronIDDecisions_[electron];
	bool passesIso = true; // FIXME Iso already applied in ID (check in AT)
	return passesPtAndEta && passesID && passesIso;
}

void TopPairElectronPlusJetsSelectionFilter::getLooseMuons() {
	looseMuons_.clear();

	// Loop through muons and store those that pass a loose selection
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);
		if (isLooseMuon(muon))
			looseMuons_.push_back(muon);
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isLooseMuon(const pat::Muon& muon) const {
	bool passesPtAndEta = muon.pt() > minLooseMuonPt_ && fabs(muon.eta()) < maxLooseMuonEta_;
	bool passesID = muon.isLooseMuon();
	// bool passesIso = getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) < looseMuonIso_;
	bool passesIso = muon.trackIso() / muon.pt() < 0.1;;

	return passesPtAndEta && passesID && passesIso;
}

void TopPairElectronPlusJetsSelectionFilter::goodIsolatedElectrons() {
	goodIsolatedElectrons_.clear();

	// Loop over electrons and select those that satisfy full selection
	// for (unsigned index = 0; index < electrons_.size(); ++index) {
	for (size_t index = 0; index < electrons_->size(); ++index){

		// const pat::Electron electron = electrons_.at(index);
		const auto electron = electrons_->ptrAt(index);
		// bool passesIso = getRelativeIsolation(electron, 0.3, rho_, isRealData_, useDeltaBetaCorrectionsForElectrons_,
				// useRhoActiveAreaCorrections_) < tightElectronIso_;
		bool passesIso = false;

		double relIsoWithDBeta = electronIsolation(*electron);
		if ( nonIsolatedElectronSelection_ ) {
			passesIso = relIsoWithDBeta > controlElectronIso_ ? true : false;
		}
      	else {
      		passesIso = true;
      	}

		if (isGoodElectron(electron) && passesIso) {
			goodIsolatedElectrons_.push_back(*electron);
			//Check if this is the first, and therefore the signal, electron
			if ( goodIsolatedElectrons_.size()==1 ) signalElectronIndex_ = index;
		}
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isGoodElectron(const edm::Ptr<pat::Electron>& electron) const {
	bool passesPtAndEta = electron->pt() > minSignalElectronPt_ && fabs(electron->eta()) < maxSignalElectronEta_;
	bool notInCrack = fabs(electron->superCluster()->eta()) < 1.4442 || fabs(electron->superCluster()->eta()) > 1.5660;
	bool inECAL = fabs(electron->superCluster()->eta()) < 2.5;

	//2D impact w.r.t primary vertex
	// bool passesD0 = fabs(electron.dB(pat::Electron::PV2D)) < 0.02; //cm
	// bool passesID = electron.electronID("mvaTrigV0") > 0.5;
	bool passesID = false;

	if ( nonIsolatedElectronSelection_ || invertedConversionSelection_ ) {
		passesID = passesElectronID( *electron );
	}
	else {
		passesID = signalElectronIDDecisions_[electron];
	}

	bool passesD0 = true;
	return passesPtAndEta && notInCrack && inECAL && passesD0 && passesID;
}

bool TopPairElectronPlusJetsSelectionFilter::passesElectronID(const pat::Electron& electron) const {
	// The selection for QCD control regions aren't available via electron.electronID(selectionCriteria)
	// Have to apply them by hand
	// Code based on https://github.com/lgray/cmssw/blob/common_isolation_selection_70X/TestElectronID/ElectronIDAnalyzer/plugins/ElectronIDAnalyzer.cc
	// Selection criteria from https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2

	// WARNING BAD CODING PRACTISES
	
	double dEtaIn = electron.deltaEtaSuperClusterTrackAtVtx();
	double dPhiIn = electron.deltaPhiSuperClusterTrackAtVtx();
	double hOverE = electron.hcalOverEcal();
	double isolation = electronIsolation( electron );
	// Note not using "full5x5" sigmaIetaIeta
	// double full5x5_sigmaIetaIeta = (*full5x5sieie_)[electron];
	double sigmaIetaIeta = electron.sigmaIetaIeta();

	// double d0 = (-1) * electron.gsfTrack()->dxy(pv.position() );
	double d0 = fabs(electron.dB(pat::Electron::PV2D)); //cm

	double dz = 0;
	if (vertices_.empty()) dz=1e30;
	else {
		const reco::Vertex &pv = vertices_.front();
		dz = electron.gsfTrack()->dz( pv.position() );
	}

	double ooEmooP = 0;
    if ( electron.ecalEnergy() == 0 || !std::isfinite(electron.ecalEnergy()) ) {
		ooEmooP = 1e30;
    }
    else {
		ooEmooP = fabs(1.0/electron.ecalEnergy() - electron.eSuperClusterOverP()/electron.ecalEnergy() );
    }

    unsigned int expectedMissingInnerHits = electron.gsfTrack()->hitPattern().numberOfHits(reco::HitPattern::HitCategory::MISSING_INNER_HITS);
	bool passConversionVeto = electron.passConversionVeto();

	// Now have all variables to apply electron ID
	double electronSCEta = fabs( electron.superCluster()->eta() );
	bool passesId = false;
	if ( electronSCEta <= 1.479 ) {
		// In barrel
		bool passes_dEta = dEtaIn < 0.0091 ? 1 : 0 ;
		bool passes_dPhi = dPhiIn < 0.031 ? 1 : 0 ;
		bool passes_sigmaIetaIeta = sigmaIetaIeta < 0.0106 ? 1 : 0 ;
		bool passes_hOverE = hOverE < 0.0532 ? 1 : 0 ;
		bool passes_d0 = d0 < 0.0126 ? 1 : 0;
		bool passes_dz = dz < 0.0116 ? 1 : 0 ;
		bool passes_ooEmoop = ooEmooP < 0.0609 ? 1 : 0 ;

		bool passesIso = false, passes_conversion = false;
		if ( nonIsolatedElectronSelection_ ) {
			passesIso = isolation > controlElectronIso_ ? 1 : 0;
			passes_conversion = passConversionVeto && expectedMissingInnerHits <= 1 ;
		}
		else if ( invertedConversionSelection_ ) {
			passesIso = isolation < 0.1649 ? 1 : 0;
			passes_conversion = !passConversionVeto && !(expectedMissingInnerHits <= 1) ;
		} else {
			passesIso = isolation < 0.1649 ? 1 : 0;
			passes_conversion = passConversionVeto && expectedMissingInnerHits <= 1 ;
		}

		if ( passes_dEta && passes_dPhi && passes_sigmaIetaIeta && passes_hOverE && passes_d0 && passes_dz && passes_ooEmoop && passesIso && passes_conversion ) {
			passesId = true;
		}

	}
	else if ( electronSCEta > 1.479 && electronSCEta < 2.5 ) {
		// In endcap
		bool passes_dEta = dEtaIn < 0.0106 ? 1 : 0 ;
		bool passes_dPhi = dPhiIn < 0.0359 ? 1 : 0 ;
		bool passes_sigmaIetaIeta = sigmaIetaIeta < 0.0305 ? 1 : 0 ;
		bool passes_hOverE = hOverE < 0.0835 ? 1 : 0 ;
		bool passes_d0 = d0 < 0.0163 ? 1 : 0;
		bool passes_dz = dz < 0.5999 ? 1 : 0 ;
		bool passes_ooEmoop = ooEmooP < 0.1126 ? 1 : 0 ;

		bool passesIso = false, passes_conversion = false;
		if ( nonIsolatedElectronSelection_ ) {
			passesIso = isolation > controlElectronIso_ ? 1 : 0;
			passes_conversion = passConversionVeto && expectedMissingInnerHits <= 1 ;
		}
		else if ( invertedConversionSelection_ ) {
			passesIso = isolation < 0.2075 ? 1 : 0;
			passes_conversion = !passConversionVeto && !(expectedMissingInnerHits <= 1) ;
		} else {
			passesIso = isolation < 0.2075 ? 1 : 0;
			passes_conversion = passConversionVeto && expectedMissingInnerHits <= 1 ;
		}
		if ( passes_dEta && passes_dPhi && passes_sigmaIetaIeta && passes_hOverE && passes_d0 && passes_dz && passes_ooEmoop && passesIso && passes_conversion ) {
			passesId = true;
		}
	}
	else {
		// Not interesting
		passesId = false;
	}

	return passesId;
}

double TopPairElectronPlusJetsSelectionFilter::electronIsolation(const pat::Electron& electron) const {
	reco::GsfElectron::PflowIsolationVariables pfIso = electron.pfIsolationVariables();
	// Compute isolation with delta beta correction for PU
	float absiso = pfIso.sumChargedHadronPt 
	  + std::max(0.0 , pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - 0.5 * pfIso.sumPUPt );
	return absiso/electron.pt();
}


void TopPairElectronPlusJetsSelectionFilter::cleanedJets() {
	cleanedJets_.clear();
	cleanedJetIndex_.clear();

	// Loop over jets
	unsigned int indexInNtuple = 0;
	for (unsigned index = 0; index < jets_.size(); ++index) {
		const pat::Jet jet = jets_.at(index);

		// Only jets with pt> ~20 end up in the ntuple
		// isGoodJet also requires other selection, so have to check pt here first
		// to get index of cleaned jets in jets that end up in ntuple
		if ( jet.pt() <= minJetPtInNtuples_ ) {
			continue;
		}

		// Check jet passes selection criteria
		if (!isGoodJet(jet)){
			indexInNtuple++;
			continue;
		}

		// Check if jet overlaps with the signal muon
		bool overlaps(false);
		if (tagAndProbeStudies_) {
			// Clean against all leptons for tag and probe studies
			if (goodIsolatedElectrons_.size() >= 1)
				for (unsigned index = 0; index < goodIsolatedElectrons_.size(); ++index) {
					double dR = deltaR(goodIsolatedElectrons_.at(index), jet);
					if (dR < cleaningDeltaR_) overlaps = true;
				}
		}
		else {
			if (hasSignalElectron_ && goodIsolatedElectrons_.size() == 1) {
				double dR = deltaR(signalElectron_, jet);
				overlaps = dR < cleaningDeltaR_;
			}
		}

		// Keep jet if it doesn't overlap with the signal electron
		if (!overlaps){
			cleanedJets_.push_back(jet);
			cleanedJetIndex_.push_back(indexInNtuple);
		}
		indexInNtuple++;
	}
}

void TopPairElectronPlusJetsSelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	cleanedBJetIndex_.clear();

	// Loop over cleaned jets
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);

		// Check b jet passes pt requirement (probably same as min jet pt unless assymmetric)
		if ( jet.pt()<= minBJetPt_ ) continue;

		// Does jet pass b tag selection
		if (jet.bDiscriminator(bJetDiscriminator_) > minBJetDiscriminator_) {
			// Keep if it does
			cleanedBJets_.push_back(jet);
			cleanedBJetIndex_.push_back(index);
		}
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isGoodJet(const pat::Jet& jet) const {
	//both cuts are done at PAT config level (selectedPATJets) this is just for safety
	// double smearFactor = getSmearedJetPtScale(jet, 0);
	// bool passesPtAndEta(smearFactor*jet.pt() > 20. && fabs(jet.eta()) < 2.5);

	bool passesPtAndEta(jet.pt() > minJetPtInNtuples_ && fabs(jet.eta()) < 2.4);
	bool passesJetID(false);
	bool passNOD = jet.numberOfDaughters() > 1;
	bool passNHF = jet.neutralHadronEnergyFraction() + jet.HFHadronEnergyFraction() < 0.99;
	bool passNEF = jet.neutralEmEnergyFraction() < 0.99;
	bool passCHF = true;
	bool passNCH = true;
	bool passCEF = true;
	if (fabs(jet.eta()) < 2.4) {
		passCEF = jet.chargedEmEnergyFraction() < 0.99;
		passCHF = jet.chargedHadronEnergyFraction() > 0;
		passNCH = jet.chargedMultiplicity() > 0;
	}
	passesJetID = passNOD && passCEF && passNHF && passNEF && passCHF && passNCH;

	return passesPtAndEta && passesJetID;
}

bool TopPairElectronPlusJetsSelectionFilter::passesSelectionStep(edm::Event& iEvent,
		unsigned int selectionStep) const {
	TTbarEPlusJetsReferenceSelection::Step step = TTbarEPlusJetsReferenceSelection::Step(selectionStep);
	switch (step) {
	case TTbarEPlusJetsReferenceSelection::AllEvents:
		return true;
	case TTbarEPlusJetsReferenceSelection::EventCleaningAndTrigger:
		return passesEventCleaning(iEvent) && passesTriggerSelection();
	case TTbarEPlusJetsReferenceSelection::ExactlyOneSignalElectron:
		return hasExactlyOneSignalElectron();
	case TTbarEPlusJetsReferenceSelection::LooseMuonVeto:
		return passesLooseMuonVeto();
	case TTbarEPlusJetsReferenceSelection::LooseElectronVeto:
		return passesLooseElectronVeto();
	case TTbarEPlusJetsReferenceSelection::ConversionVeto:
		return passesConversionVeto();
	case TTbarEPlusJetsReferenceSelection::AtLeastOneGoodJet:
		return hasAtLeastOneGoodJet();
	case TTbarEPlusJetsReferenceSelection::AtLeastTwoGoodJets:
		return hasAtLeastTwoGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastThreeGoodJets:
		return hasAtLeastThreeGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastFourGoodJets:
		return hasAtLeastFourGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastOneBtag:
		return hasAtLeastOneGoodBJet();
	case TTbarEPlusJetsReferenceSelection::AtLeastTwoBtags:
		return hasAtLeastTwoGoodBJets();
	default:
		break;
	}

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::passesEventCleaning(edm::Event& iEvent) const {
	return true;
}

bool TopPairElectronPlusJetsSelectionFilter::passesTriggerSelection() const {
	// if (dropTriggerSelection_)
	// 	return true;
	// else if (isRealData_) {
	// 	//2011 data: run 160404 to run 180252
	// 	if (runNumber_ >= 160404 && runNumber_ <= 163869)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30", hltConfig_, triggerResults_);
	// 	else if (runNumber_ > 163869 && runNumber_ <= 165633)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30", hltConfig_, triggerResults_);
	// 	else if (runNumber_ > 165633 && runNumber_ <= 178380)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30", hltConfig_,
	// 				triggerResults_);
	// 	else if (runNumber_ > 178380 && runNumber_ <= 180252)
	// 		return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFJet30", hltConfig_,
	// 				triggerResults_);
	// 	//2012 data: run 190456 to run 208686
	// 	else if (runNumber_ >= 190456 && runNumber_ <= 208686) //2012 data
	// 		return triggerFired("HLT_Ele27_WP80_v", hltConfig_, triggerResults_);

	// } else {
	// 	if (MCSampleTag_ == "Fall11") {	//Fall11 MC
	// 		return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30", hltConfig_, triggerResults_);
	// 	} else if (MCSampleTag_ == "Summer12") { //Summer12 MC
	// 		return triggerFired("HLT_Ele27_WP80_v", hltConfig_, triggerResults_);
	// 	} else if (MCSampleTag_ == "Summer11Leg") { //7TeV legacy MC
	// 		return true; // to be updated once we have trigger efficiencies
	// 	} else
	// 		return false;
	// }
	// return false;
	return true;
}

bool TopPairElectronPlusJetsSelectionFilter::hasExactlyOneSignalElectron() const {
	if (tagAndProbeStudies_)
		return goodIsolatedElectrons_.size() >= 1;
	else {
		return goodIsolatedElectrons_.size() == 1;
	}
}

bool TopPairElectronPlusJetsSelectionFilter::passesLooseMuonVeto() const {
	// Require no electrons in the event
	return looseMuons_.size() == 0;
}

bool TopPairElectronPlusJetsSelectionFilter::passesLooseElectronVeto() const {
	double invariantMass = 0;
	bool isZEvent = false;

	if (tagAndProbeStudies_) {
		if ( (looseElectrons_.size() >= 1) && hasSignalElectron_ ) {
			for (unsigned int index = 0; index < electrons_->size(); ++index) {
				const pat::Electron probeElectron_ = electrons_->at(index);
				// skip the tag electron itself
				if (probeElectron_.p4() == signalElectron_.p4())
					continue;
				invariantMass = (signalElectron_.p4()+probeElectron_.p4()).mass();
				bool passesLowerLimit = invariantMass > 60;
				bool passesUpperLimit = invariantMass < 120;
				if (passesLowerLimit && passesUpperLimit)
					isZEvent = true;
			}
		}
		return isZEvent == true;
	}
	else
		// Require only one loose electron, which is the signal electron
		return looseElectrons_.size() < 2;
}

bool TopPairElectronPlusJetsSelectionFilter::passesConversionVeto() const {
	if (!hasExactlyOneSignalElectron())
		return false;

	bool passVeto = signalElectron_.passConversionVeto();

   if ( invertedConversionSelection_ )
           return !passVeto;
   else
           return passVeto;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastOneGoodJet() const {
	if (cleanedJets_.size() > 0)
		return cleanedJets_.at(0).pt() > min1JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(0), 0)*cleanedJets_.at(0).pt() > min1JetPt_;

	return false;

}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastTwoGoodJets() const {
	if (cleanedJets_.size() > 1)
		return cleanedJets_.at(1).pt() > min2JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(1), 0)*cleanedJets_.at(1).pt() > min2JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastThreeGoodJets() const {
	if (cleanedJets_.size() > 2)
		return cleanedJets_.at(2).pt() > min3JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(2), 0)*cleanedJets_.at(2).pt() > min3JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastFourGoodJets() const {
	if (cleanedJets_.size() > 3)
		return cleanedJets_.at(3).pt() > min4JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(3), 0)*cleanedJets_.at(3).pt() > min4JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasExactlyZeroGoodBJet() const {
       return cleanedBJets_.size() == 0;
}

bool TopPairElectronPlusJetsSelectionFilter::hasExactlyOneGoodBJet() const {
       return cleanedBJets_.size() == 1;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastOneGoodBJet() const {
	return cleanedBJets_.size() > 0;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastTwoGoodBJets() const {
	return cleanedBJets_.size() > 1;
}

// ------------ method called once each job just before starting event loop  ------------
void TopPairElectronPlusJetsSelectionFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TopPairElectronPlusJetsSelectionFilter::endJob() {
}

bool TopPairElectronPlusJetsSelectionFilter::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {

	bool changed = true;
	if (hltConfig_.init(iRun, iSetup, hltInputTag_.process(), changed)) {
		// if init returns TRUE, initialisation has succeeded!
		edm::LogInfo("TopPairElectronPlusJetsSelectionFilter") << "HLT config with process name "
				<< hltInputTag_.process() << " successfully extracted";
	} else {
		// if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
		// with the file and/or code and needs to be investigated!
		edm::LogError("TopPairElectronPlusJetsSelectionFilter_Error")
				<< "Error! HLT config extraction with process name " << hltInputTag_.process() << " failed";
		// In this case, all access methods will return empty values!
	}
	return true;
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairElectronPlusJetsSelectionFilter);
