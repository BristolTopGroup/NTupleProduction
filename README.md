NTupleProduction
================

## Brief Description
Software for nTuples production (44X) from AOD files for ttbar+MET differential cross section analysis

## General Recipe

To setup the code:

```
export SCRAM_ARCH=slc5_amd64_gcc434
scram p -n CMSSW_4_4_4_nTuple_v9a CMSSW_4_4_4
cd CMSSW_4_4_4_nTuple_v9a/src
cmsenv
#PAT recipe
addpkg DataFormats/PatCandidates V06-05-01
addpkg PhysicsTools/PatAlgos     V08-07-47
addpkg PhysicsTools/PatUtils     V03-09-18-03
addpkg CommonTools/ParticleFlow  V00-03-05-10
addpkg FWCore/GuiBrowsers        V00-00-60

#MET Analysis
addpkg JetMETCorrections/Type1MET V04-05-08
addpkg PhysicsTools/PatUtils b4_2_X_cvMEtCorr_13Feb2012_JEC11V12
addpkg DataFormats/METReco V03-03-07

#MET Filters
addpkg DataFormats/METReco lhx_12JAN2012_v1
addpkg RecoMET/METFilters lhx_14APR2012_v1
cvs co -r V00-00-08 RecoMET/METAnalyzers

#still needed for 3D Lumi reweighting
addpkg PhysicsTools/Utilities V08-03-18

#Egamma tools
cvs co -r V00-00-10 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools

#ElectroWeak tools (pdf weights). In order to run with CRAB check:
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEWKUtilities#How_to_compile_link_run
addpkg ElectroWeakAnalysis/Utilities V00-04-00

#Bristol tools & RootTupleMaker
git clone git@github.com:BristolTopGroup/NTupleProduction.git -b 44X BristolAnalysis/NTupleTools
#TopSkimming
git clone git@github.com:BristolTopGroup/TopSkimming.git TopQuarkAnalysis/TopSkimming

#setup full version of LHAPDF (faster AND prevents crashes!)
scram setup lhapdffull
scram b -j8

#copy pile up histograms into working directory
cp BristolAnalysis/NTupleTools/data/PileUp/*.root .
#get XML files for electron MVA
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
cd - 

#test release
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=44X useData=1 maxEvents=100 dataType=Test skim=NoSkim >&test_data.log &
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=44X useData=0 maxEvents=100 dataType=Test skim=NoSkim >&test_mc.log &
#wait until tasks finish
```


## Notes
More information can be found at [Bristol Ntuple Recipes twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/BristolNTuplerRecipes)

## Bugs
Please report any problems on our [issues page](https://github.com/BristolTopGroup/NTupleProduction/issues).
