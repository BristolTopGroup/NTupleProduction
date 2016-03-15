#ifndef BristolNTupleVertex
#define BristolNTupleVertex

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class BristolNTuple_Vertex : public edm::EDProducer {
 public:
  explicit BristolNTuple_Vertex(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT<std::vector<reco::Vertex>> inputTag;
  const std::string     prefix,suffix;
};

#endif
