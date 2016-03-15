#ifndef EventWeight_Producer_PU_h
#define EventWeight_Producer_PU_h
/**
 * Original from UserCode/Bromo/TopAnalysis/TopUtils
 **/

#include <memory>
#include <string>
#include <iostream>

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Common/interface/View.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

class EventWeight_Producer_PU: public edm::EDProducer {

public:
	explicit EventWeight_Producer_PU(const edm::ParameterSet&);
	~EventWeight_Producer_PU();

private:

	int error_code;

	virtual void produce(edm::Event&, const edm::EventSetup&);

	edm::EDGetToken inTag_PUSource;
	std::string inTag_WeightName;

	std::string inTag_MCSampleTag;

	edm::FileInPath inTag_MCSampleFile;
	std::string inTag_MCSampleHistoName;
	edm::FileInPath inTag_DataFile;
	std::string inTag_DataHistoName;

	edm::LumiReWeighting LumiWeights_;

	double wght_;
};

#endif
