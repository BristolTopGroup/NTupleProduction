#include "BristolAnalysis/NTupleTools/plugins/TopPairElectronPlusJets2012SelectionFilter.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"
// system include files
#include <memory>
#include <iostream>
// user include files
#include "DataFormats/RecoCandidate/interface/IsoDepositDirection.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
#include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
#include "DataFormats/PatCandidates/interface/Isolation.h"
#include "EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"

using namespace edm;
using namespace std;
using namespace reco;
using namespace isodeposit;
using namespace pat;

TopPairElectronPlusJets2012SelectionFilter::TopPairElectronPlusJets2012SelectionFilter(const edm::ParameterSet& iConfig) :
		jetInput_(iConfig.getParameter < edm::InputTag > ("jetInput")), //
		electronInput_(iConfig.getParameter < edm::InputTag > ("electronInput")), //
		muonInput_(iConfig.getParameter < edm::InputTag > ("muonInput")), //
		hltInputTag_(iConfig.getParameter < edm::InputTag > ("HLTInput")), //
		VertexInput_(iConfig.getParameter < edm::InputTag > ("VertexInput")), //
		trkInput_(iConfig.getParameter < edm::InputTag > ("trkInput")), //
		hcalNoiseInput_(iConfig.getParameter < edm::InputTag > ("HcalNoiseInput")), //
		hcalLaserFilterInput_(iConfig.getParameter < edm::InputTag > ("HCALLaserFilterInput")), //
		ecalDeadCellFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALDeadCellFilterInput")), //
		trackingFailureFilter_(iConfig.getParameter < edm::InputTag > ("TrackingFailureFilterInput")), //
		eeBadScFilter_(iConfig.getParameter < edm::InputTag > ("BadEESupercrystalFilterInput")), //
		min1JetPt_(iConfig.getParameter<double>("min1JetPt")), //
		min2JetPt_(iConfig.getParameter<double>("min2JetPt")), //
		min3JetPt_(iConfig.getParameter<double>("min3JetPt")), //
		min4JetPt_(iConfig.getParameter<double>("min4JetPt")), //
		tightElectronIso_(iConfig.getParameter<double>("tightElectronIsolation")), //
		looseElectronIso_(iConfig.getParameter<double>("looseElectronIsolation")), //
		looseMuonIso_(iConfig.getParameter<double>("looseMuonIsolation")), //
		useDeltaBetaCorrectionsForMuons_(iConfig.getParameter<bool>("useDeltaBetaCorrectionsForMuons")), //
		useDeltaBetaCorrectionsForElectrons_(iConfig.getParameter<bool>("useDeltaBetaCorrectionsForElectrons")), //
		useRhoActiveAreaCorrections_(iConfig.getParameter<bool>("useRhoActiveAreaCorrections")), //
		useMETFilters_(iConfig.getParameter<bool>("useMETFilters")), //
		useEEBadScFilter_(iConfig.getParameter<bool>("useEEBadScFilter")), //
		prefix_(iConfig.getUntrackedParameter < std::string > ("prefix")), //
		MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
		debug_(iConfig.getUntrackedParameter<bool>("debug")), //
		taggingMode_(iConfig.getParameter<bool>("taggingMode")), //
		passes_(), //
		runNumber_(0), //
		isRealData_(false), //
		hasSignalElectron_(false), //
		rho_(0), //
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
	produces<unsigned int>(prefix_ + "NumberOfBtags");
	produces < pat::JetCollection > (prefix_ + "cleanedJets");
	produces < pat::ElectronCollection > (prefix_ + "signalElectron");
}

void TopPairElectronPlusJets2012SelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
	edm::ParameterSetDescription desc;
	desc.add < InputTag > ("jetInput");
	desc.add < InputTag > ("electronInput");
	desc.add < InputTag > ("muonInput");
	desc.add < InputTag > ("HLTInput");
	desc.add < InputTag > ("VertexInput");
	desc.add < InputTag > ("trkInput");
	desc.add < InputTag > ("HcalNoiseInput");
	desc.add < InputTag > ("HCALLaserFilterInput");
	desc.add < InputTag > ("ECALDeadCellFilterInput");
	desc.add < InputTag > ("TrackingFailureFilterInput");
	desc.add < InputTag > ("BadEESupercrystalFilterInput");
	desc.add<double>("min1JetPt", 30.0);
	desc.add<double>("min2JetPt", 30.0);
	desc.add<double>("min3JetPt", 30.0);
	desc.add<double>("min4JetPt", 30.0);
	desc.add<double>("tightElectronIsolation", 0.1);
	desc.add<double>("looseElectronIsolation", 0.15);
	desc.add<double>("looseMuonIsolation", 0.2);

	desc.add<bool>("useDeltaBetaCorrectionsForMuons", true);
	desc.add<bool>("useDeltaBetaCorrectionsForElectrons", false);
	desc.add<bool>("useRhoActiveAreaCorrections", true);
	desc.add<bool>("useMETFilters", false);
	desc.add<bool>("useEEBadScFilter", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairElectronPlusJets2012Selection.");
	desc.addUntracked<bool>("debug", false);
	desc.add<bool>("taggingMode", false);
	descriptions.add("applyTopPairElectronPlusJets2012Selection", desc);
}

TopPairElectronPlusJets2012SelectionFilter::~TopPairElectronPlusJets2012SelectionFilter() {

}

bool TopPairElectronPlusJets2012SelectionFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	setupEventContent(iEvent);
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	std::auto_ptr < pat::JetCollection > jetoutput(new pat::JetCollection());

	bool passesSelection(true);

	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		if (debug_)
			cout << "Doing selection step: " << TTbarEPlusJetsReferenceSelection::StringSteps[step] << endl;
		bool passesStep(passesSelectionStep(iEvent, step));
		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;
		//if not in tagginmode and selection step doesn't pass leave loop.
		if (!(taggingMode_ || passesSelection))
			break;
	}
	for (unsigned int step = 0; step < TTbarEPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarEPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");

	for (unsigned int index = 0; index < cleanedJets_.size(); ++index)
		jetoutput->push_back(cleanedJets_.at(index));
	iEvent.put(jetoutput, prefix_ + "cleanedJets");

	std::auto_ptr < pat::ElectronCollection > signalElectron(new pat::ElectronCollection());
	signalElectron->push_back(signalElectron_);
	iEvent.put(signalElectron, prefix_ + "signalElectron");

	return taggingMode_ || passesSelection;
}

void TopPairElectronPlusJets2012SelectionFilter::setupEventContent(edm::Event& iEvent) {
	if (debug_)
		cout << "Setting up the event content" << endl;
	runNumber_ = iEvent.run();
	isRealData_ = iEvent.isRealData();
	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByLabel(hltInputTag_, triggerResults);
	triggerResults_ = *triggerResults;

	edm::Handle<double> rhoH;
	iEvent.getByLabel(edm::InputTag("kt6PFJets", "rho"), rhoH);
	rho_ = *rhoH.product();

	edm::Handle < pat::JetCollection > jets;
	iEvent.getByLabel(jetInput_, jets);
	jets_ = *jets;

	edm::Handle < pat::ElectronCollection > electrons;
	iEvent.getByLabel(electronInput_, electrons);
	electrons_ = *electrons;

	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByLabel(muonInput_, muons);
	muons_ = *muons;
	if (debug_)
		cout << "Getting loose electrons" << endl;
	getLooseElectrons();
	if (debug_)
		cout << "Getting loose muons" << endl;
	getLooseMuons();
	//this is the correct order: goodIsolatedElectrons, signalElectron, cleanedJets, cleanedBJets
	if (debug_)
		cout << "Getting isolated electrons" << endl;
	goodIsolatedElectrons();
	if (debug_)
		cout << "Getting signal electron" << endl;
	hasSignalElectron_ = goodIsolatedElectrons_.size() > 0;
	if (hasSignalElectron_)
		signalElectron_ = goodIsolatedElectrons_.front();
	if (debug_)
		cout << "Getting clean jets" << endl;
	cleanedJets();
	if (debug_)
		cout << "Getting clean B jets" << endl;
	cleanedBJets();
}

void TopPairElectronPlusJets2012SelectionFilter::getLooseElectrons() {
	looseElectrons_.clear();

	for (unsigned index = 0; index < electrons_.size(); ++index) {
		const pat::Electron electron = electrons_.at(index);
		if (isLooseElectron(electron))
			looseElectrons_.push_back(electron);
	}
}

bool TopPairElectronPlusJets2012SelectionFilter::isLooseElectron(const pat::Electron& electron) const {
	bool passesPtAndEta = electron.pt() > 20 && fabs(electron.eta()) < 2.5;
	//		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	bool passesID = electron.electronID("mvaTrigV0") > 0.5;
	bool passesIso = getRelativeIsolation(electron, 0.3, rho_, isRealData_, useDeltaBetaCorrectionsForElectrons_,
			useRhoActiveAreaCorrections_) < looseElectronIso_;
	return passesPtAndEta && passesID && passesIso;
}

void TopPairElectronPlusJets2012SelectionFilter::getLooseMuons() {
	looseMuons_.clear();

	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);
		if (isLooseMuon(muon))
			looseMuons_.push_back(muon);
	}
}

bool TopPairElectronPlusJets2012SelectionFilter::isLooseMuon(const pat::Muon& muon) const {
	bool passesPtAndEta = muon.pt() > 10 && fabs(muon.eta()) < 2.5;
//	cout << "muon.pt() = " << muon.pt() << endl;
//	cout << "fabs(muon.eta()) = " << fabs(muon.eta()) << endl;
	bool passesID = muon.isPFMuon() && (muon.isGlobalMuon() || muon.isTrackerMuon()); // put TrackerMuon requirement back in, as per 2012 twiki...correct?
//	cout << "muon.isPFMuon() = " << muon.isPFMuon() << endl;
//	cout << "muon.isGlobalMuon() = " << muon.isGlobalMuon() << endl;
//	cout << "muon.isTrackerMuon() = " << muon.isTrackerMuon() << endl;
	bool passesIso = getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) < looseMuonIso_;
//	cout << "getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) = " << getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) << endl;
	return passesPtAndEta && passesID && passesIso;
}

void TopPairElectronPlusJets2012SelectionFilter::goodIsolatedElectrons() {
	goodIsolatedElectrons_.clear();
	for (unsigned index = 0; index < electrons_.size(); ++index) {
		const pat::Electron electron = electrons_.at(index);
		if (debug_) {
			cout << "Electron:" << endl;
			cout << "pT: " << electron.pt() << " eta: " << electron.eta() << " phi: " << electron.phi() << endl;
		}

		bool passesIso = getRelativeIsolation(electron, 0.3, rho_, isRealData_, useDeltaBetaCorrectionsForElectrons_,
				useRhoActiveAreaCorrections_) < tightElectronIso_;
		if (isGoodElectron(electron) && passesIso)
			goodIsolatedElectrons_.push_back(electron);
	}
}

bool TopPairElectronPlusJets2012SelectionFilter::isGoodElectron(const pat::Electron& electron) const {
	bool passesPtAndEta = electron.pt() > 30. && fabs(electron.eta()) < 2.5;
	bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	//2D impact w.r.t primary vertex
	bool passesD0 = fabs(electron.dB(pat::Electron::PV2D)) < 0.02; //cm
	bool passesID = electron.electronID("mvaTrigV0") > 0.5;
//	cout << "Event " << ":" << runNumber_ << endl << "electron.pt() = " << electron.pt() << endl << "fabs(electron.eta()) = " << fabs(electron.eta()) << endl << "passesPtAndEta = " << passesPtAndEta << endl << "notInCrack = " << notInCrack << endl << "electron.dB(pat::Electron::PV2D) = " << electron.dB(pat::Electron::PV2D) << endl << "passesD0 = " << passesD0 << endl << "electron.electronID('mvaTrigV0') = " << electron.electronID("mvaTrigV0") << endl << "passesID = " << passesID << endl;
	return passesPtAndEta && notInCrack && passesD0 && passesID; // removed passeHoverE...not in twiki
}

void TopPairElectronPlusJets2012SelectionFilter::cleanedJets() {
	cleanedJets_.clear();
	for (unsigned index = 0; index < jets_.size(); ++index) {
		const pat::Jet jet = jets_.at(index);
		if (!isGoodJet(jet))
			continue;
		bool overlaps(false);
		if (hasSignalElectron_) {
			double dR = deltaR(signalElectron_, jet);
			overlaps = dR < 0.3;
		}
		if (!overlaps)
			cleanedJets_.push_back(jet);
	}
}

void TopPairElectronPlusJets2012SelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);
		if (jet.bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679)
			cleanedBJets_.push_back(jet);
	}
}

bool TopPairElectronPlusJets2012SelectionFilter::isGoodJet(const pat::Jet& jet) const {
	//both cuts are done at PAT config level (selectedPATJets) this is just for safety
	double smearFactor = getSmearedJetPtScale(jet, 0);
	bool passesPtAndEta(smearFactor*jet.pt() > 20. && fabs(jet.eta() < 2.5)); // 30GeV and 2.4 for 2011, but set to 20 and 2.5 so the selection is the same as for 2012 8TeV. Not sure if this is the correct thing to do.
	bool passesJetID(false);

	bool passNOD = jet.numberOfDaughters() > 1;
	//bool passNHF = (jet.neutralHadronEnergy() + jet.HFHadronEnergy()) / jet.energy() < 0.99;
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

bool TopPairElectronPlusJets2012SelectionFilter::passesSelectionStep(edm::Event& iEvent,
		unsigned int selectionStep) const {
	TTbarEPlusJetsReferenceSelection::Step step = TTbarEPlusJetsReferenceSelection::Step(selectionStep);
	switch (step) {
	case TTbarEPlusJetsReferenceSelection::AllEvents:
		return true;
	case TTbarEPlusJetsReferenceSelection::EventCleaningAndTrigger:
		if(passesEventCleaning(iEvent) && passesTriggerSelection()){
           cout << "trig+evt: " << iEvent.id().event() << endl;
           }
		return passesEventCleaning(iEvent) && passesTriggerSelection();
	case TTbarEPlusJetsReferenceSelection::OneIsolatedElectron:
		if(hasExactlyOneIsolatedLepton()){
           cout << "1electron: " <<  iEvent.id().event() << endl;
           }
		return hasExactlyOneIsolatedLepton();
	case TTbarEPlusJetsReferenceSelection::LooseMuonVeto:
        if(passesLooseLeptonVeto()){
         cout << "mu veto: " <<  iEvent.id().event() << endl;
         }
		return passesLooseLeptonVeto();
	case TTbarEPlusJetsReferenceSelection::DiLeptonVeto:
		if(passesDileptonVeto()){
           cout << "dilepton veto: "  << iEvent.id().event() << endl;
           }
		return passesDileptonVeto();
	case TTbarEPlusJetsReferenceSelection::ConversionVeto:
		if(passesConversionVeto()){
           cout << "conversion veto: "  << iEvent.id().event() << endl;
           }
		return passesConversionVeto();
	case TTbarEPlusJetsReferenceSelection::AtLeastOneGoodJet:
		return hasAtLeastOneGoodJet();
	case TTbarEPlusJetsReferenceSelection::AtLeastTwoGoodJets:
		return hasAtLeastTwoGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastThreeGoodJets:
		return hasAtLeastThreeGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastFourGoodJets:
		if(hasAtLeastFourGoodJets()){
           cout << "ge4j: " <<  iEvent.id().event() << endl;
           }
		return hasAtLeastFourGoodJets();
	case TTbarEPlusJetsReferenceSelection::AtLeastOneBtag:
		return hasAtLeastOneGoodBJet();
	case TTbarEPlusJetsReferenceSelection::AtLeastTwoBtags:
		if(hasAtLeastTwoGoodBJets()){
          cout << "ge2b: " <<  iEvent.id().event() << endl;
          }
		return hasAtLeastTwoGoodBJets();
	default:
		break;
	}

	return false;
}

bool TopPairElectronPlusJets2012SelectionFilter::passesEventCleaning(edm::Event& iEvent) const {
	// Scraping veto is filtered on at
	if (!passesScrapingVeto(iEvent))
		return false;

	// Good Primary Vertex Part - goodness done at PAT selection level
	bool passesPrimaryVertexRequirement(false);
	edm::Handle < reco::VertexCollection > primaryVertices;
	iEvent.getByLabel(VertexInput_, primaryVertices);
	if (primaryVertices.isValid()) {
		int nVertices = primaryVertices->size();
		edm::LogInfo("TopPairElectronPlusJets2012SelectionFilter") << "Total # Primary Vertices: " << nVertices;
		if (nVertices > 0)
			passesPrimaryVertexRequirement = true;
	} else
		edm::LogError("EventFilterError") << "Error! Can't get the product " << VertexInput_;
	if (!passesPrimaryVertexRequirement)
		return false;

	bool passesMETFilters(true);
	if (useMETFilters_) {
		passesMETFilters = passesMETFilters && passesFilter(iEvent, hcalNoiseInput_);
		passesMETFilters = passesMETFilters && passesFilter(iEvent, hcalLaserFilterInput_);
		passesMETFilters = passesMETFilters && passesFilter(iEvent, ecalDeadCellFilterInput_);
		passesMETFilters = passesMETFilters && passesFilter(iEvent, trackingFailureFilter_);
		if (useEEBadScFilter_)
			passesMETFilters = passesMETFilters && passesFilter(iEvent, eeBadScFilter_);

		//beam halo ID
		bool cscTightID(false);
		edm::Handle < reco::BeamHaloSummary > TheBeamHaloSummary;
		iEvent.getByLabel("BeamHaloSummary", TheBeamHaloSummary);
		if (TheBeamHaloSummary.isValid()) {
			edm::LogInfo("TopPairElectronPlusJets2012SelectionFilter") << "Successfully obtained BeamHaloSummary";
			const reco::BeamHaloSummary TheSummary = (*TheBeamHaloSummary.product());
			cscTightID = TheSummary.CSCTightHaloId();
		} else
			edm::LogError("TopPairElectronPlusJets2012SelectionFilter_Error")
					<< "Error! Can't get the product BeamHaloSummary";
		//passes MET filters and is not BeamHalo
		passesMETFilters = passesMETFilters && !cscTightID;
	}

	return passesMETFilters;
}

bool TopPairElectronPlusJets2012SelectionFilter::passesScrapingVeto(edm::Event& event) const {
	bool result(false);
	edm::Handle < reco::TrackCollection > tracks;
	event.getByLabel(trkInput_, tracks);
	double fraction = 1.;
	unsigned int numTracks(10);
	double hpTrackThreshold(0.25);

	if (tracks.isValid()) {
		edm::LogInfo("EventFilter") << "Total # Tracks: " << tracks->size();

		int numhighpurity = 0;

		reco::TrackBase::TrackQuality trackQuality = reco::TrackBase::qualityByName("highPurity");

		if (tracks->size() > numTracks) {
			for (reco::TrackCollection::const_iterator it = tracks->begin(); it != tracks->end(); ++it) {
				if (it->quality(trackQuality))
					numhighpurity++;
			}
			fraction = (double) numhighpurity / (double) tracks->size();
		}
	} else {
		edm::LogError("EventFilterError") << "Error! Can't get the product " << trkInput_;
	}
	if (fraction >= hpTrackThreshold)
		result = true;
	return result;
}

bool TopPairElectronPlusJets2012SelectionFilter::passesTriggerSelection() const {
	if (isRealData_) {
		//2011 data: run 160404 to run 180252
		if (runNumber_ >= 160404 && runNumber_ <= 163869)
			return triggerFired("HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30", hltConfig_, triggerResults_);
		else if (runNumber_ > 163869 && runNumber_ <= 165633)
			return triggerFired("HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30", hltConfig_, triggerResults_);
		else if (runNumber_ > 165633 && runNumber_ <= 178380)
			return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30", hltConfig_,
					triggerResults_);
		else if (runNumber_ > 178380 && runNumber_ <= 180252)
			return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFJet30", hltConfig_,
					triggerResults_);
		//2012 data: run 190456 to run 208686
		else if (runNumber_ >= 190456 && runNumber_ <= 208686)
            return triggerFired("HLT_Ele27_WP80_v", hltConfig_, triggerResults_);
		else
			return false;
	} else {
		if (MCSampleTag_ == "Fall11") { //Fall11 MC
			return triggerFired("HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30", hltConfig_,
					triggerResults_);
		} else if (MCSampleTag_ == "Summer12"){ //Summer12 MC
            return triggerFired("HLT_Ele27_WP80_v", hltConfig_, triggerResults_);
		} else
			return false;
	}
	return false;
}

bool TopPairElectronPlusJets2012SelectionFilter::hasExactlyOneIsolatedLepton() const {
	return goodIsolatedElectrons_.size() == 1;
}

bool TopPairElectronPlusJets2012SelectionFilter::passesLooseLeptonVeto() const {
	return looseMuons_.size() == 0;
}

bool TopPairElectronPlusJets2012SelectionFilter::passesDileptonVeto() const {
	return looseElectrons_.size() < 2;
}

bool TopPairElectronPlusJets2012SelectionFilter::passesConversionVeto() const {
//	if (hasSignalElectron_)
	if (hasExactlyOneIsolatedLepton())
	return signalElectron_.passConversionVeto()	&& signalElectron_.gsfTrack()->trackerExpectedHitsInner().numberOfHits() < 1; // left in the trackerExpectedHitsInner <1 as per twikis, although it is not there in the AnalysisTools, because it seems to make no difference to number of events passing
	return false;

}

bool TopPairElectronPlusJets2012SelectionFilter::hasAtLeastOneGoodJet() const {
	if (cleanedJets_.size() > 0)
		return getSmearedJetPtScale(cleanedJets_.at(0), 0)*cleanedJets_.at(0).pt() > min1JetPt_;

	return false;
}

bool TopPairElectronPlusJets2012SelectionFilter::hasAtLeastTwoGoodJets() const {
	if (cleanedJets_.size() > 1)
		return getSmearedJetPtScale(cleanedJets_.at(1), 0)*cleanedJets_.at(1).pt() > min2JetPt_;
	return false;
}

bool TopPairElectronPlusJets2012SelectionFilter::hasAtLeastThreeGoodJets() const {
	if (cleanedJets_.size() > 2)
		return getSmearedJetPtScale(cleanedJets_.at(2), 0)*cleanedJets_.at(2).pt() > min3JetPt_;
	return false;
}

bool TopPairElectronPlusJets2012SelectionFilter::hasAtLeastFourGoodJets() const {
	if (cleanedJets_.size() > 3)
		return getSmearedJetPtScale(cleanedJets_.at(3), 0)*cleanedJets_.at(3).pt() > min4JetPt_;
	return false;
}

bool TopPairElectronPlusJets2012SelectionFilter::hasAtLeastOneGoodBJet() const {
	return cleanedBJets_.size() > 0;
}

bool TopPairElectronPlusJets2012SelectionFilter::hasAtLeastTwoGoodBJets() const {
	return cleanedBJets_.size() > 1;
}

// ------------ method called once each job just before starting event loop  ------------
void TopPairElectronPlusJets2012SelectionFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TopPairElectronPlusJets2012SelectionFilter::endJob() {
}

bool TopPairElectronPlusJets2012SelectionFilter::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {

	bool changed = true;
	if (hltConfig_.init(iRun, iSetup, hltInputTag_.process(), changed)) {
		// if init returns TRUE, initialisation has succeeded!
		edm::LogInfo("TopPairElectronPlusJets2012SelectionFilter") << "HLT config with process name "
				<< hltInputTag_.process() << " successfully extracted";
	} else {
		// if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
		// with the file and/or code and needs to be investigated!
		edm::LogError("TopPairElectronPlusJets2012SelectionFilter_Error")
				<< "Error! HLT config extraction with process name " << hltInputTag_.process() << " failed";
		// In this case, all access methods will return empty values!
	}
	return true;
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairElectronPlusJets2012SelectionFilter);
