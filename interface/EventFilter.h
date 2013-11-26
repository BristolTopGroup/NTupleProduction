#ifndef BristolEventFilter
#define BristolNTuplebeamSpot

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1.h"
#include <vector>

namespace Filters {
enum value {
	allEvents,
	passHBHENoiseFilter,
	passCSCBeamHaloFilter,
	passHCALLaserFilter,
	passECALDeadCellFilter,
	passECALDeadCellTriggerPrimitiveFilter,
	passTrackingFailureFilter,
	passEEBadSCFilter,
	passECALLaserCorrFilter,
	passTrackingPOGFilters,
	passScrapingVeto,
	passGoodPrimaryVertex,
	passElectronCuts,
	passMuonCuts,
	passJetCuts,
	NUMBER_OF_FILTERS
};

const std::string names[NUMBER_OF_FILTERS] = { "All Events", //
		"HBHENoiseFilter", //
		"CSCBeamHaloFilter", //
		"HCALLaserFilter", //
		"ECALDeadCellFilter", //
		"ECALDeadCellTriggerPrimitiveFilter", //
		"TrackingFailureFilter", //
		"EEBadSupercrystalFilter", //
		"ECALLaserCorrFilter", //
		"TrackingPOGFilters", //
		"ScrapingVeto", //
		"GoodPrimaryVertex", //
		"ElectronCuts", //
		"MuonCuts", //
		"JetCuts" };
}

class EventFilter: public edm::EDFilter {
public:
	explicit EventFilter(const edm::ParameterSet&);
	virtual ~EventFilter();
	static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
	virtual void beginJob();
	virtual bool filter(edm::Event&, const edm::EventSetup&);
	virtual void endJob();

	virtual bool beginRun(edm::Run&, edm::EventSetup const&);
	virtual bool endRun(edm::Run&, edm::EventSetup const&);
	virtual bool beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
	virtual bool endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);

	bool passesSelectionStep(edm::Event& event, Filters::value filter);
	bool passesFilter(edm::Event& event, edm::InputTag filter);

	bool passesCSCTightBeamHaloID(edm::Event& event);
	bool passesScrapingVeto(edm::Event& event);
	bool passesGoodPrimaryVertex(edm::Event& event);
	bool passesElectronCuts(edm::Event& event);
	bool passesMuonCuts(edm::Event& event);
	bool passesJetCuts(edm::Event& event);

	edm::InputTag hbheNoiseFilterInput_, hcalLaserFilterInput_, ecalDeadCellFilterInput_, ecalDeadCellTriggerPrimitiveFilterInput_,//
			trackingFailureFilterInput_, //
			eeBadSCFilterInput_, //
			ecalLaserCorrFilterInput_, //
			manystripclus53XInput_, //
			toomanystripclus53XInput_, //
			logErrorTooManyClustersInput_, //
			trkInput_, vertexInput_, //
			jetInput_, electronInput_, muonInput_;

	int minNVertices_, maxNVertices_, minNJets_, maxNJets_, minNElectrons_, maxNElectrons_, minNMuons_, maxNMuons_;

	double minJetPt_, maxAbsJetEta_, minElectronPt_, maxAbsElectronEta_, minMuonPt_, maxAbsMuonEta_;

	bool debug_, counteitherleptontype_, useTrackingFailureFilter_, useTrackingPOGFilters_, useOptionalMETFilters_;
	std::vector<int> eventCount_;

	TH1I* hCount;
};

#endif
