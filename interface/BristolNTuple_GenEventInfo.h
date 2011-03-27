#ifndef BristolNTupleGenEventInfo
#define BristolNTupleGenEventInfo

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_GenEventInfo : public edm::EDProducer {
 public:
  explicit BristolNTuple_GenEventInfo(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   genEvtInfoInputTag;
  const bool            storePDFWeights;
  const edm::InputTag   pdfWeightsInputTag;
  const std::string     prefix,suffix;
};

#endif
