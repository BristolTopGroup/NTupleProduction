NTupleProduction
================

## Brief Description
Software for nTuples production (v10) from AOD files for ttbar+X differential cross section analysis

## General Recipe

To setup the code:

```
#set CERNUSERNAME if not previously set
export CERNUSERNAME=yourCERNUsername
# if you don't have a token already (like on lxplus), you need to get it:
#kinit $CERNUSERNAME@CERN.CH

#change CMSSW installation paths
export SCRAM_ARCH=slc5_amd64_gcc462
scram p -n CMSSW_5_3_9_nTuple_v10 CMSSW_5_3_9
cd CMSSW_5_3_9_nTuple_v10/src
cmsenv

#PAT recipe V08-09-57 (https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATReleaseNotes52X#V08_09_57)
#StdDictionaries tag manually updated (https://hypernews.cern.ch/HyperNews/CMS/get/met/282/1/3/1/1.html)
addpkg DataFormats/PatCandidates   V06-05-06-10
addpkg PhysicsTools/PatAlgos       V08-09-57
addpkg PhysicsTools/PatUtils       V03-09-28
addpkg DataFormats/CaloRecHit      V02-05-11
addpkg DataFormats/StdDictionaries V00-02-15
addpkg FWCore/GuiBrowsers          V00-00-70
addpkg RecoMET/METProducers        V03-03-12-02

#To add the latest EGM isolation definition
addpkg RecoParticleFlow/PFProducer V15-02-06

#MET Analysis (https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMetAnalysis)
addpkg DataFormats/METReco V03-03-11-01 
addpkg JetMETCorrections/Type1MET V04-06-09-02
addpkg CommonTools/RecoUtils V00-01-04
addpkg DataFormats/ParticleFlowCandidate V15-03-04-01
addpkg DataFormats/TrackReco V10-02-02-01
addpkg DataFormats/VertexReco V02-00-04-01

#MET Filters
cvs co -r V00-00-13-01 RecoMET/METFilters
cvs co -r V00-00-08 RecoMET/METAnalyzers

#Egamma tools (https://twiki.cern.ch/twiki/bin/view/CMS/TWikiTopRefEventSel#Electrons)
cvs co -r V00-00-30-01 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools

# ElectroWeakAnalysis needed for full LHAPDF libraries to work
addpkg ElectroWeakAnalysis/Utilities

#Bristol Tools
git clone git@github.com:BristolTopGroup/NTupleProduction.git BristolAnalysis/NTupleTools
#TopSkimming
git clone git@github.com:BristolTopGroup/TopSkimming.git TopQuarkAnalysis/TopSkimming

#setup full version of LHAPDF (faster AND prevents crashes!)
scram setup lhapdffull
touch $CMSSW_BASE/src/ElectroWeakAnalysis/Utilities/BuildFile.xml
scram b -j8

#copy pile up histograms into working directory
cp BristolAnalysis/NTupleTools/data/PileUp/*.root .
#get XML files for electron MVA
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
cd - 

#test release
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=53X useData=1 maxEvents=100 dataType=Test skim=NoSkim >&test_data.log &
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=53X useData=0 maxEvents=100 dataType=Test skim=NoSkim >&test_mc.log &
#wait until tasks finish
```


## Notes
More information can be found at [Bristol Ntuple Recipes twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/BristolNTuplerRecipes), although it's outdated.

## Bugs
Please report any problems on our [issues page](https://github.com/BristolTopGroup/NTupleProduction/issues).
