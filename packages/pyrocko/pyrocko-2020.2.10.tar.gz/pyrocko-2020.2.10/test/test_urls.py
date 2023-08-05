
import unittest
import logging
from pyrocko import util
from . import common

logger = logging.getLogger('pyrocko.test.test_urls')

try:
    from urllib2 import (Request, HTTPError, urlopen)
except ImportError:
    from urllib.request import (Request, urlopen)
    from urllib.error import HTTPError


class UrlsTestCase(unittest.TestCase):

    @common.require_internet
    def test_url_alive(self):
        # Test urls which are used as references in pyrocko if they still
        # exist.
        to_check = [
            ('http://nappe.wustl.edu/antelope/css-formats/wfdisc.htm',
             'pyrocko.css'),
            ('http://www.ietf.org/timezones/data/leap-seconds.list',
             'pyrocko.config'),
            ('http://stackoverflow.com/questions/2417794/', 'cake_plot'),
            ('http://igppweb.ucsd.edu/~gabi/rem.html', 'crust2x2_data'),
            ('http://kinherd.org/pyrocko_data/gsc20130501.txt', 'crustdb'),
            ('http://download.geonames.org/export/dump/', 'geonames'),
            ('http://emolch.github.io/gmtpy/', 'gmtpy'),
            ('http://www.apache.org/licenses/LICENSE-2.0', 'kagan.py'),
            ('http://www.opengis.net/kml/2.2', 'model'),
            ('http://maps.google.com/mapfiles/kml/paddle/S.png', 'model'),
            ('http://de.wikipedia.org/wiki/Orthodrome', 'orthodrome'),
            ('http://peterbird.name/oldFTP/PB2002', 'tectonics'),
            ('http://gsrm.unavco.org/model', 'tectonics'),
            ('http://stackoverflow.com/questions/19332902/', 'util'),
        ]

        for url, label in to_check:
            try:
                try:
                    req = Request(url, method='HEAD')
                except TypeError:
                    req = Request(url)

                f = urlopen(req)
                f.close()
            except Exception as e:
                logger.warn('%s - %s referenced in pyrocko.%s' %
                            (e, url, label))


if __name__ == '__main__':
    util.setup_logging('test_urls', 'warning')
    unittest.main()
