#ifndef BristolNTuplePFJetsExtra
#define BristolNTuplePFJetsExtra

#include <string>
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondFormats/BTauObjects/interface/BTagCalibrationReader.h"

class BristolNTuple_PFJets : public edm::EDProducer {

 public:
  explicit BristolNTuple_PFJets(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT<std::vector<pat::Jet>> inputTag;
  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const double      minJetPtToStore;
  const std::string jecUncPath;
  const bool readJEC;
  const std::string jetCorrectionService;
  const bool readJECuncertainty, doVertexAssociation;
  const edm::EDGetTokenT<std::vector<reco::Vertex>> vtxInputTag;
  const bool isRealData;

  const std::string btagCalibrationFile_;
  BTagCalibration calib;
  BTagCalibrationReader medium_reader_bc, medium_reader_bc_up, medium_reader_bc_down;
  BTagCalibrationReader medium_reader_udsg, medium_reader_udsg_up, medium_reader_udsg_down;
  BTagCalibrationReader tight_reader_bc, tight_reader_bc_up, tight_reader_bc_down;
  BTagCalibrationReader tight_reader_udsg, tight_reader_udsg_up, tight_reader_udsg_down;

  double returnBTagSF(std::vector<pat::Jet>::const_iterator jet, BTagCalibrationReader reader, uint bTagEntryJetFlavour);
};

#endif
