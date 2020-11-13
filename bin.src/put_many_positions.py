#!/user/bin/env python

import argparse
import numpy
from lsst.daf.butler import Butler, DatasetType


def main(repo, visit, detector, instrument, out_collection, ra=None, dec=None, size=None, filename=None):
    butler = Butler(repo, writeable=True, run=out_collection)
    # This doesn't strictly need to be done every time,
    # but doesn't seem to hurt if the
    # dataset type already exists
    position_dataset_type = DatasetType('cutout_positions', dimensions=['visit', 'detector', 'instrument'],
                                        universe=butler.registry.dimensions,
                                        storageClass='StructuredDataDict')
    butler.registry.registerDatasetType(position_dataset_type)

    if filename:
        poslist = numpy.genfromtxt(filename, dtype=None, delimiter=',')
    else:
        poslist = [(ra, dec, size), ]
    pos = dict(ident=[i for i in range(len(poslist))],
               ra=[float(el[0]) for el in poslist],
               dec=[float(el[1]) for el in poslist],
               size=[int(el[2]) for el in poslist])
    butler.put(pos, 'cutout_positions', visit=visit, detector=detector, instrument=instrument)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('repository', type=str,
                        help='Repository for outputs')
    parser.add_argument('visit', type=int,
                        help='Visit for the detector to cut out')
    parser.add_argument('detector', type=int,
                        help='Detector number for the detector to cut out')
    parser.add_argument('instrument', type=str,
                        help='Instrument detector to cut out comes from')
    parser.add_argument('out_collection', type=str,
                        help='Output collection name')
    parser.add_argument('--ra', type=float, default=None,
                        help='RA in degrees for the center of the cutout')
    parser.add_argument('--dec', type=float, default=None,
                        help='Declination in degrees for the center of the cutout')
    parser.add_argument('--size', type=int, default=None,
                        help='Size of the cutout')
    parser.add_argument('--filename', type=str, default=None,
                        help='Filename with RA, Dec pairs separatted by a comma. '
                             'Must not be set if --ra and --dec are set.')

    args = parser.parse_args()
    if args.ra and args.dec and args.size and not args.filename:
        main(args.repository, args.visit, args.detector, args.instrument,
             args.out_collection, ra=args.ra, dec=args.dec)
    elif not args.ra and not args.dec and not args.size and args.filename:
        main(args.repository, args.visit, args.detector, args.instrument,
             args.out_collection, filename=args.filename)
    else:
        raise ValueError('Incorrect arguments either (--ra, --dec, --size)'
                         'or --filename, but not both.  Values are:\n'
                         f'--ra: {args.ra}\n'
                         f'--dec: {args.dec}\n'
                         f'--size: {args.size}\n'
                         f'--filename: {args.filename}')
