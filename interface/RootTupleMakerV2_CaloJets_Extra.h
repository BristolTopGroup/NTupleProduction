#ifndef RootTupleMakerV2CaloJetsExtra
#define RootTupleMakerV2CaloJetsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"


class RootTupleMakerV2_CaloJets_Extra : public edm::EDProducer {
 public:
  explicit RootTupleMakerV2_CaloJets_Extra(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
//  const std::string     jecUncPath;
//  const bool            applyResJEC;
//  const std::string     resJEC;
};

#endif
