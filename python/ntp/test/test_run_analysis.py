import unittest
import ntp
from os.path import exists, isabs, abspath
from ntp.commands.run.analysis import local, DICE
import ntp.commands.run.analysis as analysis


class TestRunAnalysis(unittest.TestCase):

    def setUp(self):
        self.command = analysis.Command()

    def test_input_files_from_path_wildcard(self):
        files = analysis.input_files_from_path('data/ScaleFactors/*.root')
        self.assertEqual(4, len(files))
        self.assertTrue(all([exists(f) for f in files]))
        self.assertTrue(all([isabs(f) for f in files]))

    def test_input_files_from_paths(self):
        f1 = 'data/ScaleFactors/hadronLegEfficiencies_electron.root'
        files = analysis.input_files_from_path(f1)
        self.assertEqual(1, len(files))
        self.assertTrue(all([exists(f) for f in files]))
        self.assertTrue(all([isabs(f) for f in files]))

    def test_input_files_from_path_with_comma(self):
        f1 = 'data/ScaleFactors/hadronLegEfficiencies_electron.root'
        f2 = 'data/ScaleFactors/scaleFactors_electron_id_iso.root'
        path = ','.join([f1, f2])
        files = analysis.input_files_from_path(path)
        self.assertEqual(2, len(files))
        self.assertTrue(all([exists(f) for f in files]))
        self.assertTrue(all([isabs(f) for f in files]))

    def test_input_files_from_nonexisting_path(self):
        f1 = 'data/ScaleFactors/hadronLegEfficiencies_electron.root'
        f2 = 'data/ScaleFactors/doesnotexist.root'
        path = ','.join([f1, f2])
        files = analysis.input_files_from_path(path)
        self.assertEqual(1, len(files))
        self.assertTrue(all([exists(f) for f in files]))
        self.assertTrue(all([isabs(f) for f in files]))

    def test_input_files_from_dataset(self):
        # This test requires HDFS
        if exists('/hdfs/TopQuarkGroup'):
            dataset = 'TTJets_PowhegPythia8'
            files = analysis.input_files_from_dataset(dataset)
            
    def test_run_noop(self):
        f1 = 'data/ScaleFactors/hadronLegEfficiencies_electron.root'
        f2 = 'data/ScaleFactors/scaleFactors_electron_id_iso.root'
        parameters = {
            'files': ','.join([f1, f2]),
            'noop': True,
        }
        arguments = []
        self.command.run(arguments, parameters)


class TestRunAnalysisLocal(unittest.TestCase):

    def setUp(self):
        self.command = local.Command()

    def test_input_files_from_path_wildcard(self):
        f1 = abspath('data/ScaleFactors/hadronLegEfficiencies_electron.root')
        

class TestRunAnalysisDICE(unittest.TestCase):

    def setUp(self):
        self.command = DICE.Command()

if __name__ == '__main__':
    unittest.main()
