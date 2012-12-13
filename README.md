NTupleProduction
================

## Brief Description
Software for nTuples creation from AOD files for ttbar+MET differential cross section analysis

## General Recipe

To setup the code:

```
export SCRAM_ARCH=slc5_amd64_gcc462
scram p -n CMSSW_5_3_5_nTuple_v9a CMSSW_5_3_5
cd CMSSW_5_3_5_nTuple_v9a/src
cmsenv

#PAT recipe (V08-09-43)
addpkg DataFormats/PatCandidates V06-05-06-03
addpkg PhysicsTools/PatAlgos     V08-09-43

#PatUtils (although not in official recipe, apparently still needed)
addpkg PhysicsTools/PatUtils V03-09-26

#To add the latest EGM isolation definition
#addpkg RecoParticleFlow/PFProducer V15-02-06

#MET Analysis
addpkg JetMETCorrections/Type1MET V04-06-09

#MET Filters
cvs co -r V00-00-10 RecoMET/METFilters
cvs co -r V00-00-08 RecoMET/METAnalyzers

#Egamma tools
cvs co -r V00-00-31 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools

#Bristol Tools
git clone git@github.com:BristolTopGroup/NTupleProduction.git BristolAnalysis/NTupleTools
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
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=53X useData=1 maxEvents=100 dataType=Test skim=NoSkim >&test_data.log &
nohup cmsRun BristolAnalysis/NTupleTools/test/makeTuples_cfg.py CMSSW=53X useData=0 maxEvents=100 dataType=Test skim=NoSkim >&test_mc.log &
#wait until tasks finish
```


## Notes
More information can be found at [Bristol Ntuple Recipes twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/BristolNTuplerRecipes)

## Bugs
Please report any problems on our [issues page](https://github.com/BristolTopGroup/NTupleProduction/issues).
