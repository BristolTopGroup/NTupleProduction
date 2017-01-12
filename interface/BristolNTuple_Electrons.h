#ifndef BristolNTupleElectronsExtra
#define BristolNTupleElectronsExtra

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

class BristolNTuple_Electrons: public edm::EDProducer {
public:
  explicit BristolNTuple_Electrons(const edm::ParameterSet&);

private:
  void produce(edm::Event &, const edm::EventSetup &);

  const edm::EDGetToken inputTag;

  const std::string prefix, suffix;
  const unsigned int maxSize;
  const double minPtToStore_;
  const bool storePFIsolation_, debugRelease_;

};

#endif
