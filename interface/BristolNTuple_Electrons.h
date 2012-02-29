#ifndef BristolNTupleElectronsExtra
#define BristolNTupleElectronsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_Electrons : public edm::EDProducer {
 public:
  explicit BristolNTuple_Electrons(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   trkInputTag, dcsInputTag, inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const bool storePFIsolation_, debugRelease_;
  const edm::InputTag  vtxInputTag, beamSpotInputTag, conversionsInputTag, likelihoodInputTag;
};

#endif
