#ifndef BristolNTupleBeamSpot
#define BristolNTuplebeamSpot

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


class BristolNTuple_BeamSpot : public edm::EDProducer {
 public:
  explicit BristolNTuple_BeamSpot(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const std::string     prefix,suffix;
};

#endif
