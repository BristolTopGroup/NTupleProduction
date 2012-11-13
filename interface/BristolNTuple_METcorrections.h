#ifndef BristolNTupleMETcorrectionsExtra
#define BristolNTupleMETcorrectionsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include <TFormula.h>
#include <string>

class BristolNTuple_METcorrections : public edm::EDProducer {
 public:
  explicit BristolNTuple_METcorrections(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   inputTag;
  const std::string     prefix,suffix;

};

#endif
