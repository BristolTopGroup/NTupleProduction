#ifndef RootTupleMakerV2METExtra
#define RootTupleMakerV2METExtra

#include "FWCore/Framework/interface/EDProducer.h"

class RootTupleMakerV2_MET_Extra : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_MET_Extra(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;
  const bool            store_uncorrected_MET;
};

#endif
