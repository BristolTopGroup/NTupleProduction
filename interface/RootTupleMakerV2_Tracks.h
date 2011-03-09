#ifndef RootTupleMakerV2Tracks
#define RootTupleMakerV2Tracks

#include "FWCore/Framework/interface/EDProducer.h"

class RootTupleMakerV2_Tracks : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_Tracks(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const std::string     prefix,suffix;
};

#endif
