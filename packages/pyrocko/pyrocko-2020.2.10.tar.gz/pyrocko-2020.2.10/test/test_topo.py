from __future__ import division, print_function, absolute_import
import unittest
import numpy as num
from pyrocko import util, config
from pyrocko.dataset import topo


def have_srtm_credentials():
    if config.config().earthdata_credentials is None:
        return False
    return True


class TopoTestCase(unittest.TestCase):

    @unittest.skipUnless(
        have_srtm_credentials(),
        'No Earthdata credentials in config.')
    def test_srtm(self):
        srtm = topo.srtmgl3
        tiles = list(srtm.available_tilenames())

        tilenum = num.random.randint(0, len(tiles)-1)
        srtm.download_tile(tiles[tilenum])
        srtm.get_tile(0, 0)

    @unittest.skip('etopo not downloaded.')
    def test_etopo(self):
        topo.etopo1.make_tiles()

    def test_tile(self):
        tile1 = topo.tile.Tile(
            0., 0.,
            1., 1.,
            num.ones((100, 100)))
        tile2 = topo.tile.Tile(
            0., 0.,
            1., 1.,
            num.ones((100, 100)))

        topo.tile.combine([tile1, tile2])


if __name__ == '__main__':
    util.setup_logging('test_topo', 'debug')
    unittest.main()
