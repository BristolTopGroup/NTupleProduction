#ifndef RootTupleMakerV2BeamSpot
#define RootTupleMakerV2beamSpot

#include "FWCore/Framework/interface/EDProducer.h"

class RootTupleMakerV2_BeamSpot : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_BeamSpot(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const std::string     prefix,suffix;
};

#endif
