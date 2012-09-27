#include "BristolAnalysis/NTupleTools/interface/TopSemiLeptonicEventFilter.h"
// system include files
#include <memory>

// user include files


#include "FWCore/Framework/interface/MakerMacros.h"


using namespace edm;
using namespace std;

TopSemiLeptonicEventFilter::TopSemiLeptonicEventFilter(const edm::ParameterSet& iConfig) :
    jetInput_(iConfig.getParameter<edm::InputTag> ("jetInput")),
    electronInput_(iConfig.getParameter<edm::InputTag> ("electronInput")),
    muonInput_(iConfig.getParameter<edm::InputTag> ("muonInput")),
    vertexInput_(iConfig.getParameter<edm::InputTag>("VertexInput")),
    hcalNoiseInput_(iConfig.getParameter<edm::InputTag>("HcalNoiseInput")),
    trkInput_(iConfig.getParameter<edm::InputTag>("TracksInput")),
    minJetPt_(iConfig.getParameter<double> ("minJetPt")),
    maxAbsJetEta_(iConfig.getParameter<double> ("maxAbsJetEta")),
    minElectronPt_(iConfig.getParameter<double> ("minElectronPt")),
    maxAbsElectronEta_(iConfig.getParameter<double> ("maxAbsElectronEta")),
    minMuonPt_(iConfig.getParameter<double> ("minMuonPt")),
    maxAbsMuonEta_(iConfig.getParameter<double> ("maxAbsMuonEta")),
    tightElectronIso_(0.125),
    looseElectronIso_(0.2),
    tightMuonIso_(0.1),
    looseMuonIso_(0.2),
    electronPlusJetsSelection_(true),
    muonPlusJetsSelection_(false),
    useTrigger_(false),
    useCiCElectronID_(iConfig.getParameter<bool>("useCiCElectronID")),
    vtxMinNDOF_(iConfig.getParameter<unsigned int>("VertexMinimumNDOF")),
    vtxMaxAbsZ_(iConfig.getParameter<double>("VertexMaxAbsZ")),
    vtxMaxAbsRho_(iConfig.getParameter<double>("VertexMaxAbsRho")),
    numTracks_(iConfig.getParameter<unsigned int>("NumTracks")),
    hpTrackThreshold_(iConfig.getParameter<double>("HPTrackThreshold")),
    debug_(iConfig.getUntrackedParameter<bool> ("debug")),
    passes_(),
    totalCount(0)//,
//    hCount()
{

//    edm::Service<TFileService> histServ;

    unsigned int nSteps(Selection::NUMBER_OF_SELECTION_STEPS);
//    hCount = histServ->make<TH1I> ("EventCounter", "Event Counter", nSteps, -0.5, double(nSteps) + 0.5);
//    hCount->GetXaxis()->SetBinLabel(1, "all events");
    for(unsigned int step = 0; step < nSteps; ++step){
    	passes_.at(step) = 0;
//    	hCount->GetXaxis()->SetBinLabel(step + 2, Selection::StringSteps[step].c_str());
    }
}

TopSemiLeptonicEventFilter::~TopSemiLeptonicEventFilter() {

}

bool TopSemiLeptonicEventFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    ++totalCount;


    if (passesEventCleaning(iEvent))
		passes_.at(Selection::EventCleaning)++;
    else
		return false;


    if (passesEventCleaning(iEvent) || !useTrigger_)
		passes_.at(Selection::Trigger)++;
    else
		return false;

    edm::Handle <pat::JetCollection> jets;
	iEvent.getByLabel(jetInput_, jets);

	edm::Handle <pat::ElectronCollection> electrons;
	iEvent.getByLabel(electronInput_, electrons);

	edm::Handle < pat::MuonCollection > muons;
	iEvent.getByLabel(muonInput_, muons);

	const pat::JetCollection & allJets = * jets;
	const pat::ElectronCollection & allElectrons = * electrons;
	const pat::MuonCollection & allMuons= * muons;

	const pat::ElectronCollection goodIsolatedElectrons = getGoodIsolatedElectrons(allElectrons);
	const pat::ElectronCollection looseElectrons = getLooseElectrons(allElectrons);
	const pat::MuonCollection looseMuons = getLooseMuons(allMuons);
	const pat::JetCollection goodJets = getGoodJets(allJets);
	const pat::ElectronCollection cleanedGoodIsoElectrons = cleanElectronsAgainstJets(goodIsolatedElectrons, goodJets);
	const pat::JetCollection cleanedGoodJets = cleanJetsAgainstElectrons(goodJets, goodIsolatedElectrons);
	const pat::ElectronCollection cleanedLooseElectrons = removeGoodIsolatedElectronsFromLooseElectrons(goodIsolatedElectrons, looseElectrons);

    if ((cleanedGoodIsoElectrons.size() == 1 && electronPlusJetsSelection_))
		passes_.at(Selection::ExactlyOneIsolatedLepton)++;
    else
		return false;

    const pat::Electron selectedElectron = cleanedGoodIsoElectrons.front();

    if (looseMuons.size() == 0)
		passes_.at(Selection::LooseMuonVeto)++;
    else
		return false;

//    if (passesLooseElectronVeto(selectedElectron, looseElectrons))
    if (cleanedLooseElectrons.size() == 0)
		passes_.at(Selection::LooseElectronVeto)++;
    else
		return false;



    if (selectedElectron.gsfTrack()->trackerExpectedHitsInner().numberOfHits() == 0 || muonPlusJetsSelection_)
		passes_.at(Selection::ConvRejectionInnerHits)++;
    else
		return false;

    if (!(selectedElectron.convDist() < 0.02 && selectedElectron.convDcot() < 0.02) || muonPlusJetsSelection_)
		passes_.at(Selection::ConvRejectionPartnerTrack)++;
    else
		return false;

    if (cleanedGoodJets.size() > 0)
		passes_.at(Selection::OneJet)++;
    else
		return false;

	if (cleanedGoodJets.size() > 1)
		passes_.at(Selection::TwoJets)++;
	else
		return false;

	if (cleanedGoodJets.size() > 2)
		passes_.at(Selection::ThreeJets)++;
	else
		return false;

	if (cleanedGoodJets.size() > 3)
		passes_.at(Selection::FourJets)++;
	else
		return false;


	return true;
}

// ------------ method called once each job just before starting event loop  ------------
void TopSemiLeptonicEventFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void TopSemiLeptonicEventFilter::endJob() {
//    hCount->SetBinContent(1, totalCount);
    cout << "Total events = " << totalCount << endl;
    unsigned int nSteps(Selection::NUMBER_OF_SELECTION_STEPS);
    for (unsigned int step = 0; step < nSteps; ++step) {
    	cout << Selection::StringSteps[step] << " = " << passes_.at(step) << endl;
//		hCount->SetBinContent(step + 2, passes_.at(step));
	}
}

bool TopSemiLeptonicEventFilter::passesEventCleaning(edm::Event& iEvent) const{
	edm::Handle<bool> hbheFilterResult;
	iEvent.getByLabel(hcalNoiseInput_, hbheFilterResult);

	if (hbheFilterResult.isValid()) {
		edm::LogInfo("TopSemiLeptonicEventFilter") << "Successfully obtained " << hcalNoiseInput_;

	} else {
		edm::LogError("TopSemiLeptonicEventFilter_EventSelectionError") << "Error! Can't get the product " << hcalNoiseInput_;
	}

	if (*hbheFilterResult == false)
		return false;

	// Scraping Events Part
	edm::Handle < reco::TrackCollection > tracks;
	iEvent.getByLabel(trkInput_, tracks);
	double fraction = 1.;

	if (tracks.isValid()) {
		edm::LogInfo("TopSemiLeptonicEventFilter") << "Total # Tracks: " << tracks->size();

		int numhighpurity = 0;

		reco::TrackBase::TrackQuality trackQuality = reco::TrackBase::qualityByName("highPurity");

		if (tracks->size() > numTracks_) {
			for (reco::TrackCollection::const_iterator it = tracks->begin(); it != tracks->end(); ++it) {
				if (it->quality(trackQuality))
					numhighpurity++;
			}
			fraction = (double) numhighpurity / (double) tracks->size();

		}
	} else {
		edm::LogError("TopSemiLeptonicEventFilterError") << "Error! Can't get the product " << trkInput_;
	}
	if (fraction < hpTrackThreshold_)
		return false;

	// Good Primary Vertex Part
	edm::Handle < reco::VertexCollection > primaryVertices;
	iEvent.getByLabel(vertexInput_, primaryVertices);
	int numGoodVertices(0);

	if (primaryVertices.isValid()) {
		edm::LogInfo("TopSemiLeptonicEventFilter") << "Total # Primary Vertices: " << primaryVertices->size();

		for (reco::VertexCollection::const_iterator it = primaryVertices->begin(); it != primaryVertices->end(); ++it) {
			if (!(it->isFake()) && it->ndof() >= vtxMinNDOF_ && fabs(it->z()) <= vtxMaxAbsZ_
					&& fabs(it->position().rho()) <= vtxMaxAbsRho_)
				++numGoodVertices;
		}
	} else {
		edm::LogError("TopSemiLeptonicEventFilterError") << "Error! Can't get the product " << vertexInput_;
	}
	if (numGoodVertices < 1)
		return false;

	return true;
}

bool TopSemiLeptonicEventFilter::passesElectronTrigger() const{
	//TODO: implement
	return true;
}

bool TopSemiLeptonicEventFilter::passesMuonTrigger() const{
	//TODO: implement
	return true;
}

pat::ElectronCollection TopSemiLeptonicEventFilter::getGoodIsolatedElectrons(const pat::ElectronCollection electrons) const {
	pat::ElectronCollection goodIsoElectrons;

	for (unsigned index = 0; index < electrons.size(); ++index) {
		const pat::Electron electron = electrons.at(index);
		if (debug_) {
			cout << "Electron:" << endl;
			cout << "pT: " << electron.pt() << " eta: " << electron.eta() << " phi: " << electron.phi() << endl;
		}

		bool passesPtAndEta = electron.pt() > minElectronPt_ && fabs(electron.eta()) < maxAbsElectronEta_;
		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442
				|| fabs(electron.superCluster()->eta()) > 1.5660;
		bool passesD0 = electron.dB(pat::Electron::BS2D) < 0.02;//cm


		bool passesID = false;
		if(useCiCElectronID_)
			passesID = electron.electronID("eidHyperTight1MC") > 0;
		else{//SimpleCutBasedID WP70
			bool passesSigmaIEta(false);
			bool passesDPhiIn(false);
			bool passesDEtaIn(false);
			bool passesHadOverEm(false);

			if (fabs(electron.superCluster()->eta()) < 1.4442) {
				passesSigmaIEta = electron.sigmaIetaIeta() < 0.01;
				passesDPhiIn = fabs(electron.deltaPhiSuperClusterTrackAtVtx()) < 0.03;
				passesDEtaIn = fabs(electron.deltaEtaSuperClusterTrackAtVtx()) < 0.004;
				passesHadOverEm = electron.hadronicOverEm() < 0.025;
			} else {
				passesSigmaIEta = electron.sigmaIetaIeta() < 0.03;
				passesDPhiIn = fabs(electron.deltaPhiSuperClusterTrackAtVtx()) < 0.02;
				passesDEtaIn = fabs(electron.deltaEtaSuperClusterTrackAtVtx()) < 0.005;
				passesHadOverEm = electron.hadronicOverEm() < 0.025;
			}
			passesID = passesSigmaIEta && passesDPhiIn && passesDEtaIn && passesHadOverEm;
		}

		double relIso = (electron.chargedHadronIso() + electron.neutralHadronIso() + electron.photonIso())
				/ electron.et();

		bool passesIso = relIso < 0.125;
		if (passesPtAndEta && notInCrack && passesD0 && passesID && passesIso)
			goodIsoElectrons.push_back(electron);

	}
	return goodIsoElectrons;
}

pat::ElectronCollection TopSemiLeptonicEventFilter::getLooseElectrons(const pat::ElectronCollection electrons) const {
	pat::ElectronCollection looseElectrons;

	for (unsigned index = 0; index < electrons.size(); ++index) {
		const pat::Electron electron = electrons.at(index);
		if (debug_) {
			cout << "Electron:" << endl;
			cout << "pT: " << electron.pt() << " eta: " << electron.eta() << " phi: " << electron.phi() << endl;
		}

		bool passesPtAndEta = electron.pt() > 20 && fabs(electron.eta()) < 2.5;
		bool notInCrack = fabs(electron.superCluster()->eta()) < 1.4442
				|| fabs(electron.superCluster()->eta()) > 1.5660;
		bool passesID = false;
		if(useCiCElectronID_)
			passesID = electron.electronID("eidLooseMC") > 0;
		else {//SimpleCutBasedID WP95
			bool passesSigmaIEta(false);
			bool passesDPhiIn(false);
			bool passesDEtaIn(false);
			bool passesHadOverEm(false);

			if (fabs(electron.superCluster()->eta()) < 1.4442) {
				passesSigmaIEta = electron.sigmaIetaIeta() < 0.01;
				passesDPhiIn = fabs(electron.deltaPhiSuperClusterTrackAtVtx()) < 0.8;
				passesDEtaIn = fabs(electron.deltaEtaSuperClusterTrackAtVtx()) < 0.007;
				passesHadOverEm = electron.hadronicOverEm() < 0.15;
			} else {
				passesSigmaIEta = electron.sigmaIetaIeta() < 0.03;
				passesDPhiIn = fabs(electron.deltaPhiSuperClusterTrackAtVtx()) < 0.7;
				passesDEtaIn = fabs(electron.deltaEtaSuperClusterTrackAtVtx()) < 0.01;
				passesHadOverEm = electron.hadronicOverEm() < 0.07;
			}
			passesID = passesSigmaIEta && passesDPhiIn && passesDEtaIn && passesHadOverEm;
		}
		double relIso = (electron.chargedHadronIso() + electron.neutralHadronIso() + electron.photonIso())
				/ electron.et();

		bool passesIso = relIso < 0.2;
		if (passesPtAndEta && notInCrack && passesID && passesIso)
			looseElectrons.push_back(electron);

	}
	return looseElectrons;
}

pat::JetCollection TopSemiLeptonicEventFilter::getGoodJets(const pat::JetCollection jets) const{
	pat::JetCollection goodJets;
	for (unsigned index = 0; index < jets.size(); ++index) {
		const pat::Jet jet = jets.at(index);
		bool passesPtAndEta = jet.pt() > minJetPt_ && fabs(jet.eta()) < maxAbsJetEta_;
		bool passesID = jet.numberOfDaughters() > 1 && jet.neutralHadronEnergyFraction() < 0.99
				&& jet.neutralEmEnergyFraction() < 0.99
				&& ((jet.chargedEmEnergyFraction() < 0.99 && jet.chargedHadronEnergyFraction() > 0
						&& jet.chargedMultiplicity() > 0) || fabs(jet.eta()) > 2.4);
		if(passesPtAndEta && passesID)
			goodJets.push_back(jet);
	}
	return goodJets;
}

pat::MuonCollection TopSemiLeptonicEventFilter::getLooseMuons(const pat::MuonCollection muons) const {
	pat::MuonCollection looseMuons;
	for (unsigned index = 0; index < muons.size(); ++index) {
		const pat::Muon muon = muons.at(index);
		bool isGlobal = muon.isGood("AllGlobalMuons") > 0;
		bool ptAndEta = muon.pt() > 10.0 && fabs(muon.eta()) < 2.5;
		double relIso = (muon.chargedHadronIso() + muon.neutralHadronIso() + muon.photonIso()) / muon.pt();
		bool passIso = relIso < 0.2;

		if (isGlobal && ptAndEta && passIso)
			looseMuons.push_back(muon);
	}
	return looseMuons;
}

pat::ElectronCollection TopSemiLeptonicEventFilter::cleanElectronsAgainstJets(const pat::ElectronCollection electrons,
		const pat::JetCollection jets) const {
	pat::ElectronCollection cleanElectrons;
	for (unsigned index = 0; index < electrons.size(); ++index) {
		const pat::Electron electron = electrons.at(index);
		bool overlaps(true);
		for (unsigned jetIndex = 0; jetIndex < jets.size(); ++jetIndex) {
			const pat::Jet jet = jets.at(jetIndex);
			double dR = deltaR(electron, jet);
			overlaps = dR < 0.3;
		}
		if (!overlaps)
			cleanElectrons.push_back(electron);
	}
	return cleanElectrons;
}

pat::JetCollection TopSemiLeptonicEventFilter::cleanJetsAgainstElectrons(const pat::JetCollection jets,
		const pat::ElectronCollection electrons) const {
	pat::JetCollection cleanJets;
	for (unsigned index = 0; index < jets.size(); ++index) {
		const pat::Jet jet = jets.at(index);
		bool overlaps(true);
		for (unsigned eleIndex = 0; eleIndex < electrons.size(); ++eleIndex) {
			const pat::Electron electron = electrons.at(eleIndex);
			double dR = deltaR(electron, jet);
			overlaps = dR < 0.3;
		}
		if (!overlaps)
			cleanJets.push_back(jet);
	}
	return cleanJets;
}

pat::ElectronCollection TopSemiLeptonicEventFilter::removeGoodIsolatedElectronsFromLooseElectrons(
		const pat::ElectronCollection goodElectrons, const pat::ElectronCollection looseElectrons) const {
	pat::ElectronCollection cleanElectrons;
	for (unsigned index = 0; index < looseElectrons.size(); ++index) {
		const pat::Electron looseElectron = looseElectrons.at(index);
		bool overlaps(true);
		for (unsigned goodIndex = 0; goodIndex < goodElectrons.size(); ++goodIndex) {
			const pat::Electron electron = goodElectrons.at(goodIndex);
			double dR = deltaR(electron, looseElectron);
			overlaps = dR < 0.1;
		}
		if (!overlaps)
			cleanElectrons.push_back(looseElectron);
	}
	return cleanElectrons;
}

//define this as a plug-in
DEFINE_FWK_MODULE(TopSemiLeptonicEventFilter);
