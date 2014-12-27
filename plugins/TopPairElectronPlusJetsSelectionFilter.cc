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

		// Selection criteria
		minSignalElectronPt_(iConfig.getParameter<double>("minSignalElectronPt")), //
		maxSignalElectronEta_(iConfig.getParameter<double>("maxSignalElectronEta")), //
		signalElectronIDCriteria_(iConfig.getParameter<std::string>("signalElectronIDCriteria")), //
		minSignalElectronID_(iConfig.getParameter<double>("minSignalElectronID")), //
		minLooseMuonPt_(iConfig.getParameter<double>("minLooseMuonPt")), //
		maxLooseMuonEta_(iConfig.getParameter<double>("maxLooseMuonEta")), //
		minLooseElectronPt_(iConfig.getParameter<double>("minLooseElectronPt")), //
		maxLooseElectronEta_(iConfig.getParameter<double>("maxLooseElectronEta")), //
		looseElectronIDCriteria_(iConfig.getParameter<std::string>("looseElectronIDCriteria")), //
		minLooseElectronID_(iConfig.getParameter<double>("minLooseElectronID")), //

		min1JetPt_(iConfig.getParameter<double>("min1JetPt")), //
		min2JetPt_(iConfig.getParameter<double>("min2JetPt")), //
		min3JetPt_(iConfig.getParameter<double>("min3JetPt")), //
		min4JetPt_(iConfig.getParameter<double>("min4JetPt")), //

		cleaningDeltaR_(iConfig.getParameter<double>("cleaningDeltaR")), //

		bJetDiscriminator_(iConfig.getParameter<std::string>("bJetDiscriminator")), //
		minBJetDiscriminator_(iConfig.getParameter<double>("minBJetDiscriminator")), //

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

	desc.add<double>("minSignalElectronPt",0.);
	desc.add<double>("maxSignalElectronEta",10.);
	desc.add<std::string>("signalElectronIDCriteria","idCriteria");
	desc.add<double>("minSignalElectronID",0);
	desc.add<double>("minLooseMuonPt",0.);
	desc.add<double>("maxLooseMuonEta",10.);
	desc.add<double>("minLooseElectronPt",0.);
	desc.add<double>("maxLooseElectronEta",10.);
	desc.add<std::string>("looseElectronIDCriteria","idCriteria");
	desc.add<double>("minLooseElectronID",0);

	desc.add<double>("min1JetPt", 30.0);
	desc.add<double>("min2JetPt", 30.0);
	desc.add<double>("min3JetPt", 30.0);
	desc.add<double>("min4JetPt", 30.0);

	desc.add<double>("cleaningDeltaR", 0.3 );
	desc.add < std::string > ("bJetDiscriminator", "combinedSecondaryVertexBJetTags");
	desc.add<double>("minBJetDiscriminator", 0.679 );
	
	desc.add<bool>("tagAndProbeStudies", false);
	desc.add<bool>("dropTriggerSelection", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairElectronPlusJetsSelection.");
	desc.addUntracked<bool>("debug", false);
	desc.add<bool>("taggingMode", false);
	desc.add<bool>("bSelectionInTaggingMode", false);
	desc.add<bool>("jetSelectionInTaggingMode", false);
	descriptions.add("applyTopPairElectronPlusJetsSelection", desc);
}

TopPairElectronPlusJetsSelectionFilter::~TopPairElectronPlusJetsSelectionFilter() {

}

bool TopPairElectronPlusJetsSelectionFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	// Get content from event
	// Including selecting a signal electron, loose leptons, jets and bjets
	setupEventContent(iEvent);
	
	// Store number of cleaned jets in events
	unsigned int numberOfJets(cleanedJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfJets)), prefix_ + "NumberOfJets");

	// Store indices of cleaned jets in event
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedJetIndex_)), prefix_ + "cleanedJetIndex");
	
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	iEvent.put(std::auto_ptr<std::vector<unsigned int> >(new std::vector<unsigned int>(cleanedBJetIndex_)), prefix_ + "cleanedBJetIndex");

	// std::auto_ptr < pat::JetCollection > jetoutput(new pat::JetCollection());

	bool passesSelection(true);
	bool passesSelectionExceptJetRequirements(true);
	bool passesSelectionExceptBtagging(true);

	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
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

		// if doesn't pass selection and not in tagging mode, stop here to save CPU time
		if ( !(taggingMode_ || passesSelection) )
			break;
	}
	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");

	// for (unsigned int index = 0; index < cleanedJets_.size(); ++index)
		// jetoutput->push_back(cleanedJets_.at(index));
	// iEvent.put(jetoutput, prefix_ + "cleanedJets");

	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(signalElectronIndex_)),prefix_ + "signalElectronIndex");

	if ( bSelectionInTaggingMode_ )
		return taggingMode_ || passesSelectionExceptBtagging;
	else if ( jetSelectionInTaggingMode_ )
		return taggingMode_ || passesSelectionExceptJetRequirements;
	else
		return taggingMode_ || passesSelection;

}

void TopPairElectronPlusJetsSelectionFilter::setupEventContent(edm::Event& iEvent) {
	if (debug_)
		cout << "Setting up the event content" << endl;

	// Event info
	runNumber_ = iEvent.run();
	isRealData_ = iEvent.isRealData();

	// Trigger info
	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByLabel(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	// Jets
	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(jetInput_, jets);
	jets_ = *jets;

	// Electrons
	edm::Handle < pat::ElectronCollection > electrons;
	iEvent.getByLabel(electronInput_, electrons);
	electrons_ = *electrons;

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
	for (unsigned index = 0; index < electrons_.size(); ++index) {
		const pat::Electron electron = electrons_.at(index);
		if (isLooseElectron(electron))
			looseElectrons_.push_back(electron);
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isLooseElectron(const pat::Electron& electron) const {
	bool passesPtAndEta = electron.pt() > minLooseElectronPt_ && fabs(electron.eta()) < maxLooseElectronEta_;
	//		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	// bool passesID = electron.electronID("mvaTrigV0") > 0.5;
	// bool passesIso = getRelativeIsolation(electron, 0.3, rho_, isRealData_, useDeltaBetaCorrectionsForElectrons_,
	// 		useRhoActiveAreaCorrections_) < looseElectronIso_;
	bool passesID = electron.electronID(looseElectronIDCriteria_) > minLooseElectronID_;
	bool passesIso = true;
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
	bool passesIso = true;

	return passesPtAndEta && passesID && passesIso;
}

void TopPairElectronPlusJetsSelectionFilter::goodIsolatedElectrons() {
	goodIsolatedElectrons_.clear();

	// Loop over electrons and select those that satisfy full selection
	for (unsigned index = 0; index < electrons_.size(); ++index) {
		const pat::Electron electron = electrons_.at(index);

		// bool passesIso = getRelativeIsolation(electron, 0.3, rho_, isRealData_, useDeltaBetaCorrectionsForElectrons_,
				// useRhoActiveAreaCorrections_) < tightElectronIso_;
		bool passesIso = true;
		if (isGoodElectron(electron) && passesIso) {
			goodIsolatedElectrons_.push_back(electron);
			//Check if this is the first, and therefore the signal, electron
			if ( goodIsolatedElectrons_.size()==1 ) signalElectronIndex_ = index;
		}
	}
}

bool TopPairElectronPlusJetsSelectionFilter::isGoodElectron(const pat::Electron& electron) const {
	bool passesPtAndEta = electron.pt() > minSignalElectronPt_ && fabs(electron.eta()) < maxSignalElectronEta_;
	bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	//2D impact w.r.t primary vertex
	// bool passesD0 = fabs(electron.dB(pat::Electron::PV2D)) < 0.02; //cm
	// bool passesID = electron.electronID("mvaTrigV0") > 0.5;
	bool passesID = electron.electronID(signalElectronIDCriteria_) > minSignalElectronID_;
	bool passesD0 = true;
	return passesPtAndEta && notInCrack && passesD0 && passesID;
}

void TopPairElectronPlusJetsSelectionFilter::cleanedJets() {
	cleanedJets_.clear();
	cleanedJetIndex_.clear();

	// Loop over jets
	for (unsigned index = 0; index < jets_.size(); ++index) {
		const pat::Jet jet = jets_.at(index);

		// Check jet passes selection criteria
		if (!isGoodJet(jet))
			continue;

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
			cleanedJetIndex_.push_back(index);
		}
	}
}

void TopPairElectronPlusJetsSelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	cleanedBJetIndex_.clear();

	// Loop over cleaned jets
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);
		
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
	double smearFactor = getSmearedJetPtScale(jet, 0);
	bool passesPtAndEta(smearFactor*jet.pt() > 20. && fabs(jet.eta()) < 2.5);
	bool passesJetID(false);
	bool passNOD = jet.numberOfDaughters() > 1;
	bool passNHF = jet.neutralHadronEnergyFraction() < 0.99;
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
	else
		return goodIsolatedElectrons_.size() == 1;
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
			for (unsigned int index = 0; index < electrons_.size(); ++index) {
				const pat::Electron probeElectron_ = electrons_.at(index);
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
	return signalElectron_.passConversionVeto();
				// Not sure if this is accessible from miniAOD, plus more or less applied in passConversionVeto
				// && signalElectron_.gsfTrack()->numberOfLostTrackerHits(HitPattern::MISSING_INNER_HITS) < 1; // left in the trackerExpectedHitsInner <1, although it is not there in the AnalysisTools, because it seems to make no difference
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastOneGoodJet() const {
	if (cleanedJets_.size() > 0)
		return getSmearedJetPtScale(cleanedJets_.at(0), 0)*cleanedJets_.at(0).pt() > min1JetPt_;

	return false;

}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastTwoGoodJets() const {
	if (cleanedJets_.size() > 1)
		return getSmearedJetPtScale(cleanedJets_.at(1), 0)*cleanedJets_.at(1).pt() > min2JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastThreeGoodJets() const {
	if (cleanedJets_.size() > 2)
		return getSmearedJetPtScale(cleanedJets_.at(2), 0)*cleanedJets_.at(2).pt() > min3JetPt_;

	return false;
}

bool TopPairElectronPlusJetsSelectionFilter::hasAtLeastFourGoodJets() const {
	if (cleanedJets_.size() > 3)
		return getSmearedJetPtScale(cleanedJets_.at(3), 0)*cleanedJets_.at(3).pt() > min4JetPt_;

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
