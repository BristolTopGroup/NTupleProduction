#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_PFJets.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/ESHandle.h"

using namespace std;

BristolNTuple_PFJets::BristolNTuple_PFJets(const edm::ParameterSet& iConfig) :
  		inputTag(consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("InputTag"))),	
  		eventJetInputTag(consumes< edm::View< reco::PFJet > >(iConfig.getParameter<edm::InputTag>("EventJetTag"))),			
  		njettiness1InputTag(consumes< edm::ValueMap< float > >(iConfig.getParameter<edm::InputTag>("NJettiness1Tag"))),			
  		njettiness2InputTag(consumes< edm::ValueMap< float > >(iConfig.getParameter<edm::InputTag>("NJettiness2Tag"))),			
  		njettiness3InputTag(consumes< edm::ValueMap< float > >(iConfig.getParameter<edm::InputTag>("NJettiness3Tag"))),			
  		njettiness4InputTag(consumes< edm::ValueMap< float > >(iConfig.getParameter<edm::InputTag>("NJettiness4Tag"))),			
  		njettiness5InputTag(consumes< edm::ValueMap< float > >(iConfig.getParameter<edm::InputTag>("NJettiness5Tag"))),			
  		njettiness6InputTag(consumes< edm::ValueMap< float > >(iConfig.getParameter<edm::InputTag>("NJettiness6Tag"))),			
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")), //
		maxSize(iConfig.getParameter<unsigned int>("MaxSize")), //
		minJetPtToStore(iConfig.getParameter<double>("minJetPtToStore")), //
		readJEC(iConfig.getParameter < bool > ("ReadJEC")), //
		doVertexAssociation(iConfig.getParameter<bool>("DoVertexAssociation")), //
		isRealData(iConfig.getParameter<bool>("isRealData")) {
	//kinematic variables
	produces < std::vector<double> > (prefix + "Px" + suffix);
	produces < std::vector<double> > (prefix + "Py" + suffix);
	produces < std::vector<double> > (prefix + "Pz" + suffix);
	produces < std::vector<double> > (prefix + "Energy" + suffix);
	//kinematic variables before corrections
	produces < std::vector<double> > (prefix + "PxRAW" + suffix);
	produces < std::vector<double> > (prefix + "PyRAW" + suffix);
	produces < std::vector<double> > (prefix + "PzRAW" + suffix);
	produces < std::vector<double> > (prefix + "EnergyRAW" + suffix);
	// extra kinematic variables for easier debugging
	produces < std::vector<double> > (prefix + "Pt" + suffix);
	produces < std::vector<double> > (prefix + "Eta" + suffix);
	produces < std::vector<double> > (prefix + "Phi" + suffix);
	//extra properties
	produces < std::vector<double> > (prefix + "Charge" + suffix);
	produces < std::vector<double> > (prefix + "Mass" + suffix);
	produces < std::vector<int> > (prefix + "PartonFlavour" + suffix);
	produces < std::vector<int> > (prefix + "HadronFlavour" + suffix);
	//generated jet properties
    if (!isRealData) {
        produces < std::vector<double> > (prefix + "GenJet.Energy" + suffix);
	    produces < std::vector<double> > (prefix + "GenJet.Pt" + suffix);
	    produces < std::vector<double> > (prefix + "GenJet.Px" + suffix);
	    produces < std::vector<double> > (prefix + "GenJet.Py" + suffix);
	    produces < std::vector<double> > (prefix + "GenJet.Pz" + suffix);
	    produces < std::vector<double> > (prefix + "GenJet.Eta" + suffix);
	    produces < std::vector<double> > (prefix + "GenJet.Phi" + suffix);

        produces < std::vector<double> > (prefix + "GenParton.Energy" + suffix);
	    produces < std::vector<double> > (prefix + "GenParton.Pt" + suffix);
	    produces < std::vector<double> > (prefix + "GenParton.Px" + suffix);
	    produces < std::vector<double> > (prefix + "GenParton.Py" + suffix);
	    produces < std::vector<double> > (prefix + "GenParton.Pz" + suffix);
	    produces < std::vector<double> > (prefix + "GenParton.Eta" + suffix);
	    produces < std::vector<double> > (prefix + "GenParton.Phi" + suffix);
	    produces < std::vector<int> > (prefix + "GenParton.PdgId" + suffix);
    }
	//jet energy correction and uncertainties
    produces < std::vector<double> > (prefix + "JEC" + suffix);
	produces < std::vector<double> > (prefix + "JECUnc" + suffix);
	produces < std::vector<double> > (prefix + "L2L3ResJEC" + suffix);
	produces < std::vector<double> > (prefix + "L3AbsJEC" + suffix);
	produces < std::vector<double> > (prefix + "L2RelJEC" + suffix);
	produces < std::vector<double> > (prefix + "L1OffJEC" + suffix);
	//jet ID variables
	produces < std::vector<double> > (prefix + "ChargedEmEnergyFraction" + suffix);
	produces < std::vector<double> > (prefix + "ChargedHadronEnergyFraction" + suffix);
	produces < std::vector<double> > (prefix + "ChargedMuEnergyFraction" + suffix);
	produces < std::vector<double> > (prefix + "ElectronEnergyFraction" + suffix);
	produces < std::vector<double> > (prefix + "MuonEnergyFraction" + suffix);
	produces < std::vector<double> > (prefix + "NeutralEmEnergyFraction" + suffix);
	produces < std::vector<double> > (prefix + "NeutralHadronEnergyFraction" + suffix);
	produces < std::vector<double> > (prefix + "PhotonEnergyFraction" + suffix);
	produces < std::vector<int> > (prefix + "ChargedHadronMultiplicity" + suffix);
	produces < std::vector<int> > (prefix + "ChargedMultiplicity" + suffix);
	produces < std::vector<int> > (prefix + "ElectronMultiplicity" + suffix);
	produces < std::vector<int> > (prefix + "MuonMultiplicity" + suffix);
	produces < std::vector<int> > (prefix + "NeutralHadronMultiplicity" + suffix);
	produces < std::vector<int> > (prefix + "NeutralMultiplicity" + suffix);
	produces < std::vector<int> > (prefix + "PhotonMultiplicity" + suffix);
	produces < std::vector<int> > (prefix + "NConstituents" + suffix);
	produces < std::vector<double> > (prefix + "ChargedEmEnergyFractionRAW" + suffix);
	produces < std::vector<double> > (prefix + "ChargedHadronEnergyFractionRAW" + suffix);
	produces < std::vector<double> > (prefix + "NeutralEmEnergyFractionRAW" + suffix);
	produces < std::vector<double> > (prefix + "NeutralHadronEnergyFractionRAW" + suffix);
	produces < std::vector<int> > (prefix + "PassLooseID" + suffix);
	produces < std::vector<int> > (prefix + "PassTightID" + suffix);
	//b-tagging information
	produces < std::vector<double> > (prefix + "combinedInclusiveSecondaryVertexV2BJetTags" + suffix);
	produces < std::vector<bool> > (prefix + "passesLooseCSV" + suffix);
	produces < std::vector<bool> > (prefix + "passesMediumCSV" + suffix);
	produces < std::vector<bool> > (prefix + "passesTightCSV" + suffix);
	produces < std::vector<double> > (prefix + "mediumBTagSF" + suffix);
	produces < std::vector<double> > (prefix + "mediumBTagSFUp" + suffix);
	produces < std::vector<double> > (prefix + "mediumBTagSFDown" + suffix);
	produces < std::vector<double> > (prefix + "tightBTagSF" + suffix);
	produces < std::vector<double> > (prefix + "tightBTagSFUp" + suffix);
	produces < std::vector<double> > (prefix + "tightBTagSFDown" + suffix);
	// JER information
	produces < std::vector<double> > (prefix + "jer" + suffix);
	produces < std::vector<double> > (prefix + "jerSF" + suffix);
	produces < std::vector<double> > (prefix + "jerSFUp" + suffix);
	produces < std::vector<double> > (prefix + "jerSFDown" + suffix);

	produces < float > (prefix + "tau1" + suffix);
	produces < float > (prefix + "tau2" + suffix);
	produces < float > (prefix + "tau3" + suffix);
	produces < float > (prefix + "tau4" + suffix);
	produces < float > (prefix + "tau5" + suffix);
	produces < float > (prefix + "tau6" + suffix);

	//jet-vertex association
	if (doVertexAssociation) {
		produces < std::vector<double> > (prefix + "BestVertexTrackAssociationFactor" + suffix);
		produces < std::vector<int> > (prefix + "BestVertexTrackAssociationIndex" + suffix);
		produces < std::vector<double> > (prefix + "ClosestVertexWeighted3DSeparation" + suffix);
		produces < std::vector<double> > (prefix + "ClosestVertexWeightedXYSeparation" + suffix);
		produces < std::vector<double> > (prefix + "ClosestVertexWeightedZSeparation" + suffix);
		produces < std::vector<int> > (prefix + "ClosestVertex3DIndex" + suffix);
		produces < std::vector<int> > (prefix + "ClosestVertexXYIndex" + suffix);
		produces < std::vector<int> > (prefix + "ClosestVertexZIndex" + suffix);
	}

}

void BristolNTuple_PFJets::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	//kinematic variables
	std::auto_ptr < std::vector<double> > px(new std::vector<double>());
	std::auto_ptr < std::vector<double> > py(new std::vector<double>());
	std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
	//kinematic variables before corrections
	std::auto_ptr < std::vector<double> > px_raw(new std::vector<double>());
	std::auto_ptr < std::vector<double> > py_raw(new std::vector<double>());
	std::auto_ptr < std::vector<double> > pz_raw(new std::vector<double>());
	std::auto_ptr < std::vector<double> > energy_raw(new std::vector<double>());
	// extra kinematic variables for easier debugging
  	std::auto_ptr<std::vector<double> > pt_store(new std::vector<double>());
  	std::auto_ptr<std::vector<double> > eta_store(new std::vector<double>());
  	std::auto_ptr<std::vector<double> > phi_store(new std::vector<double>());
	//extra properties
	std::auto_ptr < std::vector<double> > charge(new std::vector<double>());
	std::auto_ptr < std::vector<double> > mass(new std::vector<double>());
	std::auto_ptr < std::vector<int> > partonFlavour(new std::vector<int>());
	std::auto_ptr < std::vector<int> > hadronFlavour(new std::vector<int>());
	//generated jet properties
	std::auto_ptr < std::vector<double> > genJet_energy(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genJet_pt(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genJet_px(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genJet_py(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genJet_pz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genJet_eta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genJet_phi(new std::vector<double>());
	//Matched parton properties
	std::auto_ptr < std::vector<double> > genParton_energy(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genParton_pt(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genParton_px(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genParton_py(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genParton_pz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genParton_eta(new std::vector<double>());
	std::auto_ptr < std::vector<double> > genParton_phi(new std::vector<double>());	
	std::auto_ptr < std::vector<int> > genParton_pdgId(new std::vector<int>());	
	//jet energy correction and uncertainties
	std::auto_ptr < std::vector<double> > jec_vec(new std::vector<double>());
	std::auto_ptr < std::vector<double> > jecUnc_vec(new std::vector<double>());
	std::auto_ptr < std::vector<double> > l2l3resJEC_vec(new std::vector<double>());
	std::auto_ptr < std::vector<double> > l3absJEC_vec(new std::vector<double>());
	std::auto_ptr < std::vector<double> > l2relJEC_vec(new std::vector<double>());
	std::auto_ptr < std::vector<double> > l1offJEC_vec(new std::vector<double>());
	//jet ID variables
	std::auto_ptr < std::vector<double> > chargedEmEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<double> > chargedHadronEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<double> > chargedMuEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<double> > electronEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<double> > muonEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<double> > neutralEmEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<double> > neutralHadronEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<double> > photonEnergyFraction(new std::vector<double>());
	std::auto_ptr < std::vector<int> > chargedHadronMultiplicity(new std::vector<int>());
	std::auto_ptr < std::vector<int> > chargedMultiplicity(new std::vector<int>());
	std::auto_ptr < std::vector<int> > electronMultiplicity(new std::vector<int>());
	std::auto_ptr < std::vector<int> > muonMultiplicity(new std::vector<int>());
	std::auto_ptr < std::vector<int> > neutralHadronMultiplicity(new std::vector<int>());
	std::auto_ptr < std::vector<int> > neutralMultiplicity(new std::vector<int>());
	std::auto_ptr < std::vector<int> > photonMultiplicity(new std::vector<int>());
	std::auto_ptr < std::vector<int> > nConstituents(new std::vector<int>());
	std::auto_ptr < std::vector<double> > chargedEmEnergyFractionRAW(new std::vector<double>());
	std::auto_ptr < std::vector<double> > chargedHadronEnergyFractionRAW(new std::vector<double>());
	std::auto_ptr < std::vector<double> > neutralEmEnergyFractionRAW(new std::vector<double>());
	std::auto_ptr < std::vector<double> > neutralHadronEnergyFractionRAW(new std::vector<double>());
	std::auto_ptr < std::vector<int> > passLooseID(new std::vector<int>());
	std::auto_ptr < std::vector<int> > passTightID(new std::vector<int>());
	//b-tagging information
	std::auto_ptr < std::vector<double> > combinedInclusiveSecondaryVertexV2BJetTags(new std::vector<double>());
	std::auto_ptr < std::vector<bool> > passesLooseCSV(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > passesMediumCSV(new std::vector<bool>());
	std::auto_ptr < std::vector<bool> > passesTightCSV(new std::vector<bool>());
	std::auto_ptr < std::vector<double> > medium_btagSF(new std::vector<double>());
	std::auto_ptr < std::vector<double> > medium_btagSF_up(new std::vector<double>());
	std::auto_ptr < std::vector<double> > medium_btagSF_down(new std::vector<double>());
	std::auto_ptr < std::vector<double> > tight_btagSF(new std::vector<double>());
	std::auto_ptr < std::vector<double> > tight_btagSF_up(new std::vector<double>());
	std::auto_ptr < std::vector<double> > tight_btagSF_down(new std::vector<double>());
	//jet energy resolution and scale factors
	std::auto_ptr < std::vector<double> > jer(new std::vector<double>());
	std::auto_ptr < std::vector<double> > jerSF(new std::vector<double>());
	std::auto_ptr < std::vector<double> > jerSF_up(new std::vector<double>());
	std::auto_ptr < std::vector<double> > jerSF_down(new std::vector<double>());

	std::auto_ptr < float > tau1(new float() );
	std::auto_ptr < float > tau2(new float() );
	std::auto_ptr < float > tau3(new float() );
	std::auto_ptr < float > tau4(new float() );
	std::auto_ptr < float > tau5(new float() );
	std::auto_ptr < float > tau6(new float() );

	//jet-vertex association
	std::auto_ptr < std::vector<double> > bestVertexTrackAssociationFactor(new std::vector<double>());
	std::auto_ptr < std::vector<int> > bestVertexTrackAssociationIndex(new std::vector<int>());
	std::auto_ptr < std::vector<double> > closestVertexWeighted3DSeparation(new std::vector<double>());
	std::auto_ptr < std::vector<double> > closestVertexWeightedXYSeparation(new std::vector<double>());
	std::auto_ptr < std::vector<double> > closestVertexWeightedZSeparation(new std::vector<double>());
	std::auto_ptr < std::vector<int> > closestVertex3DIndex(new std::vector<int>());
	std::auto_ptr < std::vector<int> > closestVertexXYIndex(new std::vector<int>());
	std::auto_ptr < std::vector<int> > closestVertexZIndex(new std::vector<int>());

	edm::Handle < std::vector<pat::Jet> > jets;
	iEvent.getByToken(inputTag, jets);

	edm::Handle < edm::View<reco::PFJet> > eventjets;
	iEvent.getByToken(eventJetInputTag, eventjets);

	edm::Handle < edm::ValueMap< float > > njettiness1;
	iEvent.getByToken(njettiness1InputTag, njettiness1);
	edm::Handle < edm::ValueMap< float > > njettiness2;
	iEvent.getByToken(njettiness2InputTag, njettiness2);
	edm::Handle < edm::ValueMap< float > > njettiness3;
	iEvent.getByToken(njettiness3InputTag, njettiness3);
	edm::Handle < edm::ValueMap< float > > njettiness4;
	iEvent.getByToken(njettiness4InputTag, njettiness4);
	edm::Handle < edm::ValueMap< float > > njettiness5;
	iEvent.getByToken(njettiness5InputTag, njettiness5);
	edm::Handle < edm::ValueMap< float > > njettiness6;
	iEvent.getByToken(njettiness6InputTag, njettiness6);
		   
	*tau1.get() = 0;
	*tau2.get() = 0;
	*tau3.get() = 0;
	*tau4.get() = 0;
	*tau5.get() = 0;
	*tau6.get() = 0;

    for( unsigned int i = 0 ; i < eventjets->size() ; i++ ) {
		*tau1.get() = (*njettiness1)[ eventjets->refAt( i ) ];
		*tau2.get() = (*njettiness2)[ eventjets->refAt( i ) ];
		*tau3.get() = (*njettiness3)[ eventjets->refAt( i ) ];
		*tau4.get() = (*njettiness4)[ eventjets->refAt( i ) ];
		*tau5.get() = (*njettiness5)[ eventjets->refAt( i ) ];
		*tau6.get() = (*njettiness6)[ eventjets->refAt( i ) ];

		// std::cout << "njettiness1 : " << *tau1 << " njettiness2 : " << *tau2 << " njettiness3 : " << *tau3 << " njettiness4 : " << *tau4 << std::endl;
       }

	if (jets.isValid()) {
		for (std::vector<pat::Jet>::const_iterator it = jets->begin(); it != jets->end(); ++it) {
			// exit from loop when you reach the required number of jets
			if (px->size() >= maxSize)
				break;

			double pt = it->pt();
			double ptUp = it->userFloat("ptUp");
			double ptDown = it->userFloat("ptDown");
			// do not store any jets below a pt threshold
			if (pt <=minJetPtToStore && ptUp <= minJetPtToStore && ptDown <= minJetPtToStore)
				continue;

			if (!iEvent.isRealData()) {
				// Store generated jet resolutions for monte carlo
				double genjet_energy(0);
				double genjet_pt(0);
				double genjet_px(0);
				double genjet_py(0);
				double genjet_pz(0);
				double genjet_eta(0);
				double genjet_phi(0);

				double genparton_energy(0);
				double genparton_pt(0);
				double genparton_px(0);
				double genparton_py(0);
				double genparton_pz(0);
				double genparton_eta(0);
				double genparton_phi(0);
				double genparton_pdgId(0);				
				// take only jets with corrected pt>10 according to: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TWikiTopRefSyst#Jet_energy_resolution
				if (it->pt() > 10) {
					if (it->genJet()) { //matching (stop segmentation fault due to jet having no associated generator jet)
						genjet_energy = it->genJet()->energy();
						genjet_pt = it->genJet()->pt();
						genjet_px = it->genJet()->px();
						genjet_py = it->genJet()->py();
						genjet_pz = it->genJet()->pz();
						genjet_eta = it->genJet()->eta();
						genjet_phi = it->genJet()->phi();						
					}

					if ( it->genParton() ) {
						genparton_energy = it->genParton()->energy();
						genparton_pt = it->genParton()->pt();
						genparton_px = it->genParton()->px();
						genparton_py = it->genParton()->py();
						genparton_pz = it->genParton()->pz();
						genparton_eta = it->genParton()->eta();
						genparton_phi = it->genParton()->phi();
						genparton_pdgId = it->genParton()->pdgId();
					}
				}
				//generated jet properties
				genJet_energy->push_back(genjet_energy);
				genJet_pt->push_back(genjet_pt);
				genJet_px->push_back(genjet_px);
				genJet_py->push_back(genjet_py);
				genJet_pz->push_back(genjet_pz);
				genJet_eta->push_back(genjet_eta);
				genJet_phi->push_back(genjet_phi);

				// Matched parton properties
				genParton_energy->push_back(genparton_energy);
				genParton_pt->push_back(genparton_pt);
				genParton_px->push_back(genparton_px);
				genParton_py->push_back(genparton_py);
				genParton_pz->push_back(genparton_pz);
				genParton_eta->push_back(genparton_eta);
				genParton_phi->push_back(genparton_phi);
				genParton_pdgId->push_back(genparton_pdgId);
			}

			// fill in all the vectors
			//kinematic variables
			if ( readJEC ) {
				double jec = it->userFloat("JEC");
				px->push_back(it->correctedJet("Uncorrected").px() * jec );
				py->push_back(it->correctedJet("Uncorrected").py() * jec );
				pz->push_back(it->correctedJet("Uncorrected").pz() * jec );
				energy->push_back(it->correctedJet("Uncorrected").energy() * jec);
				jec_vec->push_back(jec);
			}
			else {
				px->push_back(it->px());
				py->push_back(it->py());
				pz->push_back(it->pz());
				energy->push_back(it->energy());
				jec_vec->push_back(it->userFloat("JEC"));
			}

			//kinematic variables before corrections
			px_raw->push_back(it->correctedJet("Uncorrected").px());
			py_raw->push_back(it->correctedJet("Uncorrected").py());
			pz_raw->push_back(it->correctedJet("Uncorrected").pz());
			energy_raw->push_back(it->correctedJet("Uncorrected").energy());

			// extra kinematic variables for easier debugging
			pt_store->push_back(it->pt());
			eta_store->push_back(it->eta());
			phi_store->push_back(it->phi());

			//extra properties
			charge->push_back(it->jetCharge());
			mass->push_back(it->mass());
			partonFlavour->push_back(it->partonFlavour());
			hadronFlavour->push_back(it->hadronFlavour());

			//jet energy correction and uncertainties
			jecUnc_vec->push_back(it->userFloat("JECUncertainty"));
			l2l3resJEC_vec->push_back(it->userFloat("L2L3ResJEC"));
			l3absJEC_vec->push_back(it->userFloat("L3AbsJEC"));
			l2relJEC_vec->push_back(it->userFloat("L2RelJEC"));
			l1offJEC_vec->push_back(it->userFloat("L1OffJEC"));

			//jet ID variables
			chargedEmEnergyFraction->push_back(it->chargedEmEnergyFraction());
			chargedHadronEnergyFraction->push_back(it->chargedHadronEnergyFraction());
			chargedMuEnergyFraction->push_back(it->chargedMuEnergyFraction());
			electronEnergyFraction->push_back(it->electronEnergy() / it->energy());
			muonEnergyFraction->push_back(it->muonEnergyFraction());
			neutralEmEnergyFraction->push_back(it->neutralEmEnergyFraction());
			neutralHadronEnergyFraction->push_back(it->neutralHadronEnergyFraction());
			photonEnergyFraction->push_back(it->photonEnergyFraction());
			chargedHadronMultiplicity->push_back(it->chargedHadronMultiplicity());
			chargedMultiplicity->push_back(it->chargedMultiplicity());
			electronMultiplicity->push_back(it->electronMultiplicity());
			muonMultiplicity->push_back(it->muonMultiplicity());
			neutralHadronMultiplicity->push_back(it->neutralHadronMultiplicity());
			neutralMultiplicity->push_back(it->neutralMultiplicity());
			photonMultiplicity->push_back(it->photonMultiplicity());
			nConstituents->push_back(it->numberOfDaughters());
			chargedEmEnergyFractionRAW->push_back(it->correctedJet("Uncorrected").chargedEmEnergyFraction());
			chargedHadronEnergyFractionRAW->push_back(it->correctedJet("Uncorrected").chargedHadronEnergyFraction());
			neutralEmEnergyFractionRAW->push_back(it->correctedJet("Uncorrected").neutralEmEnergyFraction());
			neutralHadronEnergyFractionRAW->push_back(it->correctedJet("Uncorrected").neutralHadronEnergyFraction());
			passLooseID->push_back(it->userInt("looseJetId"));
			passTightID->push_back(it->userInt("tightJetId"));
			// PU jet ID:
			// it->userInt("pileupJetId:fullId");

			//b-tagging information
			//names are changing between major software releases
			combinedInclusiveSecondaryVertexV2BJetTags->push_back(it->userFloat("btagDiscriminator"));
			passesLooseCSV->push_back( it->userInt("passesLooseBtagWP") );
			passesMediumCSV->push_back(it->userInt("passesMediumBtagWP") );
			passesTightCSV->push_back(it->userInt("passesTightBtagWP") );
			
			// Read and store b tagging scale factors for MC
			if (!iEvent.isRealData()) {
				medium_btagSF->push_back(it->userFloat("mediumBTagWeight"));
				medium_btagSF_up->push_back(it->userFloat("mediumBTagWeightUp"));
				medium_btagSF_down->push_back(it->userFloat("mediumBTagWeightDown"));
				tight_btagSF->push_back(it->userFloat("tightBTagWeight"));
				tight_btagSF_up->push_back(it->userFloat("tightBTagWeightUp"));
				tight_btagSF_down->push_back(it->userFloat("tightBTagWeightDown"));

				// Store JER and JER SF
				jer->push_back( it->userFloat("JER") );
				jerSF->push_back( it->userFloat("JER_SF") );
				jerSF_up->push_back( it->userFloat("JER_SFUp") );
				jerSF_down->push_back( it->userFloat("JER_SFDown") );
			}

			//jet-vertex association
			if (doVertexAssociation) {
				bestVertexTrackAssociationFactor->push_back(it->userFloat("bestVertexTrackAssociationFactor"));
				bestVertexTrackAssociationIndex->push_back(it->userInt("bestVertexTrackAssociationIndex"));
				closestVertexWeighted3DSeparation->push_back(it->userFloat("closestVertexWeighted3DSeparation"));
				closestVertexWeightedXYSeparation->push_back(it->userFloat("closestVertexWeightedXYSeparation"));
				closestVertexWeightedZSeparation->push_back(it->userFloat("closestVertexWeightedZSeparation"));
				closestVertex3DIndex->push_back(it->userInt("closestVertex3DIndex"));
				closestVertexXYIndex->push_back(it->userInt("closestVertexXYIndex"));
				closestVertexZIndex->push_back(it->userInt("closestVertexZIndex"));
			}
		}
	} 
	//-----------------------------------------------------------------
	// put vectors in the event
	//kinematic variables
	iEvent.put(px, prefix + "Px" + suffix);
	iEvent.put(py, prefix + "Py" + suffix);
	iEvent.put(pz, prefix + "Pz" + suffix);
	iEvent.put(energy, prefix + "Energy" + suffix);
	//kinematic variables before corrections
	iEvent.put(px_raw, prefix + "PxRAW" + suffix);
	iEvent.put(py_raw, prefix + "PyRAW" + suffix);
	iEvent.put(pz_raw, prefix + "PzRAW" + suffix);
	iEvent.put(energy_raw, prefix + "EnergyRAW" + suffix);

	// extra kinematic variables for easier debugging
	iEvent.put(pt_store, prefix + "Pt" + suffix);
	iEvent.put(eta_store, prefix + "Eta" + suffix);
	iEvent.put(phi_store, prefix + "Phi" + suffix);

	//extra properties
	iEvent.put(charge, prefix + "Charge" + suffix);
	iEvent.put(mass, prefix + "Mass" + suffix);
	iEvent.put(partonFlavour, prefix + "PartonFlavour" + suffix);
	iEvent.put(hadronFlavour, prefix + "HadronFlavour" + suffix);
	//generated jet properties
    if (!iEvent.isRealData()) {
		iEvent.put(genJet_energy, prefix + "GenJet.Energy" + suffix);
		iEvent.put(genJet_pt, prefix + "GenJet.Pt" + suffix);
		iEvent.put(genJet_px, prefix + "GenJet.Px" + suffix);
		iEvent.put(genJet_py, prefix + "GenJet.Py" + suffix);
		iEvent.put(genJet_pz, prefix + "GenJet.Pz" + suffix);
		iEvent.put(genJet_eta, prefix + "GenJet.Eta" + suffix);
		iEvent.put(genJet_phi, prefix + "GenJet.Phi" + suffix);

		iEvent.put(genParton_energy, prefix + "GenParton.Energy" + suffix);
		iEvent.put(genParton_pt, prefix + "GenParton.Pt" + suffix);
		iEvent.put(genParton_px, prefix + "GenParton.Px" + suffix);
		iEvent.put(genParton_py, prefix + "GenParton.Py" + suffix);
		iEvent.put(genParton_pz, prefix + "GenParton.Pz" + suffix);
		iEvent.put(genParton_eta, prefix + "GenParton.Eta" + suffix);
		iEvent.put(genParton_phi, prefix + "GenParton.Phi" + suffix);
		iEvent.put(genParton_pdgId, prefix + "GenParton.PdgId" + suffix);
    }
	//jet energy correction and uncertainties
    iEvent.put(jec_vec, prefix + "JEC" + suffix);
	iEvent.put(jecUnc_vec, prefix + "JECUnc" + suffix);
	iEvent.put(l2l3resJEC_vec, prefix + "L2L3ResJEC" + suffix);
	iEvent.put(l3absJEC_vec, prefix + "L3AbsJEC" + suffix);
	iEvent.put(l2relJEC_vec, prefix + "L2RelJEC" + suffix);
	iEvent.put(l1offJEC_vec, prefix + "L1OffJEC" + suffix);
	//jet ID variables
	iEvent.put(chargedEmEnergyFraction, prefix + "ChargedEmEnergyFraction" + suffix);
	iEvent.put(chargedHadronEnergyFraction, prefix + "ChargedHadronEnergyFraction" + suffix);
	iEvent.put(chargedMuEnergyFraction, prefix + "ChargedMuEnergyFraction" + suffix);
	iEvent.put(electronEnergyFraction, prefix + "ElectronEnergyFraction" + suffix);
	iEvent.put(muonEnergyFraction, prefix + "MuonEnergyFraction" + suffix);
	iEvent.put(neutralEmEnergyFraction, prefix + "NeutralEmEnergyFraction" + suffix);
	iEvent.put(neutralHadronEnergyFraction, prefix + "NeutralHadronEnergyFraction" + suffix);
	iEvent.put(photonEnergyFraction, prefix + "PhotonEnergyFraction" + suffix);
	iEvent.put(chargedHadronMultiplicity, prefix + "ChargedHadronMultiplicity" + suffix);
	iEvent.put(chargedMultiplicity, prefix + "ChargedMultiplicity" + suffix);
	iEvent.put(electronMultiplicity, prefix + "ElectronMultiplicity" + suffix);
	iEvent.put(muonMultiplicity, prefix + "MuonMultiplicity" + suffix);
	iEvent.put(neutralHadronMultiplicity, prefix + "NeutralHadronMultiplicity" + suffix);
	iEvent.put(neutralMultiplicity, prefix + "NeutralMultiplicity" + suffix);
	iEvent.put(photonMultiplicity, prefix + "PhotonMultiplicity" + suffix);
	iEvent.put(nConstituents, prefix + "NConstituents" + suffix);
	iEvent.put(chargedEmEnergyFractionRAW, prefix + "ChargedEmEnergyFractionRAW" + suffix);
	iEvent.put(chargedHadronEnergyFractionRAW, prefix + "ChargedHadronEnergyFractionRAW" + suffix);
	iEvent.put(neutralEmEnergyFractionRAW, prefix + "NeutralEmEnergyFractionRAW" + suffix);
	iEvent.put(neutralHadronEnergyFractionRAW, prefix + "NeutralHadronEnergyFractionRAW" + suffix);
	iEvent.put(passLooseID, prefix + "PassLooseID" + suffix);
	iEvent.put(passTightID, prefix + "PassTightID" + suffix);

	//b-tagging information
	iEvent.put(combinedInclusiveSecondaryVertexV2BJetTags, prefix + "combinedInclusiveSecondaryVertexV2BJetTags" + suffix);
	iEvent.put(passesLooseCSV, prefix + "passesLooseCSV" + suffix);
	iEvent.put(passesMediumCSV, prefix + "passesMediumCSV" + suffix);
	iEvent.put(passesTightCSV, prefix + "passesTightCSV" + suffix);
	
	iEvent.put(medium_btagSF, prefix + "mediumBTagSF" + suffix);
	iEvent.put(medium_btagSF_up, prefix + "mediumBTagSFUp" + suffix);
	iEvent.put(medium_btagSF_down, prefix + "mediumBTagSFDown" + suffix);

	iEvent.put(tight_btagSF, prefix + "tightBTagSF" + suffix);
	iEvent.put(tight_btagSF_up, prefix + "tightBTagSFUp" + suffix);
	iEvent.put(tight_btagSF_down, prefix + "tightBTagSFDown" + suffix);

	// jer information
	iEvent.put(jer, prefix + "jer" + suffix);
	iEvent.put(jerSF, prefix + "jerSF" + suffix);
	iEvent.put(jerSF_up, prefix + "jerSFUp" + suffix);
	iEvent.put(jerSF_down, prefix + "jerSFDown" + suffix);

	iEvent.put(tau1, prefix + "tau1" + suffix);
	iEvent.put(tau2, prefix + "tau2" + suffix);
	iEvent.put(tau3, prefix + "tau3" + suffix);
	iEvent.put(tau4, prefix + "tau4" + suffix);
	iEvent.put(tau5, prefix + "tau5" + suffix);
	iEvent.put(tau6, prefix + "tau6" + suffix);

	//jet-vertex association
	if (doVertexAssociation) {
		iEvent.put(bestVertexTrackAssociationFactor, prefix + "BestVertexTrackAssociationFactor" + suffix);
		iEvent.put(bestVertexTrackAssociationIndex, prefix + "BestVertexTrackAssociationIndex" + suffix);
		iEvent.put(closestVertexWeighted3DSeparation, prefix + "ClosestVertexWeighted3DSeparation" + suffix);
		iEvent.put(closestVertexWeightedXYSeparation, prefix + "ClosestVertexWeightedXYSeparation" + suffix);
		iEvent.put(closestVertexWeightedZSeparation, prefix + "ClosestVertexWeightedZSeparation" + suffix);
		iEvent.put(closestVertex3DIndex, prefix + "ClosestVertex3DIndex" + suffix);
		iEvent.put(closestVertexXYIndex, prefix + "ClosestVertexXYIndex" + suffix);
		iEvent.put(closestVertexZIndex, prefix + "ClosestVertexZIndex" + suffix);
	}

}
