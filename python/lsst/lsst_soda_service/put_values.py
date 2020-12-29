import numpy
from astropy.table import QTable
from astropy.coordinates import SkyCoord
import astropy.units as u

from lsst.daf.butler import Butler, DatasetType


def put_values(repo, visit, detector, instrument, out_collection,
               ra=None, dec=None, size=None, filename=None):
    butler = Butler(repo, writeable=True, run=out_collection)
    # This doesn't strictly need to be done every time,
    # but doesn't seem to hurt if the
    # dataset type already exists
    position_dataset_type = DatasetType('cutout_positions', dimensions=['visit', 'detector', 'instrument'],
                                        universe=butler.registry.dimensions,
                                        storageClass='AstropyQTable')
    butler.registry.registerDatasetType(position_dataset_type)

    if filename:
        poslist = numpy.genfromtxt(filename, dtype=None, delimiter=',')
    else:
        poslist = [(ra, dec, size), ]
    ident = []
    pos = []
    size = []
    for i, rec in enumerate(poslist):
        pt = SkyCoord(rec[0], rec[1], frame='icrs', unit=u.deg)
        pos.append(pt)
        ident.append(i*u.dimensionless_unscaled)
        size.append(rec[2]*u.dimensionless_unscaled)
    out_table = QTable([ident, pos, size], names=['id', 'position', 'size'])
    butler.put(out_table, 'cutout_positions', visit=visit, detector=detector, instrument=instrument)
