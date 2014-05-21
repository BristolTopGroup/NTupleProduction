#ifndef BristolNTupleGlobalEventVarsExtra
#define BristolNTupleGlobalEventVarsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Lepton.h"
#include "DataFormats/PatCandidates/interface/GenericParticle.h"
#include "DataFormats/PatCandidates/interface/Particle.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "TLorentzVector.h"



class BristolNTuple_GlobalEventVars : public edm::EDProducer {
 public:
  explicit BristolNTuple_GlobalEventVars(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::InputTag   jetInputTag;
  const edm::InputTag   leptonInputTag;
  const edm::InputTag   leptonIndexInputTag;
  const edm::InputTag   metInputTag;

  const std::string     prefix,suffix,channel;

  static double HT(const pat::JetCollection& );
  static double ST(const  pat::JetCollection&, const TLorentzVector&, const pat::MET&);
  static double M3(const pat::JetCollection&);
  static double M_bl( const pat::Jet*, const TLorentzVector&);
  static double angle_bl(const pat::Jet*, const TLorentzVector&);
  static double MT(const TLorentzVector&, const pat::MET&);
  static double WPT(const TLorentzVector&, const pat::MET&);

  static unsigned int getClosestBJet( const TLorentzVector&, const std::vector<const pat::Jet*>);


};

#endif
