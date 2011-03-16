#ifndef RootTupleMakerV2MuonsExtra
#define RootTupleMakerV2MuonsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class RootTupleMakerV2_Muons_Extra : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_Muons_Extra(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;//, inputTagPVWithBS, inputTagBS;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const bool storePFIsolation;
};

#endif
