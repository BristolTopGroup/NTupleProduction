from __future__ import division
import unittest


class TestInterpreter(unittest.TestCase):

    def test_make_chunks(self):
        from ntp.utils import make_even_chunks
        l = list(range(100))
        size_of_chunk = 9
        n_groups = int(len(l) / size_of_chunk)
        chunks = list(make_even_chunks(l, size_of_chunk))
        self.assertEqual(len(chunks), n_groups)
        for c in chunks:
            self.assertGreaterEqual(len(c), size_of_chunk)

    def test_make_chunks_one_element(self):
        from ntp.utils import make_even_chunks
        l = [5]
        chunks = list(make_even_chunks(l, 50))
        self.assertEqual(len(chunks), 1)

if __name__ == '__main__':
    unittest.main()
