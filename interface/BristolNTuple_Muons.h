#ifndef BristolNTupleMuonsExtra
#define BristolNTupleMuonsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_Muons : public edm::EDProducer {
 public:
  explicit BristolNTuple_Muons(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const std::string     muonID;
  const bool            beamSpotCorr;
  const bool storePFIsolation;
  const bool            useCocktailRefits;
  const edm::InputTag   vtxInputTag;
};

#endif
