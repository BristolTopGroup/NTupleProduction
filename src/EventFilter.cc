#include "BristolAnalysis/NTupleTools/interface/EventFilter.h"
// system include files
#include <memory>

// user include files

#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"

using namespace edm;
using namespace std;

EventFilter::EventFilter(const edm::ParameterSet& iConfig) :
		hcalNoiseInput_(iConfig.getParameter < edm::InputTag > ("HBHENoiseFilterInput")), //
		hcalLaserFilterInput_(iConfig.getParameter < edm::InputTag > ("HCALLaserFilterInput")), //
		ecalDeadCellFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALDeadCellFilterInput")), //
		ecalDeadCellTriggerPrimitiveFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALDeadCellTriggerPrimitiveFilterInput")), //
		trackingFailureFilterInput_(iConfig.getParameter < edm::InputTag > ("TrackingFailureFilterInput")), //
		eeBadSCFilterInput_(iConfig.getParameter < edm::InputTag > ("EEBadSCFilterInput")), //
		ecalLaserCorrFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALLaserCorrFilterInput")), //
		manystripclus53XInput_(iConfig.getParameter < edm::InputTag > ("manystripclus53XInput")), //
		toomanystripclus53XInput_(iConfig.getParameter < edm::InputTag > ("toomanystripclus53XInput")), //
		logErrorTooManyClustersInput_(iConfig.getParameter < edm::InputTag > ("logErrorTooManyClustersInput")), //
		trkInput_(iConfig.getParameter < edm::InputTag > ("TracksInput")), //
		vertexInput_(iConfig.getParameter < edm::InputTag > ("VertexInput")), //
		jetInput_(iConfig.getParameter < edm::InputTag > ("jetInput")), //
		electronInput_(iConfig.getParameter < edm::InputTag > ("electronInput")), //
		muonInput_(iConfig.getParameter < edm::InputTag > ("muonInput")), //
		minNVertices_(iConfig.getParameter<int>("minNVertices")), //
		maxNVertices_(iConfig.getParameter<int>("maxNVertices")), //
		minNJets_(iConfig.getParameter<int>("minNJets")), //
		maxNJets_(iConfig.getParameter<int>("maxNJets")), //
		minNElectrons_(iConfig.getParameter<int>("minNElectrons")), //
		maxNElectrons_(iConfig.getParameter<int>("maxNElectrons")), //
		minNMuons_(iConfig.getParameter<int>("minNMuons")), //
		maxNMuons_(iConfig.getParameter<int>("maxNMuons")), //
		minJetPt_(iConfig.getParameter<double>("minJetPt")), //
		maxAbsJetEta_(iConfig.getParameter<double>("maxAbsJetEta")), //
		minElectronPt_(iConfig.getParameter<double>("minElectronPt")), //
		maxAbsElectronEta_(iConfig.getParameter<double>("maxAbsElectronEta")), //
		minMuonPt_(iConfig.getParameter<double>("minMuonPt")), //
		maxAbsMuonEta_(iConfig.getParameter<double>("maxAbsMuonEta")), //
		debug_(iConfig.getParameter<bool>("debug")), //
		counteitherleptontype_(iConfig.getParameter<bool>("counteitherleptontype")), //
		useTrackingFailureFilter_(iConfig.getParameter<bool>("useTrackingFailureFilter")), //
		useTrackingPOGFilters_(iConfig.getParameter<bool>("useTrackingPOGFilters")), //
		useOptionalMETFilters_(iConfig.getParameter<bool>("useOptionalMETFilters")),//
		eventCount_(), //
		hCount() {

	edm::Service < TFileService > histServ;

	hCount = histServ->make < TH1I
			> ("EventCounter", "Event Counter", Filters::NUMBER_OF_FILTERS, -0.5, Filters::NUMBER_OF_FILTERS - 0.5);

	eventCount_.resize(Filters::NUMBER_OF_FILTERS);
	for (unsigned int index = 0; index < Filters::NUMBER_OF_FILTERS; ++index) {
		unsigned int bin = index + 1;
		eventCount_.at(index) = 0;
		std::string filterName = Filters::names[index];
		hCount->GetXaxis()->SetBinLabel(bin, filterName.c_str());
	}
}

EventFilter::~EventFilter() {

}

bool EventFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	for (unsigned int index = 0; index < Filters::NUMBER_OF_FILTERS; ++index) {
		bool passes = passesSelectionStep(iEvent, (Filters::value) index);
		if (passes)
			++eventCount_.at(index);
		else {
			//will not use the filter decision but will still save the outcome
			if(useOptionalMETFilters_ == false && (index >= Filters::passCSCBeamHaloFilter && index <= Filters::passTrackingPOGFilters))
				continue;

			return false;
		}
	}

	if (debug_)
		cout << "Event PASSED!" << endl;
	return true;
}

bool EventFilter::passesSelectionStep(edm::Event& event, Filters::value filter) {
	switch (filter) {
	case Filters::allEvents:
		return true;
	case Filters::passHBHENoiseFilter:
		return passesFilter(event, hcalNoiseInput_);
	case Filters::passCSCBeamHaloFilter:
		return passesCSCTightBeamHaloID(event);
	case Filters::passHCALLaserFilter:
		return passesFilter(event, hcalLaserFilterInput_);
	case Filters::passECALDeadCellFilter:
		return passesFilter(event, ecalDeadCellFilterInput_);
	case Filters::passECALDeadCellTriggerPrimitiveFilter:
		return passesFilter(event, ecalDeadCellTriggerPrimitiveFilterInput_);	
	case Filters::passTrackingFailureFilter:
		if (useTrackingFailureFilter_)
			return passesFilter(event, trackingFailureFilterInput_);
		else
			return true;
	case Filters::passEEBadSCFilter:
		return passesFilter(event, eeBadSCFilterInput_);
	case Filters::passECALLaserCorrFilter:
		return passesFilter(event, ecalLaserCorrFilterInput_);
	case Filters::passTrackingPOGFilters:
		if (useTrackingPOGFilters_)
			return !passesFilter(event, manystripclus53XInput_) && !passesFilter(event, toomanystripclus53XInput_) && !passesFilter(event, logErrorTooManyClustersInput_);
		else
			return true;
	case Filters::passScrapingVeto:
		return passesScrapingVeto(event);
	case Filters::passGoodPrimaryVertex:
		return passesGoodPrimaryVertex(event);
	case Filters::passElectronCuts:
		if (counteitherleptontype_)
			return passesElectronCuts(event) || passesMuonCuts(event);

		return passesElectronCuts(event);
	case Filters::passMuonCuts:
		if (counteitherleptontype_)
			return passesElectronCuts(event) || passesMuonCuts(event);

		return passesMuonCuts(event);
	case Filters::passJetCuts:
		return passesJetCuts(event);
	default:
		return false;
	}
}

bool EventFilter::passesFilter(edm::Event& event, edm::InputTag filter) {
	bool result(false);
	edm::Handle<bool> filterResult;
	event.getByLabel(filter, filterResult);
	if (filterResult.isValid()) {
		edm::LogInfo("EventFilter") << "Successfully obtained " << filter;
		result = *filterResult;
	} else
		edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product " << filter;

	return result;
}

bool EventFilter::passesCSCTightBeamHaloID(edm::Event& event) {
	bool result(false);
	edm::Handle < reco::BeamHaloSummary > TheBeamHaloSummary;
	event.getByLabel("BeamHaloSummary", TheBeamHaloSummary);
	if (TheBeamHaloSummary.isValid()) {
		edm::LogInfo("EventFilter") << "Successfully obtained BeamHaloSummary";
		const reco::BeamHaloSummary TheSummary = (*TheBeamHaloSummary.product());
		//event is NOT identified as beam halo
		result = !TheSummary.CSCTightHaloId();
	} else
		edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product BeamHaloSummary";

	return result;
}

bool EventFilter::passesScrapingVeto(edm::Event& event) {
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

bool EventFilter::passesGoodPrimaryVertex(edm::Event& event) {
	bool result(false);
	edm::Handle < reco::VertexCollection > primaryVertices;
	event.getByLabel(vertexInput_, primaryVertices);
	if (primaryVertices.isValid()) {
		int nVertices = primaryVertices->size();
		edm::LogInfo("EventFilter") << "Total # Primary Vertices: " << nVertices;
		if (nVertices >= minNVertices_)
			result = true;
		if (maxNVertices_ > -1 && nVertices > maxNVertices_)
			result = false;
	} else
		edm::LogError("EventFilterError") << "Error! Can't get the product " << vertexInput_;
	return result;
}

bool EventFilter::passesElectronCuts(edm::Event& event) {
	bool result(false);
	int nelectrons(0);

	edm::Handle < edm::View<reco::Candidate> > electrons;
	event.getByLabel(electronInput_, electrons);

	for (edm::View<reco::Candidate>::const_iterator it = electrons->begin(); it != electrons->end(); ++it) {
		if (debug_) {
			cout << "Electron:" << endl;
			cout << "pT: " << it->pt() << " eta: " << it->eta() << " phi: " << it->phi() << endl;
		}

		if (it->pt() > minElectronPt_ && fabs(it->eta()) < maxAbsElectronEta_) {
			++nelectrons;
		}
	}

	if (debug_)
		cout << "# Electrons = " << nelectrons << endl;

	if (nelectrons >= minNElectrons_)
		result = true;
	if (maxNElectrons_ > -1 && nelectrons > maxNElectrons_)
		result = false;

	return result;
}

bool EventFilter::passesMuonCuts(edm::Event& event) {
	bool result(false);
	int nmuons(0);

	edm::Handle < edm::View<reco::Candidate> > muons;
	event.getByLabel(muonInput_, muons);

	for (edm::View<reco::Candidate>::const_iterator it = muons->begin(); it != muons->end(); ++it) {
		if (debug_) {
			cout << "Muon:" << endl;
			cout << "pT: " << it->pt() << " eta: " << it->eta() << " phi: " << it->phi() << endl;
		}

		if (it->pt() > minMuonPt_ && fabs(it->eta()) < maxAbsMuonEta_) {
			++nmuons;
		}
	}

	if (debug_)
		cout << "# Muons = " << nmuons << endl;

	if (nmuons >= minNMuons_)
		result = true;
	if (maxNMuons_ > -1 && nmuons > maxNMuons_)
		result = false;
	return result;
}

bool EventFilter::passesJetCuts(edm::Event& event) {
	bool result(false);

	edm::Handle < edm::View<reco::Candidate> > jets;
	event.getByLabel(jetInput_, jets);

	int njets(0);

	for (edm::View<reco::Candidate>::const_iterator it = jets->begin(); it != jets->end(); ++it) {
		if (debug_) {
			cout << "Jet:" << endl;
			cout << "pT: " << it->pt() << " eta: " << it->eta() << " phi: " << it->phi() << endl;
		}
		if (it->pt() > minJetPt_ && fabs(it->eta()) < maxAbsJetEta_)
			++njets;

	}

	if (debug_)
		cout << "# Jets = " << njets << endl;

	if (njets >= minNJets_)
		result = true;
	if (maxNJets_ > -1 && njets > maxNJets_)
		result = false;
	return result;
}

// ------------ method called once each job just before starting event loop  ------------
void EventFilter::beginJob() {
}

// ------------ method called once each job just after ending the event loop  ------------
void EventFilter::endJob() {
	if(useOptionalMETFilters_ == false){
		cout << "Not using the optional MET filters!" << endl;
		cout << "Events won't fail these filters, but the result will be recorded." << endl;
	}

	for (unsigned int index = 0; index < eventCount_.size(); ++index) {
		unsigned int bin = index + 1;
		unsigned int nEvents = eventCount_.at(index);
		std::string filterName = Filters::names[index];
		hCount->SetBinContent(bin, nEvents);
		cout << filterName << " = " << nEvents << endl;
	}
}

// ------------ method called when starting to processes a run  ------------
bool EventFilter::beginRun(edm::Run&, edm::EventSetup const&) {
	return true;
}

// ------------ method called when ending the processing of a run  ------------
bool EventFilter::endRun(edm::Run&, edm::EventSetup const&) {
	return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool EventFilter::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
	return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool EventFilter::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
	return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void EventFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.add < edm::InputTag > ("HBHENoiseFilterInput", edm::InputTag("HBHENoiseFilterResultProducer", "HBHENoiseFilterResult"));
	desc.add < edm::InputTag > ("HCALLaserFilterInput", edm::InputTag("HcalLaserEventFilter"));
	desc.add < edm::InputTag > ("ECALDeadCellFilterInput", edm::InputTag("EcalDeadCellBoundaryEnergyFilter"));
	desc.add < edm::InputTag > ("ECALDeadCellTriggerPrimitiveFilterInput", edm::InputTag("EcalDeadCellTriggerPrimitiveFilter"));
	desc.add < edm::InputTag > ("TrackingFailureFilterInput", edm::InputTag("trackingFailureFilter"));
	desc.add < edm::InputTag > ("EEBadSCFilterInput", edm::InputTag("eeBadScFilter"));
	desc.add < edm::InputTag > ("ECALLaserCorrFilterInput", edm::InputTag("ecalLaserCorrFilter"));
	desc.add < edm::InputTag > ("manystripclus53XInput", edm::InputTag("manystripclus53X"));
	desc.add < edm::InputTag > ("toomanystripclus53XInput", edm::InputTag("toomanystripclus53X"));
	desc.add < edm::InputTag > ("logErrorTooManyClustersInput", edm::InputTag("logErrorTooManyClusters"));
	desc.add < edm::InputTag > ("TracksInput", edm::InputTag("generalTracks"));

	desc.add < edm::InputTag > ("VertexInput", edm::InputTag("goodOfflinePrimaryVertices"));
	desc.add < edm::InputTag > ("jetInput", edm::InputTag("selectedPatJets"));
	desc.add < edm::InputTag > ("electronInput", edm::InputTag("selectedPatElectrons"));
	desc.add < edm::InputTag > ("muonInput", edm::InputTag("selectedPatMuons"));

	desc.add<int>("minNVertices", 1);
	desc.add<int>("maxNVertices", -1);

	desc.add<int>("minNJets", -1);
	desc.add<int>("maxNJets", -1);

	desc.add<int>("minNElectrons", -1);
	desc.add<int>("maxNElectrons", -1);

	desc.add<int>("minNMuons", -1);
	desc.add<int>("maxNMuons", -1);

	desc.add<double>("minJetPt", -1);
	desc.add<double>("maxAbsJetEta", -1);

	desc.add<double>("minElectronPt", -1);
	desc.add<double>("maxAbsElectronEta", -1);

	desc.add<double>("minMuonPt", -1);
	desc.add<double>("maxAbsMuonEta", -1);

	desc.add<bool>("debug", false);
	desc.add<bool>("counteitherleptontype", true);
	desc.add<bool>("useTrackingFailureFilter", true);
	desc.add<bool>("useTrackingPOGFilters", true);
	desc.add<bool>("useOptionalMETFilters", false);
	descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE (EventFilter);
