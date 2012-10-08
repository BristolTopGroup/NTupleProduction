#include "BristolAnalysis/NTupleTools/plugins/TopPairMuonPlusJets2012SelectionFilter.h"
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

TopPairMuonPlusJets2012SelectionFilter::TopPairMuonPlusJets2012SelectionFilter(const edm::ParameterSet& iConfig) :
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
		tightMuonIso_(iConfig.getParameter<double>("tightMuonIsolation")), //
		looseElectronIso_(iConfig.getParameter<double>("looseElectronIsolation")), //
		looseMuonIso_(iConfig.getParameter<double>("looseMuonIsolation")), //
		useDeltaBetaCorrections_(iConfig.getParameter<bool>("useDeltaBetaCorrections")), //
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
}

void TopPairMuonPlusJets2012SelectionFilter::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
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
	desc.add<double>("min1JetPt", 45.0);
	desc.add<double>("min2JetPt", 45.0);
	desc.add<double>("min3JetPt", 45.0);
	desc.add<double>("min4JetPt", 20.0);
	desc.add<double>("tightMuonIsolation", 0.12);
	desc.add<double>("looseElectronIsolation", 0.15);
	desc.add<double>("looseMuonIsolation", 0.2);

	desc.add<bool>("useDeltaBetaCorrections", false);
	desc.add<bool>("useRhoActiveAreaCorrections", true);
	desc.add<bool>("useMETFilters", false);
	desc.add<bool>("useEEBadScFilter", false);

	desc.add < std::string > ("MCSampleTag", "Summer12");
	desc.addUntracked < std::string > ("prefix", "TopPairElectronPlusJets2012Selection.");
	desc.addUntracked<bool>("debug", false);
	desc.add<bool>("taggingMode", false);
	descriptions.add("applyTopPairMuonPlusJets2012Selection", desc);
}

TopPairMuonPlusJets2012SelectionFilter::~TopPairMuonPlusJets2012SelectionFilter() {

}

bool TopPairMuonPlusJets2012SelectionFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	setupEventContent(iEvent);
	unsigned int numberOfBtags(cleanedBJets_.size());
	iEvent.put(std::auto_ptr<unsigned int>(new unsigned int(numberOfBtags)), prefix_ + "NumberOfBtags");
	std::auto_ptr < pat::JetCollection > jetoutput(new pat::JetCollection());

	bool passesSelection(true);

	for (unsigned int step = 0; step < TTbarMuPlusJetsReferenceSelection::NUMBER_OF_SELECTION_STEPS; ++step) {
		if (debug_)
			cout << "Doing selection step: " << TTbarMuPlusJetsReferenceSelection::StringSteps[step] << endl;
		bool passesStep(passesSelectionStep(iEvent, step));
		passesSelection = passesSelection && passesStep;
		passes_.at(step) = passesStep;
		//if not in tagginmode and selection step doesn't pass leave loop.
		if (!(taggingMode_ || passesSelection))
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

	return taggingMode_ || passesSelection;
}

void TopPairMuonPlusJets2012SelectionFilter::setupEventContent(edm::Event& iEvent) {
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
		edm::LogError("TopPairMuonPlusJets2012SelectionFilterError") << "Error! Can't get the product " << VertexInput_;

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
	//this is the correct order: goodIsolatedMuons, signalElectron, cleanedJets, cleanedBJets
	if (debug_)
		cout << "Getting isolated muons" << endl;
	goodIsolatedMuons();
	if (debug_)
		cout << "Getting signal muon" << endl;
	hasSignalMuon_ = goodIsolatedMuons_.size() > 0;
	if (hasSignalMuon_)
		signalMuon_ = goodIsolatedMuons_.front();
	if (debug_)
		cout << "Getting clean jets" << endl;
	cleanedJets();
	if (debug_)
		cout << "Getting clean B jets" << endl;
	cleanedBJets();
}

void TopPairMuonPlusJets2012SelectionFilter::getLooseElectrons() {
	looseElectrons_.clear();

	for (unsigned index = 0; index < electrons_.size(); ++index) {
		const pat::Electron electron = electrons_.at(index);
		if (isLooseElectron(electron))
			looseElectrons_.push_back(electron);
	}
}

bool TopPairMuonPlusJets2012SelectionFilter::isLooseElectron(const pat::Electron& electron) const {
	bool passesPtAndEta = electron.pt() > 20 && fabs(electron.eta()) < 2.5;
	//		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442 || fabs(electron.superCluster()->eta()) > 1.5660;
	bool passesID = electron.electronID("mvaTrigV0") > 0.0;
	bool passesIso = getRelativeIsolation(electron) < looseElectronIso_;
	return passesPtAndEta && passesID && passesIso;
}

double TopPairMuonPlusJets2012SelectionFilter::getRelativeIsolation(const pat::Electron& electron) const {
	//code from: https://twiki.cern.ch/twiki/bin/view/CMS/PfIsolation
	float AEff03 = 0.00;

	if (isRealData_) {
		AEff03 = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03,
				electron.superCluster()->eta(), ElectronEffectiveArea::kEleEAData2011);
	} else {
		AEff03 = ElectronEffectiveArea::GetElectronEffectiveArea(ElectronEffectiveArea::kEleGammaAndNeutralHadronIso03,
				electron.superCluster()->eta(), ElectronEffectiveArea::kEleEAFall11MC);
	}

	AbsVetos vetos_ch;
	AbsVetos vetos_nh;
	AbsVetos vetos_ph;

	Direction Dir = Direction(electron.superCluster()->eta(), electron.superCluster()->phi());

	//threshold veto
	//vetos_nh.push_back(new ThresholdVeto( 0.5 ));
	//vetos_ph.push_back(new ThresholdVeto( 0.5 ));
	//rectangular veto
	//vetos_nh.push_back(new RectangularEtaPhiVeto( Dir, -0.1, 0.1, -0.2, 0.2));
	//vetos_ph.push_back(new RectangularEtaPhiVeto( Dir, -0.1, 0.1, -0.2, 0.2));

	//pf isolation veto setup EGM recommendation
	if (abs(electron.superCluster()->eta()) > 1.479) {
		vetos_ch.push_back(new ConeVeto(Dir, 0.015));
		vetos_ph.push_back(new ConeVeto(Dir, 0.08));
	}

	//cone size 0.3
	const double chIso03 = electron.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.3, vetos_ch).first;
	const double nhIso03 = electron.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.3, vetos_nh).first;
	const double phIso03 = electron.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.3, vetos_ph).first;

	const double puChIso03 = electron.isoDeposit(pat::PfPUChargedHadronIso)->depositAndCountWithin(0.3, vetos_ch).first;

	const double relIso = (chIso03 + nhIso03 + phIso03) / electron.pt();
	const double relIsodb = (chIso03 + max(0.0, nhIso03 + phIso03 - 0.5 * puChIso03)) / electron.pt();
	const double relIsorho = (chIso03 + max(0.0, nhIso03 + phIso03 - rho_ * AEff03)) / electron.pt();

	if (useDeltaBetaCorrections_)
		return relIsodb;
	if (useRhoActiveAreaCorrections_)
		return relIsorho;

	return relIso;
}

void TopPairMuonPlusJets2012SelectionFilter::getLooseMuons() {
	looseMuons_.clear();

	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);
		if (isLooseMuon(muon))
			looseMuons_.push_back(muon);
	}
}

bool TopPairMuonPlusJets2012SelectionFilter::isLooseMuon(const pat::Muon& muon) const {
	bool passesPtAndEta = muon.pt() > 10 && fabs(muon.eta()) < 2.5;
	bool passesID = muon.isPFMuon() && (muon.isGlobalMuon() || muon.isTrackerMuon());
	bool passesIso = getRelativeIsolation(muon) < looseMuonIso_;
	return passesPtAndEta && passesID && passesIso;
}

double TopPairMuonPlusJets2012SelectionFilter::getRelativeIsolation(const pat::Muon& muon) const {
	//cone size 0.4
	const double chIso04 = muon.isoDeposit(pat::PfChargedHadronIso)->depositAndCountWithin(0.4).first;
	const double nhIso04 = muon.isoDeposit(pat::PfNeutralHadronIso)->depositAndCountWithin(0.4).first;
	const double phIso04 = muon.isoDeposit(pat::PfGammaIso)->depositAndCountWithin(0.4).first;

	const double puChIso04 = muon.isoDeposit(pat::PfPUChargedHadronIso)->depositAndCountWithin(0.4).first;

	const double relIso = (chIso04 + nhIso04 + phIso04) / muon.pt();
	const double relIsodb = (chIso04 + max(0.0, nhIso04 + phIso04 - 0.5 * puChIso04)) / muon.pt();

	if (useDeltaBetaCorrections_ || useRhoActiveAreaCorrections_) //atm leave active area
		return relIsodb;

	return relIso;
}

void TopPairMuonPlusJets2012SelectionFilter::goodIsolatedMuons() {
	goodIsolatedMuons_.clear();
	for (unsigned index = 0; index < muons_.size(); ++index) {
		const pat::Muon muon = muons_.at(index);
		if (debug_) {
			cout << "Muon:" << endl;
			cout << "pT: " << muon.pt() << " eta: " << muon.eta() << " phi: " << muon.phi() << endl;
		}

		bool passesIso = getRelativeIsolation(muon) < tightMuonIso_;
		if (isGoodMuon(muon) && passesIso)
			goodIsolatedMuons_.push_back(muon);
	}
}

bool TopPairMuonPlusJets2012SelectionFilter::isGoodMuon(const pat::Muon& muon) const {
	bool passesPtAndEta = muon.pt() > 26. && fabs(muon.eta()) < 2.1;
	//2D impact w.r.t primary vertex
	if (!hasGoodPV_)
		return false;
	bool passesD0 = muon.dB(pat::Muon::PV2D) < 0.2 && fabs(muon.vertex().z() - primaryVertex_.z()) < 0.5; //cm
	bool passesID = muon.isPFMuon() && muon.isGlobalMuon();
	bool trackQuality = muon.normChi2() < 10 && muon.track()->hitPattern().trackerLayersWithMeasurement() > 5
			&& muon.globalTrack()->hitPattern().numberOfValidMuonHits() > 0
			&& muon.innerTrack()->hitPattern().numberOfValidPixelHits() > 0 && muon.numberOfMatchedStations() > 1;
	return passesPtAndEta && passesD0 && passesID && trackQuality;
}

void TopPairMuonPlusJets2012SelectionFilter::cleanedJets() {
	cleanedJets_.clear();
	for (unsigned index = 0; index < jets_.size(); ++index) {
		const pat::Jet jet = jets_.at(index);
		if (!isGoodJet(jet))
			continue;
		bool overlaps(false);
		if (hasSignalMuon_) {
			double dR = deltaR(signalMuon_, jet);
			overlaps = dR < 0.3;
		}
		if (!overlaps)
			cleanedJets_.push_back(jet);
	}
}

void TopPairMuonPlusJets2012SelectionFilter::cleanedBJets() {
	cleanedBJets_.clear();
	for (unsigned index = 0; index < cleanedJets_.size(); ++index) {
		const pat::Jet jet = cleanedJets_.at(index);
		if (jet.bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679)
			cleanedBJets_.push_back(jet);
	}
}

bool TopPairMuonPlusJets2012SelectionFilter::isGoodJet(const pat::Jet& jet) const {
	//both cuts are done at PAT config level (selectedPATJets) this is just for safety
	bool passesPtAndEta(jet.pt() > 20. && fabs(jet.eta() < 2.5));
	return passesPtAndEta;
}

bool TopPairMuonPlusJets2012SelectionFilter::passesSelectionStep(edm::Event& iEvent, unsigned int selectionStep) const {
	TTbarMuPlusJetsReferenceSelection::Step step = TTbarMuPlusJetsReferenceSelection::Step(selectionStep);
	switch (step) {
	case TTbarMuPlusJetsReferenceSelection::AllEvents:
		return true;
	case TTbarMuPlusJetsReferenceSelection::EventCleaningAndTrigger:
		return passesEventCleaning(iEvent) && passesTriggerSelection();
	case TTbarMuPlusJetsReferenceSelection::OneIsolatedMuon:
		return hasExactlyOneIsolatedLepton();
	case TTbarMuPlusJetsReferenceSelection::LooseElectronVeto:
		return passesLooseLeptonVeto();
	case TTbarMuPlusJetsReferenceSelection::DiLeptonVeto:
		return passesDileptonVeto();
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

bool TopPairMuonPlusJets2012SelectionFilter::passesEventCleaning(edm::Event& iEvent) const {
	// Scraping veto is filtered on at
	if (!passesScrapingVeto(iEvent))
		return false;

	// Good Primary Vertex Part - goodness done at PAT selection level
	bool passesPrimaryVertexRequirement(hasGoodPV_);
//	edm::Handle < reco::VertexCollection > primaryVertices;
//	iEvent.getByLabel(VertexInput_, primaryVertices);
//	if (primaryVertices.isValid()) {
//		int nVertices = primaryVertices->size();
//		edm::LogInfo("TopPairMuonPlusJets2012SelectionFilter") << "Total # Primary Vertices: " << nVertices;
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
		if (useEEBadScFilter_)
			passesMETFilters = passesMETFilters && passesFilter(iEvent, eeBadScFilter_);

		//beam halo ID
		bool cscTightID(false);
		edm::Handle < reco::BeamHaloSummary > TheBeamHaloSummary;
		iEvent.getByLabel("BeamHaloSummary", TheBeamHaloSummary);
		if (TheBeamHaloSummary.isValid()) {
			edm::LogInfo("TopPairMuonPlusJets2012SelectionFilter") << "Successfully obtained BeamHaloSummary";
			const reco::BeamHaloSummary TheSummary = (*TheBeamHaloSummary.product());
			cscTightID = TheSummary.CSCTightHaloId();
		} else
			edm::LogError("TopPairMuonPlusJets2012SelectionFilter_Error")
					<< "Error! Can't get the product BeamHaloSummary";
		//passes MET filters and is not BeamHalo
		passesMETFilters = passesMETFilters && !cscTightID;
	}

	return passesMETFilters;
}

bool TopPairMuonPlusJets2012SelectionFilter::passesScrapingVeto(edm::Event& event) const {
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

bool TopPairMuonPlusJets2012SelectionFilter::passesTriggerSelection() const {
	if (isRealData_) {
		if (runNumber_ >= 160404 && runNumber_ <= 173236)
			return triggerFired("HLT_IsoMu24", hltConfig_, triggerResults_);
		else if (runNumber_ >= 173236 && runNumber_ < 190456) //other triggers available (mainly sTop
			return triggerFired("HLT_IsoMu24_eta2p1", hltConfig_, triggerResults_);
		else if (runNumber_ >= 190456 && runNumber_ <= 193805)
			return triggerFired("HLT_IsoMu20_eta2p1_TriCentralPFJet30", hltConfig_, triggerResults_)
					|| triggerFired("HLT_IsoMu20_eta2p1_TriCentralPFNoPUJet30", hltConfig_, triggerResults_);
		else if (runNumber_ > 193806)
			return triggerFired("HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30", hltConfig_, triggerResults_)
					|| triggerFired("HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_30_20", hltConfig_, triggerResults_)
					|| triggerFired("HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet45_35_25", hltConfig_, triggerResults_);
		else
			return false;
	} else {
		if (MCSampleTag_ == "Fall11") {
			//Fall11 MC
			return triggerFired("HLT_IsoMu24", hltConfig_, triggerResults_);
		} else {
			//Summer11 MC
			bool fired_START52_V5 = triggerFired("HLT_IsoMu20_eta2p1_TriCentralPFJet30", hltConfig_, triggerResults_);
			bool fired_START52_V9 = triggerFired("HLT_IsoMu17_eta2p1_TriCentralPFJet30", hltConfig_, triggerResults_)
					|| triggerFired("HLT_IsoMu20_eta2p1_TriCentralPFNoPUJet30", hltConfig_, triggerResults_);
			bool fired_START53_V7A = triggerFired("HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_30_20", hltConfig_,
					triggerResults_);
			return fired_START52_V5 || fired_START52_V9 || fired_START53_V7A;
		}
	}

	return false;
}

bool TopPairMuonPlusJets2012SelectionFilter::hasExactlyOneIsolatedLepton() const {
	return goodIsolatedMuons_.size() == 1;
}

bool TopPairMuonPlusJets2012SelectionFilter::passesLooseLeptonVeto() const {
	return looseElectrons_.size() < 2;
}

bool TopPairMuonPlusJets2012SelectionFilter::passesDileptonVeto() const {
	return looseMuons_.size() == 0;
}

bool TopPairMuonPlusJets2012SelectionFilter::hasAtLeastOneGoodJet() const {
	if (cleanedJets_.size() > 0)
		return cleanedJets_.at(0).pt() > min1JetPt_;

	return false;

}

bool TopPairMuonPlusJets2012SelectionFilter::hasAtLeastTwoGoodJets() const {
	if (cleanedJets_.size() > 1)
		return cleanedJets_.at(1).pt() > min2JetPt_;
	return false;
}

bool TopPairMuonPlusJets2012SelectionFilter::hasAtLeastThreeGoodJets() const {
	if (cleanedJets_.size() > 2)
		return cleanedJets_.at(2).pt() > min3JetPt_;
	return false;
}

bool TopPairMuonPlusJets2012SelectionFilter::hasAtLeastFourGoodJets() const {
	if (cleanedJets_.size() > 3)
		return cleanedJets_.at(3).pt() > min4JetPt_;
	return false;
}

bool TopPairMuonPlusJets2012SelectionFilter::hasAtLeastOneGoodBJet() const {
	return cleanedBJets_.size() > 0;
}

bool TopPairMuonPlusJets2012SelectionFilter::hasAtLeastTwoGoodBJets() const {
	return cleanedBJets_.size() > 1;
}

// ------------ method called once each job just before starting event loop  ------------
void TopPairMuonPlusJets2012SelectionFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TopPairMuonPlusJets2012SelectionFilter::endJob() {
}

bool TopPairMuonPlusJets2012SelectionFilter::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {

	bool changed = true;
	if (hltConfig_.init(iRun, iSetup, hltInputTag_.process(), changed)) {
		// if init returns TRUE, initialisation has succeeded!
		edm::LogInfo("TopPairMuonPlusJets2012SelectionFilter") << "HLT config with process name "
				<< hltInputTag_.process() << " successfully extracted";
	} else {
		// if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
		// with the file and/or code and needs to be investigated!
		edm::LogError("TopPairMuonPlusJets2012SelectionFilter_Error")
				<< "Error! HLT config extraction with process name " << hltInputTag_.process() << " failed";
		// In this case, all access methods will return empty values!
	}
	return true;
}

//define this as a plug-in
DEFINE_FWK_MODULE (TopPairMuonPlusJets2012SelectionFilter);
