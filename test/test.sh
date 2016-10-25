#!/bin/bash
set -e
echo "Testing hepshell"
python -c 'import hepshell'
echo "Testing ntp"
python -c 'import ntp'
echo "Testing pycurl"
python -c 'import pycurl'
echo "Testing ROOT, rootpy & dps"
python -c 'import ROOT; import rootpy; import dps'
