#ifndef BristolNTupleTracks
#define BristolNTupleTracks

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"


class BristolNTuple_Tracks : public edm::EDProducer {
 public:
  explicit BristolNTuple_Tracks(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const std::string     prefix,suffix;
};

#endif
