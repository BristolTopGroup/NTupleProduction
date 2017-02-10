'''
Created on 10 Feb 2017

@author: phxlk
'''
import unittest
import os

from ntp.commands.create.tarball import Command as TarCommand
from ntp.commands.run import Command as RunCommand


class Test(unittest.TestCase):


    def setUp(self):
        existing_files = TarCommand.get_existing_files()
        for f in existing_files:
            os.remove(f)


    def tearDown(self):
        pass


    def testCreateTar(self):
        c1 = RunCommand()
        c1._create_tar_file([], {})
        existing_files = TarCommand.get_existing_files()
        self.assertTrue(len(existing_files) > 0)
        
        if not existing_files:
            return
        
        mtime1 = os.path.getmtime(existing_files[0])
        
        c2 = RunCommand()
        # this should not create a second tar file
        # since a "fresh" one exists
        c2._create_tar_file([], {})
        existing_files = TarCommand.get_existing_files()
        mtime2 = os.path.getmtime(existing_files[0])
        self.assertEqual(mtime1, mtime2)
            


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCreateTar']
    unittest.main()