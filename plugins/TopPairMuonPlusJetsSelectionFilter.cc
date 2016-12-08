#include "BristolAnalysis/NTupleTools/plugins/TopPairMuonPlusJetsSelectionFilter.h"
// system include files
#include <memory>
#include <iostream>
// user include files
#include "FWCore/Framework/interface/MakerMacros.h"

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;

TopPairMuonPlusJetsSelectionFilter::TopPairMuonPlusJetsSelectionFilter(const edm::ParameterSet& iConfig) :
				// Input tags
				cleanedJetsToken_(
						consumes < pat::JetCollection > (iConfig.getParameter < edm::InputTag > ("cleanedJets"))), //
				cleanedBJetsToken_(
						consumes < pat::JetCollection > (iConfig.getParameter < edm::InputTag > ("cleanedBJets"))), //
				vetoElectronsToken_(
						consumes < std::vector
								< pat::Electron >> (iConfig.getParameter < edm::InputTag > ("vetoElectrons"))), //
				vetoMuonsToken_(
						consumes < pat::MuonCollection > (iConfig.getParameter < edm::InputTag > ("vetoMuons"))), //
				goodMuonsToken_(
						consumes < pat::MuonCollection > (iConfig.getParameter < edm::InputTag > ("goodMuons"))), //
				muonsToken_(consumes < pat::MuonCollection > (iConfig.getParameter < edm::InputTag > ("muons"))), //
				hltInputTag_(consumes < edm::TriggerResults > (iConfig.getParameter < edm::InputTag > ("HLTInput"))), //

				// Flags and labels
				tagAndProbeStudies_(iConfig.getParameter<bool>("tagAndProbeStudies")), //
				dropTriggerSelection_(iConfig.getParameter<bool>("dropTriggerSelection")), //
				prefix_(iConfig.getUntrackedParameter < std::string > ("prefix")), //
				MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
				taggingMode_(iConfig.getParameter<bool>("taggingMode")), //
				bSelectionInTaggingMode_(iConfig.getParameter<bool>("bSelectionInTaggingMode")), //

				nonIsolatedMuonSelection1_(iConfig.getParameter<bool>("nonIsolatedMuonSelection1")), //
				nonIsolatedMuonSelection2_(iConfig.getParameter<bool>("nonIsolatedMuonSelection2")), //
				passes_(), //
				runNumber_(0), //
				signalMuonIndex_(999), //
				isRealData_(false), //
				hasSignalMuon_(false), //
				cleanedJets_(), //
				cleanedBJets_(), //
				vetoElectrons_(), //
				muons_(), //
				goodIsolatedMuons_(), //
				vetoMuons_(), //
				signalMuon_(), //
				hltConfig_(), //
				triggerResults_() {
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		passes_.at(step) = 0;
		produces<bool>(prefix_ + TTbarMuPlusJetsReferenceSelection::StringSteps[step]);
	}
	produces<bool>(prefix_ + "FullSelection");
	produces<bool>(prefix_ + "FullSelectionNoB");
	produces<unsigned int>(prefix_ + "NumberOfBtags");
	produces<unsigned int>(prefix_ + "NumberOfJets");
}

void TopPairMuonPlusJetsSelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("cleanedJets");
	desc.add < InputTag > ("cleanedBJets");
	desc.add < InputTag > ("vetoElectrons");
	desc.add < InputTag > ("muons");
	desc.add < InputTag > ("vetoMuons");
	desc.add < InputTag > ("goodMuons");
	desc.add < InputTag > ("HLTInput");

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
//	bool passesSelectionWithTightBtagging(true);

	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		TTbarMuPlusJetsReferenceSelection::Step stepName = TTbarMuPlusJetsReferenceSelection::Step(step);
		LogDebug("NTP_MuPlusJets") << "Doing selection step: "
				<< TTbarMuPlusJetsReferenceSelection::StringSteps[step];
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


	// Store info in event
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarMuPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelectionExceptBtagging)), prefix_ + "FullSelectionNoB");

	// Store number of cleaned jets in event
	unsigned int numberOfJets(cleanedJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfJets)), prefix_ + "NumberOfJets");

	// Store number of b tags in event
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");

	if (!bSelectionInTaggingMode_)
		return taggingMode_ || passesSelection;
	else
		return taggingMode_ || passesSelectionExceptBtagging;
}

void TopPairMuonPlusJetsSelectionFilter::setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	LogDebug("NTP_MuPlusJets") << "Setting up the event content";

	// Event info
	runNumber_ = iEvent.run();
	isRealData_ = iEvent.isRealData();

	// Trigger results
	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByToken(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	// Electrons (for veto)
	LogDebug("NTP_MuPlusJets") << "Getting veto electrons";
	edm::Handle < std::vector<pat::Electron> > electrons;
	iEvent.getByToken(vetoElectronsToken_, electrons);
	vetoElectrons_ = *electrons;

	// veto muons
	LogDebug("NTP_MuPlusJets") << "Getting loose muons";
	edm::Handle < pat::MuonCollection > vetoMuons;
	iEvent.getByToken(vetoMuonsToken_, vetoMuons);
	vetoMuons_ = *vetoMuons;
	// Muons
	LogDebug("NTP_MuPlusJets") << "Getting isolated muons";
	edm::Handle < pat::MuonCollection > goodMuons;
	iEvent.getByToken(goodMuonsToken_, goodMuons);
	goodIsolatedMuons_ = *goodMuons;

	// for tag and probe
	LogDebug("NTP_MuPlusJets") << "Getting all muons";
	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByToken(muonsToken_, muons);
	muons_ = *muons;

	LogDebug("NTP_MuPlusJets") << "Getting signal muon";
	hasSignalMuon_ = goodIsolatedMuons_.size() > 0;
	if (hasSignalMuon_)
		signalMuon_ = goodIsolatedMuons_.front();

	// Jet collection
	LogDebug("NTP_MuPlusJets") << "Getting clean jets";
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByToken(cleanedJetsToken_, jets);
	cleanedJets_ = *jets;

	// Get b jets from cleaned jets
	LogDebug("NTP_MuPlusJets") << "Getting clean B jets";
	edm::Handle < pat::JetCollection > bjets;
	iEvent.getByToken(cleanedBJetsToken_, bjets);
	cleanedBJets_ = *bjets;
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
	return vetoElectrons_.size() == 0;
}

bool TopPairMuonPlusJetsSelectionFilter::passesLooseMuonVeto() const {
	double invariantMass = 0;
	bool isZEvent = false;

	if (tagAndProbeStudies_) {
		if ((vetoMuons_.size() >= 1) && hasSignalMuon_) {
			for (unsigned int index = 0; index < muons_.size(); ++index) {
				const pat::Muon probeMuon = muons_.at(index);
				// skip the tag muon itself
				if (probeMuon.p4() == signalMuon_.p4())
					continue;
				invariantMass = (signalMuon_.p4() + probeMuon.p4()).mass();
				bool passesLowerLimit = invariantMass > 60;
				bool passesUpperLimit = invariantMass < 120;
				if (passesLowerLimit && passesUpperLimit)
					isZEvent = true;
			}
		}
		return isZEvent == true;
	} else
		// Require only one loose muon, which is the signal muons
		return vetoMuons_.size() < 2;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastOneGoodJet() const {
	return cleanedJets_.size() > 0;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastTwoGoodJets() const {
	return cleanedJets_.size() > 1;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastThreeGoodJets() const {
	return cleanedJets_.size() > 2;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastFourGoodJets() const {
	return cleanedJets_.size() > 3;
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

void TopPairMuonPlusJetsSelectionFilter::beginRun() {
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairMuonPlusJetsSelectionFilter);
