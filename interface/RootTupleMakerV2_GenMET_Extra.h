#ifndef RootTupleMakerV2GenMETExtra
#define RootTupleMakerV2GenMETExtra

#include "FWCore/Framework/interface/EDProducer.h"

class RootTupleMakerV2_GenMET_Extra : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_GenMET_Extra(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;
};

#endif
