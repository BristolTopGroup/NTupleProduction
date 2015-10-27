#include "BristolAnalysis/NTupleTools/plugins/TopPairMuonPlusJetsSelectionFilter.h"
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

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;

TopPairMuonPlusJetsSelectionFilter::TopPairMuonPlusJetsSelectionFilter(const edm::ParameterSet& iConfig) :
		// Input tags
		jetInput_(iConfig.getParameter < edm::InputTag > ("jetInput")), //
		electronInput_(iConfig.getParameter < edm::InputTag > ("electronInput")), //
		muonInput_(iConfig.getParameter < edm::InputTag > ("muonInput")), //
		hltInputTag_(iConfig.getParameter < edm::InputTag > ("HLTInput")), //
		VertexInput_(iConfig.getParameter < edm::InputTag > ("VertexInput")), //

		// Selection criteria
		minSignalMuonPt_(iConfig.getParameter<double>("minSignalMuonPt")), //
		maxSignalMuonEta_(iConfig.getParameter<double>("maxSignalMuonEta")), //
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

		tightMuonIso_(iConfig.getParameter<double>("tightMuonIsolation")), //
        controlMuonIso1_(iConfig.getParameter<double>("controlMuonIsolation1")), //
        controlMuonIso2_(iConfig.getParameter<double>("controlMuonIsolation2")), //
        looseMuonIso_(iConfig.getParameter<double>("looseMuonIsolation")), //

		// Flags and labels
		tagAndProbeStudies_(iConfig.getParameter<bool>("tagAndProbeStudies")), //
		dropTriggerSelection_(iConfig.getParameter<bool>("dropTriggerSelection")), //
		prefix_(iConfig.getUntrackedParameter < std::string > ("prefix")), //
		MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
		debug_(iConfig.getUntrackedParameter<bool>("debug")), //
		taggingMode_(iConfig.getParameter<bool>("taggingMode")), //
		bSelectionInTaggingMode_(iConfig.getParameter<bool>("bSelectionInTaggingMode")), //
		nonIsolatedMuonSelection1_(iConfig.getParameter<bool>("nonIsolatedMuonSelection1")), //
		nonIsolatedMuonSelection2_(iConfig.getParameter<bool>("nonIsolatedMuonSelection2")), //
		passes_(), //
		runNumber_(0), //
		signalMuonIndex_(999), //
		isRealData_(false), //
		hasSignalMuon_(false), //
		hasGoodPV_(false), //
		cleanedJetIndex_(),
		cleanedBJetIndex_(),
		jets_(), //,
		cleanedJets_(), //
		cleanedBJets_(), //
		electrons_(), //
		looseElectrons_(), //
		muons_(), //
		goodIsolatedMuons_(), //
		looseMuons_(), //
		signalMuon_(), //
		hltConfig_(), //
		triggerResults_(), //
		primaryVertex_() {
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		passes_.at(step) = 0;
		produces<bool>(prefix_ + TTbarMuPlusJetsReferenceSelection::StringSteps[step]);
	}
	produces<bool>(prefix_ + "FullSelection");
	produces<unsigned int>(prefix_ + "NumberOfBtags");
	produces<unsigned int>(prefix_ + "NumberOfJets");
	produces<std::vector<unsigned int> >(prefix_ + "cleanedJetIndex");
	produces<std::vector<unsigned int> >(prefix_ + "cleanedBJetIndex");
	// produces < pat::JetCollection > (prefix_ + "cleanedJets");
	produces<unsigned int>(prefix_ + "signalMuonIndex");
}

void TopPairMuonPlusJetsSelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("jetInput");
	desc.add < InputTag > ("electronInput");
	desc.add < InputTag > ("muonInput");
	desc.add < InputTag > ("HLTInput");
	desc.add < InputTag > ("VertexInput");
	
	desc.add<double>("minSignalMuonPt",0.);
	desc.add<double>("maxSignalMuonEta",10.);
	desc.add<double>("minLooseMuonPt",0.);
	desc.add<double>("maxLooseMuonEta",10.);
	desc.add<double>("minLooseElectronPt",0.);
	desc.add<double>("maxLooseElectronEta",10.);
	desc.add < InputTag > ("looseElectronIDMap");
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

	desc.add<double>("tightMuonIsolation", 0.12);
	desc.add<double>("controlMuonIsolation", 0.3);
	desc.add<double>("looseMuonIsolation", 0.2);

	desc.add<bool>("tagAndProbeStudies", false);
	desc.add<bool>("dropTriggerSelection", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairMuonPlusJetsSelection.");
	desc.addUntracked<bool>("debug", false);
	desc.add<bool>("taggingMode", false);
	desc.add<bool>("bSelectionInTaggingMode", false);
	desc.add<bool>("nonIsolatedMuonSelection", false);
	descriptions.add("applyTopPairMuonPlusJetsSelection", desc);
}

TopPairMuonPlusJetsSelectionFilter::~TopPairMuonPlusJetsSelectionFilter() {

}

bool TopPairMuonPlusJetsSelectionFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	// Get content from event
	// Including selecting a signal muon, loose leptons, jets and bjets
	setupEventContent(iEvent, iSetup);

	// Loop through each selection step in order and check if event satisfies each criterion
	bool passesSelection(true);
	bool passesSelectionExceptBtagging(true);
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		TTbarMuPlusJetsReferenceSelection::Step stepName = TTbarMuPlusJetsReferenceSelection::Step(step);
		if (debug_)
			cout << "Doing selection step: " << TTbarMuPlusJetsReferenceSelection::StringSteps[step] << endl;

		bool passesStep(passesSelectionStep(iEvent, step));

		// Remove at least 4 jet selection for QCD control region (only need at least 3)
		// Also require exactly zero b jets
		// Or exactly one b jet, as e.g. angle(b,l) only makes sense if there is at least one b jet
		if ( nonIsolatedMuonSelection1_ || nonIsolatedMuonSelection2_) {
			if ( stepName == TTbarMuPlusJetsReferenceSelection::AtLeastFourGoodJets )
				passesStep = true;

			if ( stepName == TTbarMuPlusJetsReferenceSelection::AtLeastOneBtag || stepName == TTbarMuPlusJetsReferenceSelection::AtLeastTwoBtags ) {
				passesStep = hasExactlyZeroGoodBJet() || hasExactlyOneGoodBJet() ;
			}
		}

		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;

		// Note if event passes all but bjet selection steps
		if ( step < TTbarMuPlusJetsReferenceSelection::AtLeastOneBtag )
			passesSelectionExceptBtagging = passesSelectionExceptBtagging && passesStep;

		// if doesn't pass selection and not in tagging mode, stop here to save CPU time
		if ( !(taggingMode_ || passesSelection) )
			break;
	}

	// Store info in event
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarMuPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");

	// Store number of cleaned jets in event
	unsigned int numberOfJets(cleanedJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfJets)), prefix_ + "NumberOfJets");

	// Store indices of cleaned jets in event
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedJetIndex_)), prefix_ + "cleanedJetIndex");

	// Store number of b tags in event
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedBJetIndex_)), prefix_ + "cleanedBJetIndex");

	// Store index of signal muon
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(signalMuonIndex_)),prefix_ + "signalMuonIndex");

	if ( !bSelectionInTaggingMode_ )
		return taggingMode_ || passesSelection;
	else
		return taggingMode_ || passesSelectionExceptBtagging;
}

void TopPairMuonPlusJetsSelectionFilter::setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	
	if (debug_)
		cout << "Setting up the event content" << endl;

	// Event info
	runNumber_ = iEvent.run();
	isRealData_ = iEvent.isRealData();

	// Trigger results
	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByLabel(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	// Primary vertices
	edm::Handle < reco::VertexCollection > primaryVertices;
	iEvent.getByLabel(VertexInput_, primaryVertices);
	if (primaryVertices.isValid()) {
		if (primaryVertices->size() >= 1) {
			primaryVertex_ = primaryVertices->at(0);
			hasGoodPV_ = true;
		} else
			hasGoodPV_ = false;
	} else
		edm::LogError("TopPairMuonPlusJetsSelectionFilterError") << "Error! Can't get the product " << VertexInput_;

	// Jet collection
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(jetInput_, jets);
	jets_ = *jets;

	if ( applyJEC_ ) {
		corrector_ = JetCorrector::getJetCorrector (jetCorrectionService_, iSetup);
		jets_ = applyNewJec( jets_, corrector_, iEvent, iSetup );
	}

	// Electrons (for veto)
	iEvent.getByLabel(electronInput_, electrons_);

	// Electron VID Decisions
	Handle<edm::ValueMap<bool> > loose_id_decisions;
	iEvent.getByToken(looseElectronIDMapToken_,loose_id_decisions);
	looseElectronIDDecisions_ = *loose_id_decisions;

	// Muons
	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByLabel(muonInput_, muons);
	muons_ = *muons;

	// Choose electrons that pass the loose selection
	if (debug_)
		cout << "Getting loose electrons" << endl;
	getLooseElectrons();

	if (muons.isValid()) {
		// Choose muons that pass the loose selection
		if (debug_)
			cout << "Getting loose muons" << endl;
		getLooseMuons();

		// Choose muons that pass the full selection
		if (debug_)
			cout << "Getting isolated muons" << endl;
		goodIsolatedMuons();

		// Get the highest pt, signal muon
		if (debug_)
			cout << "Getting signal muon" << endl;
		hasSignalMuon_ = goodIsolatedMuons_.size() > 0;
		if (hasSignalMuon_)
			signalMuon_ = goodIsolatedMuons_.front();

	} else {
		edm::LogError("TopPairMuonPlusJetsSelectionFilterError") << "Error! Can't get the product " << muonInput_;
	}

	// Clean jets against signal muon
	if (debug_)
		cout << "Getting clean jets" << endl;
	cleanedJets();

	// Get b jets from cleaned jets
	if (debug_)
		cout << "Getting clean B jets" << endl;
	cleanedBJets();
}

void TopPairMuonPlusJetsSelectionFilter::getLooseElectrons() {
	looseElectrons_.clear();

	// Loop through electrons and store those that pass a loose selection
	for (size_t index = 0; index < electrons_->size(); ++index){
		const auto electron = electrons_->ptrAt(index);		
		if (isLooseElectron(electron))
			looseElectrons_.push_back(*electron);
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isLooseElectron(const edm::Ptr<pat::Electron>& electron) const {
	bool passesPtAndEta = electron->pt() > minLooseElectronPt_ && fabs(electron->eta()) < maxLooseElectronEta_;
	//		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	// bool passesID = electron.electronID("mvaTrigV0") > 0.5;

	bool passesID = looseElectronIDDecisions_[electron];
	bool passesIso = true;

	return passesPtAndEta && passesID && passesIso;
}

void TopPairMuonPlusJetsSelectionFilter::getLooseMuons() {
	looseMuons_.clear();

	// Loop through muons and store those that pass a loose selection
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);
		if (isLooseMuon(muon))
			looseMuons_.push_back(muon);
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isLooseMuon(const pat::Muon& muon) const {
	bool passesPtAndEta = muon.pt() > minLooseMuonPt_ && fabs(muon.eta()) < maxLooseMuonEta_;
	bool passesID = muon.isLooseMuon();
	bool passesIso = getRelativeIsolation(muon, 0.4, true) < looseMuonIso_;
	// bool passesIso = muon.trackIso() / muon.pt() < 0.1;;

	return passesPtAndEta && passesID && passesIso;
}

void TopPairMuonPlusJetsSelectionFilter::goodIsolatedMuons() {
	goodIsolatedMuons_.clear();

	// Get muons that pass the full selection
	unsigned int indexToStore = 0;
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);

		// Only these muons are stored in the ntuple
		// Due to info on tracks not being available for SA muons
		// This is part of tight muon ID
		// But still have to do this (and faff with indexToStore) to get index of 
		// muon out of those that get stored in the ntuple (all but SA muons)
		if (!( muon.isGlobalMuon() || muon.isTrackerMuon() ) )
			continue;

		// bool passesIso = getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) < tightMuonIso_;
		bool passesIso = false;

        if ( nonIsolatedMuonSelection1_ ) {
        	passesIso = getRelativeIsolation(muon, 0.4, true) > controlMuonIso1_;
        }
        if ( nonIsolatedMuonSelection2_ ) {
        	passesIso = getRelativeIsolation(muon, 0.4, true) > controlMuonIso2_ 
        		&& getRelativeIsolation(muon, 0.4, true) < controlMuonIso2_;
        	// passesIso = muon.trackIso() / muon.pt() > controlMuonIso_;
		}
	   	else {
           	passesIso = getRelativeIsolation(muon, 0.4, true) < tightMuonIso_;
        	// passesIso = muon.trackIso() / muon.pt() < tightMuonIso_;
	   	}


		if (isGoodMuon(muon) && passesIso) {
			goodIsolatedMuons_.push_back(muon);

			//Check if this is the first, and therefore the signal, muon
			if ( goodIsolatedMuons_.size()==1 ) signalMuonIndex_ = indexToStore;
		}
		++indexToStore;
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isGoodMuon(const pat::Muon& muon) const {

	// Pt and eta selection
	bool passesPtAndEta = muon.pt() > minSignalMuonPt_ && fabs(muon.eta()) < maxSignalMuonEta_;

	// Passes ID Selection
	bool passesID = false;
	if ( hasGoodPV_ ) {
		passesID = muon.isTightMuon( primaryVertex_ );
	}

	return passesPtAndEta && passesID;
}

void TopPairMuonPlusJetsSelectionFilter::cleanedJets() {
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
		if (!isGoodJet(jet)) {
			indexInNtuple++;
			continue;
		}

		// Check if jet overlaps with the signal muon
		bool overlaps(false);
		if (tagAndProbeStudies_) {
			// Clean against all leptons for tag and probe studies
			if (goodIsolatedMuons_.size() >= 1)
				for (unsigned index = 0; index < goodIsolatedMuons_.size(); ++index) {
					double dR = deltaR(goodIsolatedMuons_.at(index), jet);
					if (dR < cleaningDeltaR_) overlaps = true;
				}
		}
		else {
			if (hasSignalMuon_ && goodIsolatedMuons_.size() == 1) {
				double dR = deltaR(signalMuon_, jet);
				overlaps = (dR < cleaningDeltaR_);
			}
		}
		// Keep jet if it doesn't overlap with the signal muon
		if (!overlaps){
			cleanedJets_.push_back(jet);
			cleanedJetIndex_.push_back(indexInNtuple);
		}
		indexInNtuple++;		
	}
}

void TopPairMuonPlusJetsSelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	cleanedBJetIndex_.clear();
	
	// Loop over cleaned jets
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);

		// Check b jet passes pt requirement (probably same as min jet pt unless assymmetric)
		if ( jet.pt() <= minBJetPt_ ) continue;

		// Does jet pass b tag selection
		if (jet.bDiscriminator(bJetDiscriminator_) > minBJetDiscriminator_) {
			// Keep if it does
			cleanedBJets_.push_back(jet);
			cleanedBJetIndex_.push_back(index);
		}
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isGoodJet(const pat::Jet& jet) const {
	//both cuts are done at PAT config level (selectedPATJets) this is just for safety
	// double smearFactor = getSmearedJetPtScale(jet, 0);
	// bool passesPtAndEta(smearFactor*jet.pt() > 20. && fabs(jet.eta()) < 2.5);
	bool passesPtAndEta(jet.pt() > minJetPtInNtuples_ && fabs(jet.eta()) < 2.4);
	bool passesJetID(false);
	bool passNOD = jet.numberOfDaughters() > 1;
	bool passNHF = jet.neutralHadronEnergyFraction() + jet.HFHadronEnergyFraction()  < 0.99;
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

bool TopPairMuonPlusJetsSelectionFilter::passesSelectionStep(edm::Event& iEvent, unsigned int selectionStep) const {
	TTbarMuPlusJetsReferenceSelection::Step step = TTbarMuPlusJetsReferenceSelection::Step(selectionStep);
	switch (step) {
	case TTbarMuPlusJetsReferenceSelection::AllEvents:
		return true;
	case TTbarMuPlusJetsReferenceSelection::EventCleaningAndTrigger:
		return passesEventCleaning(iEvent) && passesTriggerSelection();
	case TTbarMuPlusJetsReferenceSelection::ExactlyOneSignalMuon:
		return hasExactlyOneSignalMuon();
	case TTbarMuPlusJetsReferenceSelection::LooseMuonVeto:
		return passesLooseMuonVeto();
	case TTbarMuPlusJetsReferenceSelection::LooseElectronVeto:
		return passesLooseElectronVeto();
	case TTbarMuPlusJetsReferenceSelection::AtLeastOneGoodJet:
		return hasAtLeastOneGoodJet();
	case TTbarMuPlusJetsReferenceSelection::AtLeastTwoGoodJets:
		return hasAtLeastTwoGoodJets();
	case TTbarMuPlusJetsReferenceSelection::AtLeastThreeGoodJets:
		return hasAtLeastThreeGoodJets();
	case TTbarMuPlusJetsReferenceSelection::AtLeastFourGoodJets:
		return hasAtLeastFourGoodJets();
	case TTbarMuPlusJetsReferenceSelection::AtLeastOneBtag:
		return hasAtLeastOneGoodBJet();
	case TTbarMuPlusJetsReferenceSelection::AtLeastTwoBtags:
		return hasAtLeastTwoGoodBJets();
	default:
		break;
	}

	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::passesEventCleaning(edm::Event& iEvent) const {
	return true;
}

bool TopPairMuonPlusJetsSelectionFilter::passesTriggerSelection() const {
	// if (dropTriggerSelection_) 
	// 	return true;
	// else if (isRealData_) {
	// 	if (runNumber_ >= 160404 && runNumber_ < 173236)
	// 		return triggerFired("HLT_IsoMu24", hltConfig_, triggerResults_);
	// 	else if (runNumber_ >= 173236 && runNumber_ < 190456)
	// 		return triggerFired("HLT_IsoMu24_eta2p1", hltConfig_, triggerResults_);
	// 	else //2012 Data
	// 		return triggerFired("HLT_IsoMu24_eta2p1_v", hltConfig_, triggerResults_);
	// } else {
	// 	if (MCSampleTag_ == "Fall11") {//Fall11 MC
	// 		return triggerFired("HLT_IsoMu24", hltConfig_, triggerResults_);
	// 	} else if (MCSampleTag_ == "Summer12") {//Summer12 MC
	// 		return triggerFired("HLT_IsoMu24_eta2p1_v", hltConfig_, triggerResults_);
	// 	} else if (MCSampleTag_ == "Summer11Leg") {//Summer11Leg
	// 		return true; // to be updated once we have trigger efficiencies
	// 	}
	// }
	// return false;

	return true;
}

bool TopPairMuonPlusJetsSelectionFilter::hasExactlyOneSignalMuon() const {
	if (tagAndProbeStudies_) {
		// Need two signal muons for tag and probe studies
		return goodIsolatedMuons_.size() >= 1;
	}
	else {
		// Require exactly one signal muon for main analysis
		return goodIsolatedMuons_.size() == 1;
	}
}

bool TopPairMuonPlusJetsSelectionFilter::passesLooseElectronVeto() const {
	// Require no electrons in the event
	return looseElectrons_.size() == 0;
}

bool TopPairMuonPlusJetsSelectionFilter::passesLooseMuonVeto() const {
	double invariantMass = 0;
	bool isZEvent = false;

	if (tagAndProbeStudies_) {
		if ( (looseMuons_.size() >= 1) && hasSignalMuon_ ) {
			for (unsigned int index = 0; index < muons_.size(); ++index) {
				const pat::Muon probeMuon_ = muons_.at(index);
				// skip the tag muon itself
				if (probeMuon_.p4() == signalMuon_.p4())
					continue;
				invariantMass = (signalMuon_.p4()+probeMuon_.p4()).mass();
				bool passesLowerLimit = invariantMass > 60;
				bool passesUpperLimit = invariantMass < 120;
				if (passesLowerLimit && passesUpperLimit)
					isZEvent = true;
			}
		}
		return isZEvent == true;
	}
	else
		// Require only one loose muon, which is the signal muons
		return looseMuons_.size() < 2;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastOneGoodJet() const {
	if (cleanedJets_.size() > 0)
		return cleanedJets_.at(0).pt() > min1JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(0), 0)*cleanedJets_.at(0).pt() > min1JetPt_;

	return false;

}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastTwoGoodJets() const {
	if (cleanedJets_.size() > 1)
		return cleanedJets_.at(1).pt() > min2JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(1), 0)*cleanedJets_.at(1).pt() > min2JetPt_;

	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastThreeGoodJets() const {
	if (cleanedJets_.size() > 2)
		return cleanedJets_.at(2).pt() > min3JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(2), 0)*cleanedJets_.at(2).pt() > min3JetPt_;

	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastFourGoodJets() const {
	if (cleanedJets_.size() > 3)
		return cleanedJets_.at(3).pt() > min4JetPt_;
		// return getSmearedJetPtScale(cleanedJets_.at(3), 0)*cleanedJets_.at(3).pt() > min4JetPt_;

	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasExactlyZeroGoodBJet() const {
       return cleanedBJets_.size() == 0;
}

bool TopPairMuonPlusJetsSelectionFilter::hasExactlyOneGoodBJet() const {
       return cleanedBJets_.size() == 1;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastOneGoodBJet() const {
	return cleanedBJets_.size() >= 1;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastTwoGoodBJets() const {
	return cleanedBJets_.size() >= 2;
}

// ------------ method called once each job just before starting event loop  ------------
void TopPairMuonPlusJetsSelectionFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TopPairMuonPlusJetsSelectionFilter::endJob() {
}

bool TopPairMuonPlusJetsSelectionFilter::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {

	bool changed = true;
	if (hltConfig_.init(iRun, iSetup, hltInputTag_.process(), changed)) {
		// if init returns TRUE, initialisation has succeeded!
		edm::LogInfo("TopPairMuonPlusJetsSelectionFilter") << "HLT config with process name "
				<< hltInputTag_.process() << " successfully extracted";
	} else {
		// if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
		// with the file and/or code and needs to be investigated!
		edm::LogError("TopPairMuonPlusJetsSelectionFilter_Error")
				<< "Error! HLT config extraction with process name " << hltInputTag_.process() << " failed";
		// In this case, all access methods will return empty values!
	}
	return true;
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairMuonPlusJetsSelectionFilter);
