#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenParticles.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"


BristolNTuple_GenParticles::BristolNTuple_GenParticles(const edm::ParameterSet& iConfig) :
    inputTag(consumes< reco::GenParticleCollection > (iConfig.getParameter<edm::InputTag>("InputTag"))),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix")),
    maxSize (iConfig.getParameter<unsigned int> ("MaxSize"))
{
  produces <std::vector<double> > ( prefix + "Px" + suffix );
  produces <std::vector<double> > ( prefix + "Py" + suffix );
  produces <std::vector<double> > ( prefix + "Pz" + suffix );
  produces <std::vector<double> > ( prefix + "Energy" + suffix );
  produces <std::vector<double> > ( prefix + "Charge" + suffix );
  produces <std::vector<double> > ( prefix + "Mass" + suffix );
  produces <std::vector<int> >    ( prefix + "PdgId" + suffix );
  produces <std::vector<double> > ( prefix + "VX" + suffix );
  produces <std::vector<double> > ( prefix + "VY" + suffix );
  produces <std::vector<double> > ( prefix + "VZ" + suffix );
  produces <std::vector<int> >    ( prefix + "NumDaught" + suffix );
  produces <std::vector<int> >    ( prefix + "Status" + suffix );
  produces <std::vector<int> >    ( prefix + "MotherIndex" + suffix );
}

void BristolNTuple_GenParticles::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::auto_ptr < std::vector<double> > px(new std::vector<double>());
	std::auto_ptr < std::vector<double> > py(new std::vector<double>());
	std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
	std::auto_ptr < std::vector<double> > charge(new std::vector<double>());
	std::auto_ptr < std::vector<double> > mass(new std::vector<double>());
	std::auto_ptr < std::vector<int> > pdgId(new std::vector<int>());
	std::auto_ptr < std::vector<double> > vx(new std::vector<double>());
	std::auto_ptr < std::vector<double> > vy(new std::vector<double>());
	std::auto_ptr < std::vector<double> > vz(new std::vector<double>());
	std::auto_ptr < std::vector<int> > numDaught(new std::vector<int>());
	std::auto_ptr < std::vector<int> > status(new std::vector<int>());
	std::auto_ptr < std::vector<int> > motherIndex(new std::vector<int>());

	//-----------------------------------------------------------------
	if (!iEvent.isRealData()) {
		edm::Handle < reco::GenParticleCollection > genParticles;
		iEvent.getByToken(inputTag, genParticles);

		if (genParticles.isValid()) {
			// edm::LogInfo("BristolNTuple_GenParticlesInfo") << "Total # GenParticles: " << genParticles->size();

			for (reco::GenParticleCollection::const_iterator it = genParticles->begin(); it != genParticles->end();
					++it) {
				// exit from loop when you reach the required number of GenParticles
				if (px->size() >= maxSize)
					break;

				// fill in all the vectors
				px->push_back(it->px());
				py->push_back(it->py());
				pz->push_back(it->pz());
				energy->push_back(it->energy());
				pdgId->push_back(it->pdgId());
				vx->push_back(it->vx());
				vy->push_back(it->vy());
				vz->push_back(it->vz());
				numDaught->push_back(it->numberOfDaughters());
				status->push_back(it->status());
				charge->push_back(it->charge());
				mass->push_back(it->mass());

				int idx = -1;
				for (reco::GenParticleCollection::const_iterator mit = genParticles->begin();
						mit != genParticles->end(); ++mit) {
					if (it->mother() == &(*mit)) {
						idx = std::distance(genParticles->begin(), mit);
						break;
					}
				}
				motherIndex->push_back(idx);
			}
		} 
		// else {
		// 	edm::LogError("BristolNTuple_GenParticlesError") << "Error! Can't get the product " << inputTag;
		// }
	}
	//-----------------------------------------------------------------
	// put vectors in the event
	iEvent.put(px, prefix + "Px" + suffix);
	iEvent.put(py, prefix + "Py" + suffix);
	iEvent.put(pz, prefix + "Pz" + suffix);
	iEvent.put(energy, prefix + "Energy" + suffix);
	iEvent.put(charge, prefix + "Charge" + suffix);
	iEvent.put(mass, prefix + "Mass" + suffix);
	iEvent.put(pdgId, prefix + "PdgId" + suffix);
	iEvent.put(vx, prefix + "VX" + suffix);
	iEvent.put(vy, prefix + "VY" + suffix);
	iEvent.put(vz, prefix + "VZ" + suffix);
	iEvent.put(numDaught, prefix + "NumDaught" + suffix);
	iEvent.put(status, prefix + "Status" + suffix);
	iEvent.put(motherIndex, prefix + "MotherIndex" + suffix);
}
