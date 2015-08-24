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
		jetInput_(iConfig.getParameter < edm::InputTag > ("jetInput")), //
		electronInput_(iConfig.getParameter < edm::InputTag > ("electronInput")), //
		muonInput_(iConfig.getParameter < edm::InputTag > ("muonInput")), //
		hltInputTag_(iConfig.getParameter < edm::InputTag > ("HLTInput")), //
		VertexInput_(iConfig.getParameter < edm::InputTag > ("VertexInput")), //
		trkInput_(iConfig.getParameter < edm::InputTag > ("trkInput")), //
		hcalNoiseInput_(iConfig.getParameter < edm::InputTag > ("HcalNoiseInput")), //
		hcalLaserFilterInput_(iConfig.getParameter < edm::InputTag > ("HCALLaserFilterInput")), //
		ecalDeadCellFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALDeadCellFilterInput")), //
		ecalLaserCorrFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALLaserCorrFilterInput")), //
		manystripclus53X_(iConfig.getParameter < edm::InputTag > ("ManyStripClus53XInput")), //
		toomanystripclus53X_(iConfig.getParameter < edm::InputTag > ("TooManyStripClus53XInput")), //
//		logErrorTooManyClusters_(iConfig.getParameter < edm::InputTag > ("LogErrorTooManyClusters")), //
		trackingFailureFilter_(iConfig.getParameter < edm::InputTag > ("TrackingFailureFilterInput")), //
		eeBadScFilter_(iConfig.getParameter < edm::InputTag > ("BadEESupercrystalFilterInput")), //
		min1JetPt_(iConfig.getParameter<double>("min1JetPt")), //
		min2JetPt_(iConfig.getParameter<double>("min2JetPt")), //
		min3JetPt_(iConfig.getParameter<double>("min3JetPt")), //
		min4JetPt_(iConfig.getParameter<double>("min4JetPt")), //
		tightMuonIso_(iConfig.getParameter<double>("tightMuonIsolation")), //
		controlMuonIso_(iConfig.getParameter<double>("controlMuonIsolation")), //
		looseElectronIso_(iConfig.getParameter<double>("looseElectronIsolation")), //
		looseMuonIso_(iConfig.getParameter<double>("looseMuonIsolation")), //
		useDeltaBetaCorrectionsForMuons_(iConfig.getParameter<bool>("useDeltaBetaCorrectionsForMuons")), //
		useDeltaBetaCorrectionsForElectrons_(iConfig.getParameter<bool>("useDeltaBetaCorrectionsForElectrons")), //
		useRhoActiveAreaCorrections_(iConfig.getParameter<bool>("useRhoActiveAreaCorrections")), // refers to electrons only
		useMETFilters_(iConfig.getParameter<bool>("useMETFilters")), //
		useEEBadScFilter_(iConfig.getParameter<bool>("useEEBadScFilter")), //
		tagAndProbeStudies_(iConfig.getParameter<bool>("tagAndProbeStudies")), //
		dropTriggerSelection_(iConfig.getParameter<bool>("dropTriggerSelection")), //
		prefix_(iConfig.getUntrackedParameter < std::string > ("prefix")), //
		MCSampleTag_(iConfig.getParameter < std::string > ("MCSampleTag")), //
		debug_(iConfig.getUntrackedParameter<bool>("debug")), //
		taggingMode_(iConfig.getParameter<bool>("taggingMode")), //
		bSelectionInTaggingMode_(iConfig.getParameter<bool>("bSelectionInTaggingMode")), //
		nonIsolatedMuonSelection_(iConfig.getParameter<bool>("nonIsolatedMuonSelection")), //
		passes_(), //
		runNumber_(0), //
		signalMuonIndex_(999), //
		isRealData_(false), //
		hasSignalMuon_(false), //
		hasGoodPV_(false), //
		rho_(0), //
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
	produces < pat::JetCollection > (prefix_ + "cleanedJets");
	produces < pat::MuonCollection > (prefix_ + "signalMuon");
	produces<unsigned int>(prefix_ + "signalMuonIndex");
}

void TopPairMuonPlusJetsSelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
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
	desc.add < InputTag > ("ECALLaserCorrFilterInput");
	desc.add < InputTag > ("ManyStripClus53XInput");
	desc.add < InputTag > ("TooManyStripClus53XInput");
//	desc.add < InputTag > ("LogErrorTooManyClusters");
	desc.add < InputTag > ("TrackingFailureFilterInput");
	desc.add < InputTag > ("BadEESupercrystalFilterInput");
	desc.add<double>("min1JetPt", 30.0);
	desc.add<double>("min2JetPt", 30.0);
	desc.add<double>("min3JetPt", 30.0);
	desc.add<double>("min4JetPt", 30.0);
	desc.add<double>("tightMuonIsolation", 0.12);
	desc.add<double>("controlMuonIsolation", 0.3);
	desc.add<double>("looseElectronIsolation", 0.15);
	desc.add<double>("looseMuonIsolation", 0.2);

	desc.add<bool>("useDeltaBetaCorrectionsForMuons", true);
	desc.add<bool>("useDeltaBetaCorrectionsForElectrons", false);
	desc.add<bool>("useRhoActiveAreaCorrections", true); // refers to electrons only
	desc.add<bool>("useMETFilters", false);
	desc.add<bool>("useEEBadScFilter", false);
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
	setupEventContent(iEvent, MCSampleTag_);
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	std::auto_ptr < pat::JetCollection > jetoutput(new pat::JetCollection());

	bool passesSelection(true);
	bool passesSelectionExceptBtagging(true);

	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		TTbarMuPlusJetsReferenceSelection::Step stepName = TTbarMuPlusJetsReferenceSelection::Step(step);
		if (debug_)
			cout << "Doing selection step: " << TTbarMuPlusJetsReferenceSelection::StringSteps[stepName] << " " << passesSelectionStep(iEvent, step, MCSampleTag_) << endl;

		bool passesStep(passesSelectionStep(iEvent, step, MCSampleTag_));

		// Remove at least 4 jet selection for QCD control region (only need at least 3)
		// Also require exactly zero b jets
		// Or exactly one b jet, as e.g. angle(b,l) only makes sense if there is at least one b jet
		if ( nonIsolatedMuonSelection_ ) {
			if ( stepName == TTbarMuPlusJetsReferenceSelection::AtLeastFourGoodJets )
				passesStep = true;

			if ( stepName == TTbarMuPlusJetsReferenceSelection::AtLeastOneBtag || stepName == TTbarMuPlusJetsReferenceSelection::AtLeastTwoBtags ) {
				passesStep = hasExactlyZeroGoodBJet() || hasExactlyOneGoodBJet() ;
			}
		}

		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;

		if ( step < TTbarMuPlusJetsReferenceSelection::AtLeastOneBtag )
			passesSelectionExceptBtagging = passesSelectionExceptBtagging && passesStep;

		// if doesn't pass selection and not in tagging mode, stop here to save CPU time
		if ( !(taggingMode_ || passesSelection) )
			break;
	}
	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		std::auto_ptr<bool> passesStep(new bool(passes_.at(step)));
		iEvent.put(passesStep, prefix_ + TTbarMuPlusJetsReferenceSelection::StringSteps[step]);
	}
	iEvent.put(std::auto_ptr<bool>(new bool(passesSelection)), prefix_ + "FullSelection");
	for (unsigned int index = 0; index < cleanedJets_.size(); ++index)
		jetoutput->push_back(cleanedJets_.at(index));
	iEvent.put(jetoutput, prefix_ + "cleanedJets");

	std::auto_ptr < pat::MuonCollection > signalMuon(new pat::MuonCollection());
	signalMuon->push_back(signalMuon_);
	iEvent.put(signalMuon, prefix_ + "signalMuon");

	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(signalMuonIndex_)),prefix_ + "signalMuonIndex");

	if ( !bSelectionInTaggingMode_ )
		return taggingMode_ || passesSelection;
	else
		return taggingMode_ || passesSelectionExceptBtagging;
}

void TopPairMuonPlusJetsSelectionFilter::setupEventContent(edm::Event& iEvent, std::string MCSampleTag_) {
	
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
	if (muons.isValid()) {
		if (debug_)
			cout << "Getting loose muons" << endl;
		getLooseMuons();
		//this is the correct order: goodIsolatedMuons, signalElectron, cleanedJets, cleanedBJets
		if (debug_)
			cout << "Getting isolated muons" << endl;
		goodIsolatedMuons();
		if (debug_)
			cout << "Getting signal muon" << endl;
		hasSignalMuon_ = goodIsolatedMuons_.size() > 0;
		if (hasSignalMuon_)
			signalMuon_ = goodIsolatedMuons_.front();
	} else {
		edm::LogError("TopPairMuonPlusJetsSelectionFilterError") << "Error! Can't get the product " << muonInput_;
	}
	if (debug_)
		cout << "Getting clean jets" << endl;
	cleanedJets(MCSampleTag_);
	if (debug_)
		cout << "Getting clean B jets" << endl;
	cleanedBJets();
}

void TopPairMuonPlusJetsSelectionFilter::getLooseElectrons() {
	looseElectrons_.clear();

	for (unsigned index = 0; index < electrons_.size(); ++index) {
		const pat::Electron electron = electrons_.at(index);
		if (isLooseElectron(electron))
			looseElectrons_.push_back(electron);
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isLooseElectron(const pat::Electron& electron) const {
	bool passesPtAndEta = electron.pt() > 20 && fabs(electron.eta()) < 2.5;
	//		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	bool passesID = electron.electronID("mvaTrigV0") > 0.5;
	bool passesIso = getRelativeIsolation(electron, 0.3, rho_, isRealData_, useDeltaBetaCorrectionsForElectrons_,
			useRhoActiveAreaCorrections_) < looseElectronIso_;
	
	return passesPtAndEta && passesID && passesIso;
}

void TopPairMuonPlusJetsSelectionFilter::getLooseMuons() {
	looseMuons_.clear();

	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);
		if (isLooseMuon(muon))
			looseMuons_.push_back(muon);
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isLooseMuon(const pat::Muon& muon) const {
	bool passesPtAndEta = muon.pt() > 10 && fabs(muon.eta()) < 2.5;
	bool passesID = muon.isPFMuon() && (muon.isGlobalMuon() || muon.isTrackerMuon());
	bool passesIso = getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) < looseMuonIso_;
	
	return passesPtAndEta && passesID && passesIso;
}

void TopPairMuonPlusJetsSelectionFilter::goodIsolatedMuons() {
	goodIsolatedMuons_.clear();
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);

		bool passesIso = false;

		if ( nonIsolatedMuonSelection_ )
			passesIso = getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) > controlMuonIso_;
		else
			passesIso = getRelativeIsolation(muon, 0.4, useDeltaBetaCorrectionsForMuons_) < tightMuonIso_;

		if (isGoodMuon(muon) && passesIso) {
			goodIsolatedMuons_.push_back(muon);
			//Check if this is the first, and therefore the signal, muon
			if ( goodIsolatedMuons_.size()==1 ) signalMuonIndex_ = index;
		}
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isGoodMuon(const pat::Muon& muon) const {
	if (debug_) {
		cout << "isGoodMuon:" << "hasGoodPV: " << hasGoodPV_ << endl;
		cout << "pT: " << muon.pt() << " eta: " << muon.eta() << " phi: " << muon.phi() << endl;
		cout << "d0: " << muon.dB(pat::Muon::PV2D) << " z-dist: " << fabs(muon.vertex().z() - primaryVertex_.z());
		cout << "isPFMuon: " << muon.isPFMuon() << " isGlobalMuon: " << muon.isGlobalMuon() << endl;
//		normChi2 is causing this:
//		Exception Message:
//		BadRefCore RefCore: Request to resolve a null or invalid reference to a product of type 'std::vector<reco::Track>' has been detected.
//		Please modify the calling code to test validity before dereferencing.

//		cout << "normChi2: " << muon.normChi2() << endl;
		if (muon.globalTrack().isNonnull()) {
			cout << "normChi2: " << muon.globalTrack()->normalizedChi2() << endl;
			cout << "numberOfValidMuonHits: " << muon.globalTrack()->hitPattern().numberOfValidMuonHits()
					<< " isGlobalMuon: " << muon.innerTrack()->hitPattern().numberOfValidPixelHits() << endl;
			cout << " trackerLayersWithMeasurement: " << muon.track()->hitPattern().trackerLayersWithMeasurement()
					<< endl;
		}
		cout << "numberOfMatchedStations: " << muon.numberOfMatchedStations() << endl;
	}
	bool passesPtAndEta = muon.pt() > 26. && fabs(muon.eta()) < 2.1;
	//2D impact w.r.t primary vertex
	if (!hasGoodPV_ or muon.globalTrack().isNull())
		return false;
	bool passesD0 = fabs(muon.dB(pat::Muon::PV2D)) < 0.2 && fabs(muon.vertex().z() - primaryVertex_.z()) < 0.5; //cm
	bool passesID = muon.isPFMuon() && muon.isGlobalMuon();
	bool trackQuality = muon.globalTrack()->normalizedChi2() < 10
			&& muon.track()->hitPattern().trackerLayersWithMeasurement() > 5
			&& muon.globalTrack()->hitPattern().numberOfValidMuonHits() > 0
			&& muon.innerTrack()->hitPattern().numberOfValidPixelHits() > 0 && muon.numberOfMatchedStations() > 1;
	return passesPtAndEta && passesD0 && passesID && trackQuality;
}

void TopPairMuonPlusJetsSelectionFilter::cleanedJets(std::string MCSampleTag_) {
	cleanedJets_.clear();
	for (unsigned index = 0; index < jets_.size(); ++index) {
		const pat::Jet jet = jets_.at(index);
		if (!isGoodJet(jet, MCSampleTag_))
			continue;
		bool overlaps(false);
		if (tagAndProbeStudies_) {
			if (goodIsolatedMuons_.size() >= 1)
				for (unsigned index = 0; index < goodIsolatedMuons_.size(); ++index) {
					double dR = deltaR(goodIsolatedMuons_.at(index), jet);
					if (dR < 0.3) overlaps = true;
				}
		}
		else {
			if (hasSignalMuon_ && goodIsolatedMuons_.size() == 1) {
				double dR = deltaR(signalMuon_, jet);
				overlaps = dR < 0.3;
			}
		}
		if (!overlaps)
			cleanedJets_.push_back(jet);
	}
}

void TopPairMuonPlusJetsSelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);
		if (jet.bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679 && jet.pt() > 30 ) {
			cleanedBJets_.push_back(jet);
		}
	}
}

bool TopPairMuonPlusJetsSelectionFilter::isGoodJet(const pat::Jet& jet, std::string MCSampleTag_) const {
	//both cuts are done at PAT config level (selectedPATJets) this is just for safety
	double smearFactor = getSmearedJetPtScale(jet, 0, MCSampleTag_);
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

bool TopPairMuonPlusJetsSelectionFilter::passesSelectionStep(edm::Event& iEvent, unsigned int selectionStep, std::string MCSampleTag_) const {
	TTbarMuPlusJetsReferenceSelection::Step step = TTbarMuPlusJetsReferenceSelection::Step(selectionStep);
	switch (step) {
	case TTbarMuPlusJetsReferenceSelection::AllEvents:
		return true;
	case TTbarMuPlusJetsReferenceSelection::EventCleaningAndTrigger:
		return passesEventCleaning(iEvent) && passesTriggerSelection();
	case TTbarMuPlusJetsReferenceSelection::OneIsolatedMuon:
		return hasExactlyOneIsolatedLepton();
	case TTbarMuPlusJetsReferenceSelection::LooseMuonVeto:
		return passesLooseMuonVeto();
	case TTbarMuPlusJetsReferenceSelection::LooseElectronVeto:
		return passesLooseElectronVeto();
	case TTbarMuPlusJetsReferenceSelection::AtLeastOneGoodJet:
		return hasAtLeastOneGoodJet(MCSampleTag_);
	case TTbarMuPlusJetsReferenceSelection::AtLeastTwoGoodJets:
		return hasAtLeastTwoGoodJets(MCSampleTag_);
	case TTbarMuPlusJetsReferenceSelection::AtLeastThreeGoodJets:
		return hasAtLeastThreeGoodJets(MCSampleTag_);
	case TTbarMuPlusJetsReferenceSelection::AtLeastFourGoodJets:
		return hasAtLeastFourGoodJets(MCSampleTag_);
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
	// Scraping veto is filtered on at
	if (!passesScrapingVeto(iEvent))
		return false;

	// Good Primary Vertex Part - goodness done at PAT selection level
	bool passesPrimaryVertexRequirement(hasGoodPV_);
//	edm::Handle < reco::VertexCollection > primaryVertices;
//	iEvent.getByLabel(VertexInput_, primaryVertices);
//	if (primaryVertices.isValid()) {
//		int nVertices = primaryVertices->size();
//		edm::LogInfo("TopPairMuonPlusJetsSelectionFilter") << "Total # Primary Vertices: " << nVertices;
//		if (nVertices > 0)
//			passesPrimaryVertexRequirement = true;
//	} else
//		edm::LogError("EventFilterError") << "Error! Can't get the product " << VertexInput_;
	if (!passesPrimaryVertexRequirement)
		return false;

	bool passesMETFilters(true);
	if (useMETFilters_) {
		passesMETFilters = passesMETFilters && passesFilter(iEvent, hcalNoiseInput_);
		passesMETFilters = passesMETFilters && passesFilter(iEvent, hcalLaserFilterInput_);
		passesMETFilters = passesMETFilters && passesFilter(iEvent, ecalDeadCellFilterInput_);
		passesMETFilters = passesMETFilters && passesFilter(iEvent, trackingFailureFilter_);
		passesMETFilters = passesMETFilters && passesFilter(iEvent, ecalLaserCorrFilterInput_);
		passesMETFilters = passesMETFilters && !passesFilter(iEvent, manystripclus53X_);
		passesMETFilters = passesMETFilters && !passesFilter(iEvent, toomanystripclus53X_);
//		passesMETFilters = passesMETFilters && !passesFilter(iEvent, logErrorTooManyClusters_);
		if (useEEBadScFilter_)
			passesMETFilters = passesMETFilters && passesFilter(iEvent, eeBadScFilter_);

		//beam halo ID
		bool cscTightID(false);
		edm::Handle < reco::BeamHaloSummary > TheBeamHaloSummary;
		iEvent.getByLabel("BeamHaloSummary", TheBeamHaloSummary);
		if (TheBeamHaloSummary.isValid()) {
			edm::LogInfo("TopPairMuonPlusJetsSelectionFilter") << "Successfully obtained BeamHaloSummary";
			const reco::BeamHaloSummary TheSummary = (*TheBeamHaloSummary.product());
			cscTightID = TheSummary.CSCTightHaloId();
		} else
			edm::LogError("TopPairMuonPlusJetsSelectionFilter_Error")
					<< "Error! Can't get the product BeamHaloSummary";
		//passes MET filters and is not BeamHalo
		passesMETFilters = passesMETFilters && !cscTightID;
	}

	return passesMETFilters;
}

bool TopPairMuonPlusJetsSelectionFilter::passesScrapingVeto(edm::Event& event) const {
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

bool TopPairMuonPlusJetsSelectionFilter::passesTriggerSelection() const {
	if (dropTriggerSelection_) 
		return true;
	else if (isRealData_) {
		if (runNumber_ >= 160404 && runNumber_ < 173236)
			return triggerFired("HLT_IsoMu24", hltConfig_, triggerResults_);
		else if (runNumber_ >= 173236 && runNumber_ < 190456)
			return triggerFired("HLT_IsoMu24_eta2p1", hltConfig_, triggerResults_);
		else //2012 Data
			return triggerFired("HLT_IsoMu24_eta2p1_v", hltConfig_, triggerResults_);
	} else {
		if (MCSampleTag_ == "Fall11") {//Fall11 MC
			return triggerFired("HLT_IsoMu24", hltConfig_, triggerResults_);
		} else if (MCSampleTag_ == "Summer12") {//Summer12 MC
			return triggerFired("HLT_IsoMu24_eta2p1_v", hltConfig_, triggerResults_);
		} else if (MCSampleTag_ == "Summer11Leg") {//Summer11Leg
			return true; // to be updated once we have trigger efficiencies
		}
	}
	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasExactlyOneIsolatedLepton() const {
	if (tagAndProbeStudies_)
		return goodIsolatedMuons_.size() >= 1;
	else
		return goodIsolatedMuons_.size() == 1;
}

bool TopPairMuonPlusJetsSelectionFilter::passesLooseElectronVeto() const {
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
		return looseMuons_.size() < 2;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastOneGoodJet(std::string MCSampleTag_) const {
	if (cleanedJets_.size() > 0)
		return getSmearedJetPtScale(cleanedJets_.at(0), 0, MCSampleTag_)*cleanedJets_.at(0).pt() > min1JetPt_;
	return false;

}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastTwoGoodJets(std::string MCSampleTag_) const {
	if (cleanedJets_.size() > 1)
		return getSmearedJetPtScale(cleanedJets_.at(1), 0, MCSampleTag_)*cleanedJets_.at(1).pt() > min2JetPt_;
	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastThreeGoodJets(std::string MCSampleTag_) const {
	if (cleanedJets_.size() > 2)
		return getSmearedJetPtScale(cleanedJets_.at(2), 0, MCSampleTag_)*cleanedJets_.at(2).pt() > min3JetPt_;
	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastFourGoodJets(std::string MCSampleTag_) const {
	if (cleanedJets_.size() > 3)
		return getSmearedJetPtScale(cleanedJets_.at(3), 0, MCSampleTag_)*cleanedJets_.at(3).pt() > min4JetPt_;
	return false;
}

bool TopPairMuonPlusJetsSelectionFilter::hasExactlyZeroGoodBJet() const {
	return cleanedBJets_.size() == 0;
}

bool TopPairMuonPlusJetsSelectionFilter::hasExactlyOneGoodBJet() const {
	return cleanedBJets_.size() == 1;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastOneGoodBJet() const {
	return cleanedBJets_.size() > 0;
}

bool TopPairMuonPlusJetsSelectionFilter::hasAtLeastTwoGoodBJets() const {
	return cleanedBJets_.size() > 1;
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
