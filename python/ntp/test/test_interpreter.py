import unittest
import ntp

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.cli_input1 = ['help', 'list', 'sample']
        self.args1 = ['list', 'verbose=1', 'sample=TTJet', 'lumi=100.05']
        
    def test_find_command(self):
        command, args = ntp.interpreter._find_command_and_args(self.cli_input1)
        self.assertIsInstance(command, ntp.commands.help.Command)
        self.assertEqual(args, self.cli_input1[1:])
        
    def test_parse(self):
        positional_args, variables = ntp.interpreter._parse_args(self.args1)
        self.assertEqual(len(positional_args), 1)
        self.assertEqual(positional_args[0], 'list')
        self.assertIn('verbose', variables)
        self.assertIn('sample', variables)
        self.assertIn('lumi', variables)
        self.assertEqual(variables['verbose'], True)
        self.assertEqual(variables['sample'], 'TTJet')
        self.assertAlmostEqual(variables['lumi'], 100.05, delta = 0.001)
        
if __name__ == '__main__':
    unittest.main()