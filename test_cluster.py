import unittest

from line import Line, Multiple
from cluster import ConsonantCluster
from misc import trace, dd
from testing import strip_sources, reduce_to_text


class TestCluster(unittest.TestCase):

    maxDiff = None

    def test_basics(self):
        self.assertCountEqual(
            reduce_to_text(Line('blurbsit blabst').with_clusters),
            # Only 'urbs' gets split multiple ways, since it's in the
            # middle of a word.
            Multiple(
                [
                    ConsonantCluster('b', 'l'),
                    'u',
                    ConsonantCluster('r'),
                    ConsonantCluster('b', 's'),
                    'i',
                    ConsonantCluster('t'),
                    ConsonantCluster('b', 'l'),
                    'a',
                    ConsonantCluster('b', 's', 't')
                ],
                [
                    ConsonantCluster('b', 'l'),
                    'u',
                    ConsonantCluster('r', 'b'),
                    ConsonantCluster('s'),
                    'i',
                    ConsonantCluster('t'),
                    ConsonantCluster('b', 'l'),
                    'a',
                    ConsonantCluster('b', 's', 't')
                ],
                [
                    ConsonantCluster('b', 'l'),
                    'u',
                    ConsonantCluster('r', 'b', 's'),
                    'i',
                    ConsonantCluster('t'),
                    ConsonantCluster('b', 'l'),
                    'a',
                    ConsonantCluster('b', 's', 't')
                ],
            )
        )

    def test_urbs_an(self):
        self.assertCountEqual(
            reduce_to_text(Line('urbs an').with_clusters),
            Multiple(
                [
                    'u',
                    ConsonantCluster('r', 'b'),
                    ConsonantCluster('s'),
                    'a',
                    ConsonantCluster('n')
                ]
            )
        )

if __name__ == '__main__':
    unittest.main()

