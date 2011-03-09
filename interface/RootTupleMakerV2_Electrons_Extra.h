#ifndef RootTupleMakerV2ElectronsExtra
#define RootTupleMakerV2ElectronsExtra

#include "FWCore/Framework/interface/EDProducer.h"

class RootTupleMakerV2_Electrons_Extra : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_Electrons_Extra(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag, inputTagPVWithBS, inputTagBS;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const bool storePFIsolation;
};

#endif
