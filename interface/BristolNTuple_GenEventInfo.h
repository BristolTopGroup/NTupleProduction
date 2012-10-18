#ifndef BristolNTupleGenEventInfo
#define BristolNTupleGenEventInfo

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <boost/array.hpp>

class BristolNTuple_GenEventInfo: public edm::EDProducer {
public:
	explicit BristolNTuple_GenEventInfo(const edm::ParameterSet&);

private:
	void initLumiWeights();
	void produce(edm::Event &, const edm::EventSetup &);
	const edm::InputTag genEvtInfoInputTag;
	const edm::InputTag puWeightsInputTag_;
	const bool storePDFWeights_;//, isFall11MC_;
	const edm::InputTag pdfWeightsInputTag_;
	const edm::InputTag pileupInfoSrc_;
	const std::string prefix_, suffix_;
};

#endif
