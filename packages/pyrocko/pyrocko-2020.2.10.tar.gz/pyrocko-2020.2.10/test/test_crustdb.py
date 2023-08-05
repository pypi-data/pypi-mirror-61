from __future__ import division, print_function, absolute_import
import unittest
import numpy as num  # noqa
import logging
import shutil
from tempfile import mkdtemp
from os.path import join as pjoin

from pyrocko import util
from pyrocko.dataset import crustdb

logger = logging.getLogger('pyrocko.test.test_crustdb')


class CrustDBTestCase(unittest.TestCase):

    def setUp(self):
        self.tmpdir = mkdtemp('pyrocko.crustdb')
        self.db = crustdb.CrustDB()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    @unittest.skip('Plotting not tested atm.')
    def test_map(self):
        tmpmap = pjoin(self.tmpdir, 'map.ps')
        self.db.plotMap(tmpmap)

    def test_selections(self):
        polygon = [(25., 30.), (30., 30.), (30, 25.), (25., 25.)]
        self.db.selectLocation(25., 95., 5.)
        self.db.selectRegion(25., 30., 20., 45.)
        self.db.selectPolygon(polygon)
        self.db.selectVs()
        self.db.selectVp()
        self.db.selectMaxDepth(40.)
        self.db.selectMinDepth(20.)

    @unittest.skip('Plotting not tested atm.')
    def test_ploting(self):
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.gca()

        profile = self.db[10]
        self.db.plot(axes=ax)
        self.db.plotHistogram(axes=ax)
        profile.plot(axes=ax)

        fig.clear()


if __name__ == "__main__":
    util.setup_logging('test_crustdb', 'warning')
    unittest.main()
