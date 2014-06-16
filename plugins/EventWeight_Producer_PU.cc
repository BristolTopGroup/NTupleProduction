#include "EventWeight_Producer_PU.h"
#include "DataFormats/Common/interface/View.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "FWCore/Framework/interface/MakerMacros.h"

// =============
//  Constructor
// =============

EventWeight_Producer_PU::EventWeight_Producer_PU(const edm::ParameterSet& cfg) :
		inTag_PUSource(cfg.getParameter < edm::InputTag > ("PUSource")), //
		inTag_WeightName(cfg.getParameter < std::string > ("WeightName")), //
		inTag_MCSampleTag(cfg.getParameter < std::string > ("MCSampleTag")), //
		inTag_MCSampleFile(cfg.getParameter < edm::FileInPath > ("MCSampleFile")), //
		inTag_MCSampleHistoName(cfg.getParameter < std::string > ("MCSampleHistoName")), //
		inTag_DataFile(cfg.getParameter < edm::FileInPath > ("DataFile")), //
		inTag_DataHistoName(cfg.getParameter < std::string > ("DataHistoName")) {

	error_code = 0;

	if (inTag_MCSampleTag == "Fall11" || inTag_MCSampleTag == "Summer12" || inTag_MCSampleTag == "Summer11Leg") {

		LumiWeights_ = edm::LumiReWeighting(inTag_MCSampleFile.fullPath(), inTag_DataFile.fullPath(),
				inTag_MCSampleHistoName, inTag_DataHistoName);
	} else {

		std::cout << " ERROR: Non-valid tag for MC sample, all event weights will be 1. " << std::endl;
		error_code = -1;
	}

	produces<double>();
}

// =============
//  Destructor
// =============

EventWeight_Producer_PU::~EventWeight_Producer_PU() {
}

// =======================================================
//  Calculate and assign event weights for PU reweighting
// =======================================================

void EventWeight_Producer_PU::produce(edm::Event& evt, const edm::EventSetup& setup) {

//  std::auto_ptr<double> EventWeight_Producer_PU(new double); 

	if (error_code != 0 || evt.isRealData())
		wght_ = 1;
	else {

		edm::Handle < edm::View<PileupSummaryInfo> > pPUInfo;
		evt.getByLabel(inTag_PUSource, pPUInfo);

		edm::View<PileupSummaryInfo>::const_iterator iterPU;

		// default values to allow for tracing errors

		wght_ = -1;

		int nvtx = -1;

		for (iterPU = pPUInfo->begin(); iterPU != pPUInfo->end(); ++iterPU) // vector size is 3
				{
			int BX = iterPU->getBunchCrossing(); // -1: previous BX, 0: current BX,  1: next BX

			if (inTag_MCSampleTag == "Fall11" || inTag_MCSampleTag == "Summer12" || inTag_MCSampleTag == "Summer11Leg") {
				if (BX == 0)
					nvtx = iterPU->getTrueNumInteractions();
			}
		}

		if (inTag_MCSampleTag == "Fall11" || inTag_MCSampleTag == "Summer12" || inTag_MCSampleTag == "Summer11Leg")
			wght_ = LumiWeights_.weight(nvtx);
	}
	std::auto_ptr<double> eventWeightPUProduct(new double(wght_));
	evt.put(eventWeightPUProduct);
}

DEFINE_FWK_MODULE (EventWeight_Producer_PU);

