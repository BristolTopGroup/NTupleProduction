#ifndef BristolNTupleMETExtra
#define BristolNTupleMETExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_MET : public edm::EDProducer {
 public:
  explicit BristolNTuple_MET(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const bool storeMETUncertainties_;
  const unsigned int nMETUncertainties_;
  const std::string     prefix,suffix;
};

#endif
