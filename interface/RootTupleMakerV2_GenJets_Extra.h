#ifndef RootTupleMakerV2GenJetsExtra
#define RootTupleMakerV2GenJetsExtra

#include "FWCore/Framework/interface/EDProducer.h"

class RootTupleMakerV2_GenJets_Extra : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_GenJets_Extra(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
};

#endif
