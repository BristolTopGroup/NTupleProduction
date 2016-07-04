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
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;

TopPairMuonPlusJetsSelectionFilter::TopPairMuonPlusJetsSelectionFilter(const edm::ParameterSet& iConfig) :
				// Input tags
				jetInput_(consumes < pat::JetCollection > (iConfig.getParameter < edm::InputTag > ("jetInput"))), //
				electronInput_(
						consumes < edm::View<pat::Electron>
								> (iConfig.getParameter < edm::InputTag > ("electronInput"))), //
				muonInput_(consumes < pat::MuonCollection > (iConfig.getParameter < edm::InputTag > ("muonInput"))), //
				hltInputTag_(consumes < edm::TriggerResults > (iConfig.getParameter < edm::InputTag > ("HLTInput"))), //

				// Selection criteria
				cleaningDeltaR_(iConfig.getParameter<double>("cleaningDeltaR")), //

				minBJetDiscriminator_(iConfig.getParameter<double>("minBJetDiscriminator")), //
				tightBJetDiscriminator_(iConfig.getParameter<double>("tightBJetDiscriminator")), //

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
				cleanedJetIndex_(),
				cleanedBJetIndex_(),
				cleanedTightBJetIndex_(),
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
				triggerResults_()
	{
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		passes_.at(step) = 0;
		produces<bool>(prefix_ + TTbarMuPlusJetsReferenceSelection::StringSteps[step]);
	}
	produces<bool>(prefix_ + "FullSelection");
	produces<bool>(prefix_ + "FullSelectionNoB");
	produces<bool>(prefix_ + "FullSelection2Tight");
	produces<unsigned int>(prefix_ + "NumberOfBtags");
	produces<unsigned int>(prefix_ + "NumberOfJets");
	produces < std::vector<unsigned int> > (prefix_ + "cleanedJetIndex");
	produces < std::vector<unsigned int> > (prefix_ + "cleanedBJetIndex");
	produces < std::vector<unsigned int> > (prefix_ + "cleanedTightBJetIndex");
	// produces < pat::JetCollection > (prefix_ + "cleanedJets");
	produces<unsigned int>(prefix_ + "signalMuonIndex");
}

void TopPairMuonPlusJetsSelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("jetInput");
	desc.add < InputTag > ("electronInput");
	desc.add < InputTag > ("muonInput");
	desc.add < InputTag > ("HLTInput");

	desc.add<double>("cleaningDeltaR", 0.3);

	desc.add<double>("minBJetDiscriminator", 0.800);
	desc.add<double>("tightBJetDiscriminator", 0.935);


	desc.add<bool>("tagAndProbeStudies", false);
	desc.add<bool>("dropTriggerSelection", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairMuonPlusJetsSelection.");
	desc.addUntracked<bool>("debug", false);
	desc.add<bool>("taggingMode", false);
	desc.add<bool>("bSelectionInTaggingMode", false);
	desc.add<bool>("nonIsolatedMuonSelection1", false);
	desc.add<bool>("nonIsolatedMuonSelection2", false);
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
	bool passesSelectionWithTightBtagging(true);

	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		TTbarMuPlusJetsReferenceSelection::Step stepName = TTbarMuPlusJetsReferenceSelection::Step(step);
		if (debug_)
			cout << "Doing selection step: " << TTbarMuPlusJetsReferenceSelection::StringSteps[step] << endl;

		bool passesStep(passesSelectionStep(iEvent, step));

		// Remove at least 4 jet selection for QCD control region (only need at least 3)
		// Also require exactly zero b jets
		// Or exactly one b jet, as e.g. angle(b,l) only makes sense if there is at least one b jet
		if (nonIsolatedMuonSelection1_ || nonIsolatedMuonSelection2_) {
			if (stepName == TTbarMuPlusJetsReferenceSelection::AtLeastFourGoodJets)
				passesStep = true;

			if (stepName == TTbarMuPlusJetsReferenceSelection::AtLeastOneBtag
					|| stepName == TTbarMuPlusJetsReferenceSelection::AtLeastTwoBtags) {
				passesStep = hasExactlyZeroGoodBJet() || hasExactlyOneGoodBJet();
			}
		}

		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;

		// Note if event passes all but bjet selection steps
		if (step < TTbarMuPlusJetsReferenceSelection::AtLeastOneBtag)
			passesSelectionExceptBtagging = passesSelectionExceptBtagging && passesStep;

		// if doesn't pass selection and not in tagging mode, stop here to save CPU time
		if (!(taggingMode_ || passesSelection))
			break;
	}

	if (passesSelection) {
		passesSelectionWithTightBtagging = hasAtLeastTwoGoodTightBJets();
	}

	// Store info in event
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarMuPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelectionExceptBtagging)), prefix_ + "FullSelectionNoB");
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelectionWithTightBtagging)), prefix_ + "FullSelection2Tight");

	// Store number of cleaned jets in event
	unsigned int numberOfJets(cleanedJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfJets)), prefix_ + "NumberOfJets");

	// Store indices of cleaned jets in event
	iEvent.put(std::auto_ptr < std::vector<unsigned int> > (new std::vector<unsigned int>(cleanedJetIndex_)),
			prefix_ + "cleanedJetIndex");

	// Store number of b tags in event
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	iEvent.put(std::auto_ptr < std::vector<unsigned int> > (new std::vector<unsigned int>(cleanedBJetIndex_)),
			prefix_ + "cleanedBJetIndex");
	iEvent.put(std::auto_ptr < std::vector<unsigned int> > (new std::vector<unsigned int>(cleanedTightBJetIndex_)),
			prefix_ + "cleanedTightBJetIndex");

	// Store index of signal muon
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(signalMuonIndex_)), prefix_ + "signalMuonIndex");

	if (!bSelectionInTaggingMode_)
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
	iEvent.getByToken(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	// Jet collection
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByToken(jetInput_, jets);
	jets_ = *jets;

	// Electrons (for veto)
	iEvent.getByToken(electronInput_, electrons_);

	// Muons
	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByToken(muonInput_, muons);
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
	for (size_t index = 0; index < electrons_->size(); ++index) {
		const auto electron = electrons_->ptrAt(index);
		if (electron->userInt("isLoose"))
			looseElectrons_.push_back(*electron);
	}
}

void TopPairMuonPlusJetsSelectionFilter::getLooseMuons() {
	looseMuons_.clear();

	// Loop through muons and store those that pass a loose selection
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon& muon = muons_.at(index);
		if (muon.userInt("isLoose"))
			looseMuons_.push_back(muon);
	}
}

void TopPairMuonPlusJetsSelectionFilter::goodIsolatedMuons() {
	goodIsolatedMuons_.clear();

	// Get muons that pass the full selection
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon& muon = muons_.at(index);

		// Only these muons are stored in the ntuple
		// Due to info on tracks not being available for SA muons
		// This is part of tight muon ID
		// But still have to do this (and faff with indexToStore) to get index of 
		// muon out of those that get stored in the ntuple (all but SA muons)
		if (!(muon.isGlobalMuon() || muon.isTrackerMuon()))
			continue;

		bool isGood = false;

		if (nonIsolatedMuonSelection1_) {
			isGood = muon.userInt("isGoodNonIsoR1");
		} else if (nonIsolatedMuonSelection2_) {
			isGood = muon.userInt("isGoodNonIsoR2");
		} else {
			isGood = muon.userInt("isGood");
		}

		if (isGood) {
			goodIsolatedMuons_.push_back(muon);

			//Check if this is the first, and therefore the signal, muon
			if (goodIsolatedMuons_.size() == 1)
				signalMuonIndex_ = index;
		}
	}
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
		if (!jet.userInt("passesPt")) {
			continue;
		}

		// Check jet passes selection criteria
		if (!jet.userInt("isGood")) {
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
					if (dR < cleaningDeltaR_)
						overlaps = true;
				}
		} else {
			if (hasSignalMuon_ && goodIsolatedMuons_.size() == 1) {
				double dR = deltaR(signalMuon_, jet);
				overlaps = (dR < cleaningDeltaR_);
			}
		}
		// Keep jet if it doesn't overlap with the signal muon
		if (!overlaps) {
			cleanedJets_.push_back(jet);
			cleanedJetIndex_.push_back(indexInNtuple);
		}
		indexInNtuple++;
	}
}

void TopPairMuonPlusJetsSelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	cleanedBJetIndex_.clear();
	cleanedTightBJetIndex_.clear();

	// Loop over cleaned jets
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);

		// Check b jet passes pt requirement (probably same as min jet pt unless assymmetric)
		if (!jet.userInt("passesPt"))
			continue;

		// Does jet pass b tag selection
		if (jet.userFloat("btagDiscriminator") > minBJetDiscriminator_) {
			// Keep if it does
			cleanedBJets_.push_back(jet);
			cleanedBJetIndex_.push_back(index);
			if (jet.userFloat("btagDiscriminator") > tightBJetDiscriminator_) {
				cleanedTightBJetIndex_.push_back(index);
			}
		}
	}
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
	} else {
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
		if ((looseMuons_.size() >= 1) && hasSignalMuon_) {
			for (unsigned int index = 0; index < muons_.size(); ++index) {
				const pat::Muon probeMuon_ = muons_.at(index);
				// skip the tag muon itself
				if (probeMuon_.p4() == signalMuon_.p4())
					continue;
				invariantMass = (signalMuon_.p4() + probeMuon_.p4()).mass();
				bool passesLowerLimit = invariantMass > 60;
				bool passesUpperLimit = invariantMass < 120;
				if (passesLowerLimit && passesUpperLimit)
					isZEvent = true;
			}
		}
		return isZEvent == true;
	} else
		// Require only one loose muon, which is the signal muons
		return looseMuons_.size() < 2;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastOneGoodJet() const {
	if (cleanedJets_.size() > 0)
		return cleanedJets_.at(0).userInt("passesPt");

	return false;

}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastTwoGoodJets() const {
	if (cleanedJets_.size() > 1)
		return cleanedJets_.at(1).userInt("passesPt");

	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastThreeGoodJets() const {
	if (cleanedJets_.size() > 2)
		return cleanedJets_.at(2).userInt("passesPt");

	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastFourGoodJets() const {
	if (cleanedJets_.size() > 3)
		return cleanedJets_.at(3).userInt("passesPt");

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

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastTwoGoodTightBJets() const {
	return cleanedTightBJetIndex_.size() > 1;
}

// ------------ method called once each job just before starting event loop  ------------
void TopPairMuonPlusJetsSelectionFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TopPairMuonPlusJetsSelectionFilter::endJob() {
}

void TopPairMuonPlusJetsSelectionFilter::beginRun() {
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairMuonPlusJetsSelectionFilter);
