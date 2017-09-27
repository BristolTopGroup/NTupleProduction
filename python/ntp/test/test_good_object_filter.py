'''
Created on 17 Mar 2017

@author: phxlk
'''
from __future__ import print_function
import unittest
import pandas as pd
from ntp.utils.data import good_object_filter


class Test(unittest.TestCase):

    def setUp(self):
        data = {
            'Muons.Pt': [[100, 10, 5], [10, 5]],
            'Electrons.Pt': [[10], [32]],
            'Jets.Pt': [[400, 300, 22, 20], [400, 300, 32, 30]],
            'channel': ['muon', 'electron'],
            'TopPairElectronPlusJetsSelection.cleanedJetIndex': [[0, 1, 2, 3], [0, 1, 3]],
            'TopPairElectronPlusJetsSelection.signalElectronIndices': [[], [0]],
            'TopPairMuonPlusJetsSelection.cleanedJetIndex': [[0, 1], [0, 1]],
            'TopPairMuonPlusJetsSelection.signalMuonIndices': [[0], []],
        }
        self.df = pd.DataFrame.from_dict(data)

    def tearDown(self):
        pass

    def testGoodObjectFilter(self):
        self.assertEqual(self.df['Muons.Pt'][0], [100, 10, 5])
        self.assertEqual(self.df['Jets.Pt'][0], [400, 300, 22, 20])
        self.assertEqual(self.df['Electrons.Pt'][0], [10])

        self.df.apply(
            good_object_filter, axis=1, columns=self.df.columns.values)

        self.assertEqual(self.df['Muons.Pt'][0], [100])
        self.assertEqual(self.df['Jets.Pt'][0], [400, 300])
        self.assertEqual(self.df['Electrons.Pt'][0], [])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
