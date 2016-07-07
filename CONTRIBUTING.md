Feel free to contribute
==================

# Structure of the project
 - bin: includes scripts, part of PATH
 - condor: deprecated
 - data: directory for JSON and ROOT files that are allowed to be public
 - external: directory for external projects
 - interface: directory for header files (`*.h`)
 - notes: directory to place notes of all kinds
 - plugins: directory for header (`*.h`) and source files (`*.cc`) that need to
   			be exported as plugins, i.e. used in the Python config files.
 - python: directory for all python files, part of PYTHONPATH
 - src: directory for source files (`*.cc`)
 - vagrant: directory for additional files for vagrant
 - BuildFile.xml: build configuration for CMSSW
 
# Before you begin
 1. Create a fork of https://github.com/BristolTopGroup/NTupleProduction/
 2. clone your fork
 3. create a branch with a name that describes the work you want to do
 4. develop your code
 5. push the changes into your for
 6. create a new pull request: https://github.com/BristolTopGroup/NTupleProduction/pulls
 
 
# Changing NTuple version
The NTP uses the version number (string) stored in `python/ntp/__init__.py` (`__version__ = X`).
This number is stored in the ntuple as well as represented in the output paths for the ntuple production.

# Debug messages
The recommended way to print messages is to use the CMSSW Message Logger (https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMessageLogger)
and the output level needs to be controlled in the run configuration (`process.MessageLogger`, e.g. https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMessageLoggerDebug). `couts` are discouraged as they cannot be turned on/off without re-compilation.

# Checking if changes affect the selection
```
# before any changes are done:
ntp run sync_ex output_file=sync_exercise_current.root
ntp create cutflow workspace/results/sync_exercise_current.root
mv workspace/results/e_cutflow.json workspace/results/e_cutflow_current.json
mv workspace/results/mu_cutflow.json workspace/results/mu_cutflow_current.json
# make changes
ntp run sync_ex output_file=sync_exercise_new.root
ntp create cutflow workspace/results/sync_exercise_new.root
# the resulting file should show no changes
ntp diff cutflow workspace/results/e_cutflow.json workspace/results/e_cutflow_current.json
ntp diff cutflow workspace/results/mu_cutflow.json workspace/results/mu_cutflow_current.json
```
 