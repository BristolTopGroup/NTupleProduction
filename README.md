NTupleProduction
================

## Brief Description
Software for nTuples production from miniAOD files for ttbar+X differential cross section analysis

## General Recipe

To setup the code:

```
#set GITHUBUSERNAME if not previously set
export GITHUBUSERNAME=yourGITHUBUsername
git config --global user.github $GITHUBUSERNAME
#on soolin:
export CMSSW_GIT_REFERENCE=/storage/.cmsgit-cache


# Set up the CMSSW release
export SCRAM_ARCH=slc6_amd64_gcc491
cmsrel CMSSW_7_4_0
cd CMSSW_7_4_0/src/
cmsenv

# Do merge-topics and addpkgs first
# Add TopEventProducers as we need to modify one file later on 
git cms-addpkg TopQuarkAnalysis/TopEventProducers/

# Clone our main ntuple producing software and checkout run2 branch
git clone git@github.com:BristolTopGroup/NTupleProduction.git BristolAnalysis/NTupleTools
cd BristolAnalysis/NTupleTools
git remote rename origin upstream
git remote add origin git@github.com:<Your Git name with forked repo>/NTupleProduction.git
git fetch --all
git checkout -b CMSSW_7_3_X upstream/CMSSW_7_3_X
cd ../../

# Clone our version of the TopSkimming software and checkout run2 branch
git clone git@github.com:BristolTopGroup/TopSkimming.git TopQuarkAnalysis/TopSkimming
cd TopQuarkAnalysis/TopSkimming
git remote rename origin upstream
git checkout -b CMSSW_7_3_X upstream/CMSSW_7_3_X
cd ../../

#### In TopQuarkAnalysis/TopEventProducers/python/producers/TopDecaySubset_cfi.py
#### Set runMode to Run2

# Compile
scramv1 b -j 8


#test release
### Not yet available
```


## Notes
More information can be found at [Bristol Ntuple Recipes twiki page](https://twiki.cern.ch/twiki/bin/view/CMS/BristolNTuplerRecipes), although it's outdated.

## Bugs
Please report any problems on our [issues page](https://github.com/BristolTopGroup/NTupleProduction/issues).
