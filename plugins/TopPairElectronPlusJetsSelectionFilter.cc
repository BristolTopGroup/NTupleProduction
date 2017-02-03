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
				cleanedJetsToken_(
						consumes < pat::JetCollection > (iConfig.getParameter < edm::InputTag > ("cleanedJets"))), //
				cleanedBJetsToken_(
						consumes < pat::JetCollection > (iConfig.getParameter < edm::InputTag > ("cleanedBJets"))), //
				vetoElectronsToken_(
						consumes < std::vector<pat::Electron>
								> (iConfig.getParameter < edm::InputTag > ("vetoElectrons"))), //
				goodElectronsToken_(
						consumes < std::vector<pat::Electron>
								> (iConfig.getParameter < edm::InputTag > ("goodElectrons"))),
				electronsToken_(
						consumes < std::vector<pat::Electron> > (iConfig.getParameter < edm::InputTag > ("electrons"))),
				vetoMuonsToken_(
						consumes < pat::MuonCollection > (iConfig.getParameter < edm::InputTag > ("vetoMuons"))), //
				hltInputTag_(consumes < edm::TriggerResults > (iConfig.getParameter < edm::InputTag > ("HLTInput"))), //
				tagAndProbeStudies_(iConfig.getParameter<bool>("tagAndProbeStudies")), //
				dropTriggerSelection_(iConfig.getParameter<bool>("dropTriggerSelection")), //
				prefix_(iConfig.getUntrackedParameter < std::string > ("prefix")), //
				MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
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
				cleanedTightBJetIndex_(),
				cleanedJets_(), //
				cleanedBJets_(), //
				electrons_(), //
				goodIsolatedElectrons_(), //
				vetoElectrons_(), //
				vetoMuons_(), //
				signalElectron_(), //
				hltConfig_(), //
				triggerResults_() {
	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		passes_.at(step) = 0;
		produces<bool>(prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	produces<bool>(prefix_ + "FullSelection");
	produces<bool>(prefix_ + "FullSelectionNoB");
	produces<unsigned int>(prefix_ + "NumberOfJets");
	produces<unsigned int>(prefix_ + "NumberOfBtags");
}

void TopPairElectronPlusJetsSelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("cleanedJets");
	desc.add < InputTag > ("cleanedBJets");
	desc.add < InputTag > ("vetoElectrons");
	desc.add < InputTag > ("goodElectrons");
	desc.add < InputTag > ("electrons");
	desc.add < InputTag > ("vetoMuons");
	desc.add < InputTag > ("HLTInput");

	desc.add<double>("cleaningDeltaR", 0.3);

	desc.add<double>("minBJetDiscriminator", 0.800);
	desc.add<double>("tightBJetDiscriminator", 0.935);

	desc.add<bool>("tagAndProbeStudies", false);
	desc.add<bool>("dropTriggerSelection", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairElectronPlusJetsSelection.");
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
//	bool passesSelectionWithTightBtagging(false);

	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		TTbarEPlusJetsReferenceSelection::Step stepName = TTbarEPlusJetsReferenceSelection::Step(step);
		LogDebug("NTP_EPlusJets") << "Doing selection step: " << TTbarEPlusJetsReferenceSelection::StringSteps[step];

		bool passesStep(passesSelectionStep(iEvent, step));

		// Require exactly zero b jets for QCD control region
		// Or exactly one b jet, as e.g. angle(b,l) only makes sense if there is at least one b jet
		if (nonIsolatedElectronSelection_ || invertedConversionSelection_) {
			if (stepName == TTbarEPlusJetsReferenceSelection::AtLeastOneBtag
					|| stepName == TTbarEPlusJetsReferenceSelection::AtLeastTwoBtags) {
				passesStep = hasExactlyZeroGoodBJet() || hasExactlyOneGoodBJet();
			}
		}

		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;

		if (step < TTbarEPlusJetsReferenceSelection::AtLeastOneGoodJet)
			passesSelectionExceptJetRequirements = passesSelectionExceptJetRequirements && passesStep;

		if (step < TTbarEPlusJetsReferenceSelection::AtLeastOneBtag)
			passesSelectionExceptBtagging = passesSelectionExceptBtagging && passesStep;

		// if doesn't pass selection and not in tagging mode, stop here to save CPU time
		if (!(taggingMode_ || passesSelection))
			break;
	}

	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelectionExceptBtagging)), prefix_ + "FullSelectionNoB");

	// Store number of cleaned jets in events
	unsigned int numberOfJets(cleanedJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfJets)), prefix_ + "NumberOfJets");

	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");

	if (bSelectionInTaggingMode_)
		return taggingMode_ || passesSelectionExceptBtagging;
	else if (jetSelectionInTaggingMode_)
		return taggingMode_ || passesSelectionExceptJetRequirements;
	else
		return taggingMode_ || passesSelection;
}

void TopPairElectronPlusJetsSelectionFilter::setupEventContent(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	LogDebug("NTP_EPlusJets") << "Setting up the event content";

	// Event info
	runNumber_ = iEvent.run();
	isRealData_ = iEvent.isRealData();

	// Trigger info
	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByToken(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	// cleaned Jets
	LogDebug("NTP_EPlusJets") << "Getting clean jets";
	edm::Handle < pat::JetCollection > cleanedJets;
	iEvent.getByToken(cleanedJetsToken_, cleanedJets);
	cleanedJets_ = *cleanedJets;

	// cleaned BJets
	LogDebug("NTP_EPlusJets") << "Getting clean B jets";
	edm::Handle < pat::JetCollection > cleanedBJets;
	iEvent.getByToken(cleanedBJetsToken_, cleanedBJets);
	cleanedBJets_ = *cleanedBJets;

	// good Electrons
	LogDebug("NTP_EPlusJets") << "Getting good isolated electrons";
	edm::Handle < std::vector<pat::Electron> > goodElectrons;
	iEvent.getByToken(goodElectronsToken_, goodElectrons);
	goodIsolatedElectrons_ = *goodElectrons;

	// Electrons (for veto)
	LogDebug("NTP_EPlusJets") << "Getting veto electrons";
	edm::Handle < std::vector<pat::Electron> > vetoElectrons;
	iEvent.getByToken(vetoElectronsToken_, vetoElectrons);
	vetoElectrons_ = *vetoElectrons;

	// all Electrons (needed for tag & probe)
	LogDebug("NTP_EPlusJets") << "Getting all electrons";
	edm::Handle < std::vector<pat::Electron> > electrons;
	iEvent.getByToken(vetoElectronsToken_, electrons);
	electrons_ = *electrons;

	// Muons (for veto)
	LogDebug("NTP_EPlusJets") << "Getting loose muons";
	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByToken(vetoMuonsToken_, muons);
	vetoMuons_ = *muons;

	// Get the highest pt, signal electron
	LogDebug("NTP_EPlusJets") << "Getting signal electron";
	hasSignalElectron_ = goodIsolatedElectrons_.size() > 0;
	if (hasSignalElectron_)
		signalElectron_ = goodIsolatedElectrons_.front();
}

bool TopPairElectronPlusJetsSelectionFilter::passesSelectionStep(edm::Event& iEvent, unsigned int selectionStep) const {
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
	// Require no muons in the event
	return vetoMuons_.size() == 0;
}

bool TopPairElectronPlusJetsSelectionFilter::passesLooseElectronVeto() const {
	double invariantMass = 0;
	bool isZEvent = false;

	if (tagAndProbeStudies_) {
		if ((vetoElectrons_.size() >= 1) && hasSignalElectron_) {
			for (unsigned int index = 0; index < electrons_.size(); ++index) {
				const pat::Electron probeElectron = electrons_.at(index);
				// skip the tag electron itself
				if (probeElectron.p4() == signalElectron_.p4())
					continue;
				invariantMass = (signalElectron_.p4() + probeElectron.p4()).mass();
				bool passesLowerLimit = invariantMass > 60;
				bool passesUpperLimit = invariantMass < 120;
				if (passesLowerLimit && passesUpperLimit)
					isZEvent = true;
			}
		}
		return isZEvent == true;
	} 
	else {
		if (nonIsolatedElectronSelection_ || invertedConversionSelection_){
			return vetoElectrons_.size() < 1;
		}
		return vetoElectrons_.size() < 2;
	}
}

bool TopPairElectronPlusJetsSelectionFilter::passesConversionVeto() const {
	if (!hasExactlyOneSignalElectron())
		return false;

	bool passVeto = signalElectron_.passConversionVeto();

	if (invertedConversionSelection_)
		return !passVeto;
	else
		return passVeto;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastOneGoodJet() const {
	return cleanedJets_.size() > 0;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastTwoGoodJets() const {
	return cleanedJets_.size() > 1;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastThreeGoodJets() const {
	return cleanedJets_.size() > 2;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastFourGoodJets() const {
	return cleanedJets_.size() > 3;
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

void TopPairElectronPlusJetsSelectionFilter::beginRun() {
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairElectronPlusJetsSelectionFilter);
