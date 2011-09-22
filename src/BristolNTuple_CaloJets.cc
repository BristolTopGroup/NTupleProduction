#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_CaloJets.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "PhysicsTools/SelectorUtils/interface/JetIDSelectionFunctor.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"
#include "FWCore/Framework/interface/ESHandle.h"


BristolNTuple_CaloJets::BristolNTuple_CaloJets(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag> ("InputTag")),
    prefix(iConfig.getParameter<std::string> ("Prefix")),
    suffix(iConfig.getParameter<std::string> ("Suffix")),
    maxSize(iConfig.getParameter<unsigned int> ("MaxSize")),
    jecUncPath(iConfig.getParameter<std::string>("JECUncertainty")),
    readJECuncertainty (iConfig.getParameter<bool>   ("ReadJECuncertainty"))
{

    produces<std::vector<double> > (prefix + "Px" + suffix);
    produces<std::vector<double> > (prefix + "Py" + suffix);
    produces<std::vector<double> > (prefix + "Pz" + suffix);
    produces<std::vector<double> > (prefix + "Charge" + suffix);
    produces<std::vector<double> > (prefix + "Mass" + suffix);

    produces<std::vector<double> > (prefix + "PtRaw" + suffix);
    produces<std::vector<double> > (prefix + "Energy" + suffix);
    produces<std::vector<double> > (prefix + "EnergyRaw" + suffix);
    produces<std::vector<int> > (prefix + "PartonFlavour" + suffix);

    produces<std::vector<double> > (prefix + "JECUnc" + suffix);
    produces<std::vector<double> > (prefix + "L2L3ResJEC" + suffix);
    produces<std::vector<double> > (prefix + "L3AbsJEC" + suffix);
    produces<std::vector<double> > (prefix + "L2RelJEC" + suffix);
    produces<std::vector<double> > (prefix + "L1OffJEC" + suffix);

    produces<std::vector<double> > (prefix + "EMF" + suffix);
    produces<std::vector<double> > (prefix + "resEMF" + suffix);
    produces<std::vector<double> > (prefix + "HADF" + suffix);
    produces<std::vector<int> > (prefix + "n90Hits" + suffix);
    produces<std::vector<double> > (prefix + "fHPD" + suffix);
    produces<std::vector<double> > (prefix + "fRBX" + suffix);
    produces<std::vector<double> > (prefix + "SigmaEta" + suffix);
    produces<std::vector<double> > (prefix + "SigmaPhi" + suffix);

    //names are changing between major software releases
    produces<std::vector<double> > (prefix + "TrackCountingHighEffBTag" + suffix);
    produces<std::vector<double> > (prefix + "TrackCountingHighPurBTag" + suffix);
    produces<std::vector<double> > (prefix + "SimpleSecondaryVertexHighEffBTag" + suffix);
    produces<std::vector<double> > (prefix + "SimpleSecondaryVertexHighPurBTag" + suffix);
    produces<std::vector<double> > (prefix + "JetProbabilityBTag" + suffix);
    produces<std::vector<double> > (prefix + "JetBProbabilityBTag" + suffix);

    produces<std::vector<double> > (prefix + "SoftElectronByIP3dBJetTag" + suffix);
    produces<std::vector<double> > (prefix + "SoftElectronByPtBJetTag" + suffix);

    produces<std::vector<double> > (prefix + "SoftMuonBJetTag" + suffix);
    produces<std::vector<double> > (prefix + "SoftMuonByIP3dBJetTag" + suffix);
    produces<std::vector<double> > (prefix + "SoftMuonByPtBJetTag" + suffix);
    produces<std::vector<double> > (prefix + "CombinedSecondaryVertexMVABJetTag" + suffix);
    produces<std::vector<double> > (prefix + "CombinedSecondaryVertexBJetTag" + suffix);
    // checked 19.09.2011
    produces<std::vector<int> > (prefix + "PassLooseID" + suffix);
    produces<std::vector<int> > (prefix + "PassTightID" + suffix);
}

void BristolNTuple_CaloJets::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr < std::vector<double> > px(new std::vector<double>());
    std::auto_ptr < std::vector<double> > py(new std::vector<double>());
    std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > charge(new std::vector<double>());
    std::auto_ptr < std::vector<double> > mass(new std::vector<double>());

    std::auto_ptr < std::vector<double> > pt_raw(new std::vector<double>());
    std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
    std::auto_ptr < std::vector<double> > energy_raw(new std::vector<double>());
    std::auto_ptr < std::vector<int> > partonFlavour(new std::vector<int>());

    std::auto_ptr < std::vector<double> > jecUnc_vec(new std::vector<double>());
    std::auto_ptr < std::vector<double> > l2l3resJEC_vec(new std::vector<double>());
    std::auto_ptr < std::vector<double> > l3absJEC_vec(new std::vector<double>());
    std::auto_ptr < std::vector<double> > l2relJEC_vec(new std::vector<double>());
    std::auto_ptr < std::vector<double> > l1offJEC_vec(new std::vector<double>());

    std::auto_ptr < std::vector<double> > emf(new std::vector<double>());
    std::auto_ptr < std::vector<double> > resEmf(new std::vector<double>());
    std::auto_ptr < std::vector<double> > hadf(new std::vector<double>());
    std::auto_ptr < std::vector<int> > n90Hits(new std::vector<int>());
    std::auto_ptr < std::vector<double> > fHPD(new std::vector<double>());
    std::auto_ptr < std::vector<double> > fRBX(new std::vector<double>());
    std::auto_ptr < std::vector<double> > sigmaEta(new std::vector<double>());
    std::auto_ptr < std::vector<double> > sigmaPhi(new std::vector<double>());

    std::auto_ptr < std::vector<double> > trackCountingHighEffBTag(new std::vector<double>());
    std::auto_ptr < std::vector<double> > trackCountingHighPurBTag(new std::vector<double>());
    std::auto_ptr < std::vector<double> > simpleSecondaryVertexHighEffBTag(new std::vector<double>());
    std::auto_ptr < std::vector<double> > simpleSecondaryVertexHighPurBTag(new std::vector<double>());
    std::auto_ptr < std::vector<double> > jetProbabilityBTag(new std::vector<double>());
    std::auto_ptr < std::vector<double> > jetBProbabilityBTag(new std::vector<double>());

    std::auto_ptr < std::vector<double> > softElectronByIP3dBJetTags(new std::vector<double>());
    std::auto_ptr < std::vector<double> > softElectronByPtBJetTags(new std::vector<double>());

    std::auto_ptr < std::vector<double> > softMuonBJetTag(new std::vector<double>());
    std::auto_ptr < std::vector<double> > softMuonByIP3dBJetTags(new std::vector<double>());
    std::auto_ptr < std::vector<double> > softMuonByPtBJetTags(new std::vector<double>());

    std::auto_ptr < std::vector<double> > combinedSecondaryVertexBJetTags(new std::vector<double>());
    std::auto_ptr < std::vector<double> > combinedSecondaryVertexMVABJetTag(new std::vector<double>());

    std::auto_ptr < std::vector<int> > passLooseID(new std::vector<int>());
    std::auto_ptr < std::vector<int> > passTightID(new std::vector<int>());


    //JEC Uncertainties
    JetCorrectionUncertainty *jecUnc = 0;
    if (readJECuncertainty) {
        //(See https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/1075/1.html
        // and https://hypernews.cern.ch/HyperNews/CMS/get/physTools/2367/1.html)
        // handle the jet corrector parameters collection
        edm::ESHandle < JetCorrectorParametersCollection > JetCorParColl;
        // get the jet corrector parameters collection from the global tag
        iSetup.get<JetCorrectionsRecord> ().get(jecUncPath, JetCorParColl);
        // get the uncertainty parameters from the collection
        JetCorrectorParameters const & JetCorPar = (*JetCorParColl)["Uncertainty"];
        // instantiate the jec uncertainty object
        jecUnc = new JetCorrectionUncertainty(JetCorPar);
    }

    JetIDSelectionFunctor jetIDLoose( JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::LOOSE );
    JetIDSelectionFunctor jetIDTight( JetIDSelectionFunctor::PURE09, JetIDSelectionFunctor::TIGHT );

    pat::strbitset ret = jetIDLoose.getBitTemplate();

    edm::Handle < std::vector<pat::Jet> > jets;
    iEvent.getByLabel(inputTag, jets);

    if (jets.isValid()) {
        edm::LogInfo("BristolNTuple_CaloJetsExtraInfo") << "Total # CaloJets: " << jets->size();

        for (std::vector<pat::Jet>::const_iterator it = jets->begin(); it != jets->end(); ++it) {
            // exit from loop when you reach the required number of jets
            if (px->size() >= maxSize)
                break;
            ret.set(false);
            int passjetLoose = 0;
            if (jetIDLoose(*it, ret))
                passjetLoose = 1;

            ret.set(false);
            int passjetTight = 0;
            if (jetIDTight(*it, ret))
                passjetTight = 1;

            if (readJECuncertainty) {
                jecUnc->setJetEta(it->eta());
                jecUnc->setJetPt(it->pt()); // the uncertainty is a function of the corrected pt
            }

            // fill in all the vectors
            px->push_back(it->px());
            py->push_back(it->py());
            pz->push_back(it->pz());
            charge->push_back(it->jetCharge());
            mass->push_back(it->mass());

            pt_raw->push_back(it->correctedJet("Uncorrected").pt());
            energy->push_back(it->energy());
            energy_raw->push_back(it->correctedJet("Uncorrected").energy());
            partonFlavour->push_back(it->partonFlavour());

            l2l3resJEC_vec->push_back(it->pt() / it->correctedJet("L3Absolute").pt());
            l3absJEC_vec->push_back(it->correctedJet("L3Absolute").pt() / it->correctedJet("L2Relative").pt());
            l2relJEC_vec->push_back(it->correctedJet("L2Relative").pt() / it->correctedJet("L1Offset").pt());
            l1offJEC_vec->push_back(it->correctedJet("L1Offset").pt() / it->correctedJet("Uncorrected").pt());
            if (readJECuncertainty)
                jecUnc_vec->push_back(jecUnc->getUncertainty(true));
            else
                jecUnc_vec->push_back(-999);

            emf->push_back(it->emEnergyFraction());
            resEmf->push_back(it->jetID().restrictedEMF);
            hadf->push_back(it->energyFractionHadronic());
            n90Hits->push_back(it->jetID().n90Hits);
            fHPD->push_back(it->jetID().fHPD);
            fRBX->push_back(it->jetID().fRBX);
            sigmaEta->push_back(sqrt(it->etaetaMoment()));
            sigmaPhi->push_back(sqrt(it->phiphiMoment()));

            //names are changing between major software releases
            trackCountingHighEffBTag->push_back(it->bDiscriminator("trackCountingHighEffBJetTags"));// checked 19.09.2011
            trackCountingHighPurBTag->push_back(it->bDiscriminator("trackCountingHighPurBJetTags"));// checked 19.09.2011
            simpleSecondaryVertexHighEffBTag->push_back(it->bDiscriminator("simpleSecondaryVertexHighEffBJetTags"));// checked 19.09.2011
            simpleSecondaryVertexHighPurBTag->push_back(it->bDiscriminator("simpleSecondaryVertexHighPurBJetTags"));// checked 19.09.2011
            jetProbabilityBTag->push_back(it->bDiscriminator("jetProbabilityBJetTags"));// checked 19.09.2011
            jetBProbabilityBTag->push_back(it->bDiscriminator("jetBProbabilityBJetTags"));// checked 19.09.2011

            softElectronByIP3dBJetTags->push_back(it->bDiscriminator("softElectronByIP3dBJetTags"));// corrected 19.09.2011
            softElectronByPtBJetTags->push_back(it->bDiscriminator("softElectronByPtBJetTags"));// introduced 19.09.2011
            softMuonBJetTag->push_back(it->bDiscriminator("softMuonBJetTags"));// checked 19.09.2011
            softMuonByIP3dBJetTags->push_back(it->bDiscriminator("softMuonByIP3dBJetTags"));// corrected 19.09.2011
            softMuonByPtBJetTags->push_back(it->bDiscriminator("softMuonByPtBJetTags"));// introduced 19.09.2011
            combinedSecondaryVertexBJetTags->push_back(it->bDiscriminator("combinedSecondaryVertexBJetTags"));// corrected 19.09.2011
            combinedSecondaryVertexMVABJetTag->push_back(it->bDiscriminator("combinedSecondaryVertexMVABJetTag"));// corrected 19.09.2011

            passLooseID->push_back(passjetLoose);
            passTightID->push_back(passjetTight);
        }
    } else {
        edm::LogError("BristolNTuple_CaloJetsError") << "Error! Can't get the product " << inputTag;
    }
    delete jecUnc;
    //-----------------------------------------------------------------
    // put vectors in the event
    iEvent.put(px, prefix + "Px" + suffix);
    iEvent.put(py, prefix + "Py" + suffix);
    iEvent.put(pz, prefix + "Pz" + suffix);
    iEvent.put(charge, prefix + "Charge" + suffix);
    iEvent.put(mass, prefix + "Mass" + suffix);

    iEvent.put(pt_raw, prefix + "PtRaw" + suffix);
    iEvent.put(energy, prefix + "Energy" + suffix);
    iEvent.put(energy_raw, prefix + "EnergyRaw" + suffix);
    iEvent.put(partonFlavour, prefix + "PartonFlavour" + suffix);

    iEvent.put(jecUnc_vec, prefix + "JECUnc" + suffix);
    iEvent.put(l2l3resJEC_vec, prefix + "L2L3ResJEC" + suffix);
    iEvent.put(l3absJEC_vec, prefix + "L3AbsJEC" + suffix);
    iEvent.put(l2relJEC_vec, prefix + "L2RelJEC" + suffix);
    iEvent.put(l1offJEC_vec, prefix + "L1OffJEC" + suffix);

    iEvent.put(emf, prefix + "EMF" + suffix);
    iEvent.put(resEmf, prefix + "resEMF" + suffix);
    iEvent.put(hadf, prefix + "HADF" + suffix);
    iEvent.put(n90Hits, prefix + "n90Hits" + suffix);
    iEvent.put(fHPD, prefix + "fHPD" + suffix);
    iEvent.put(fRBX, prefix + "fRBX" + suffix);
    iEvent.put(sigmaEta, prefix + "SigmaEta" + suffix);
    iEvent.put(sigmaPhi, prefix + "SigmaPhi" + suffix);

    iEvent.put(trackCountingHighEffBTag, prefix + "TrackCountingHighEffBTag" + suffix);
    iEvent.put(trackCountingHighPurBTag, prefix + "TrackCountingHighPurBTag" + suffix);
    iEvent.put(simpleSecondaryVertexHighEffBTag, prefix + "SimpleSecondaryVertexHighEffBTag" + suffix);
    iEvent.put(simpleSecondaryVertexHighPurBTag, prefix + "SimpleSecondaryVertexHighPurBTag" + suffix);
    iEvent.put(jetProbabilityBTag, prefix + "JetProbabilityBTag" + suffix);
    iEvent.put(jetBProbabilityBTag, prefix + "JetBProbabilityBTag" + suffix);

    iEvent.put(softElectronByIP3dBJetTags, prefix + "SoftElectronByIP3dBJetTag" + suffix);
    iEvent.put(softElectronByPtBJetTags, prefix + "SoftElectronByPtBJetTag" + suffix);
    iEvent.put(softMuonBJetTag, prefix + "SoftMuonBJetTag" + suffix);
    iEvent.put(softMuonByIP3dBJetTags, prefix + "SoftMuonByIP3dBJetTag" + suffix);
    iEvent.put(softMuonByPtBJetTags, prefix + "SoftMuonByPtBJetTag" + suffix);
    iEvent.put(combinedSecondaryVertexBJetTags, prefix + "CombinedSecondaryVertexBJetTag" + suffix);
    iEvent.put(combinedSecondaryVertexMVABJetTag, prefix + "CombinedSecondaryVertexMVABJetTag" + suffix);

    iEvent.put(passLooseID, prefix + "PassLooseID" + suffix);
    iEvent.put(passTightID, prefix + "PassTightID" + suffix);
}
