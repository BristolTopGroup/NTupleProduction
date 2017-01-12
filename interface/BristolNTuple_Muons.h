#ifndef BristolNTupleMuonsExtra
#define BristolNTupleMuonsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

class BristolNTuple_Muons : public edm::EDProducer {
 public:
  explicit BristolNTuple_Muons(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT<std::vector<pat::Muon>> inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const double minPtToStore_;
  const std::string     muonID;
  const bool            beamSpotCorr;
  const bool storePFIsolation;
  const edm::EDGetTokenT<std::vector<reco::Vertex>> vtxInputTag;
  const edm::EDGetTokenT<reco::BeamSpot> beamSpotInputTag;
};

#endif
