#ifndef BristolNTuplePFJetsExtra
#define BristolNTuplePFJetsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_PFJets : public edm::EDProducer {
 public:
  explicit BristolNTuple_PFJets(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const double 			minJetPtToStore;
  const std::string jecUncPath;
  const bool readJECuncertainty, doVertexAssociation;
  const edm::InputTag   vtxInputTag;
  const bool isRealData;
};

#endif
