#!/usr/bin/env python

import argparse

from lsst.lsst_soda_service.put_values import put_values

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
        put_values(args.repository, args.visit, args.detector, args.instrument,
                   args.out_collection, ra=args.ra, dec=args.dec, size=args.size)
    elif not args.ra and not args.dec and not args.size and args.filename:
        put_values(args.repository, args.visit, args.detector, args.instrument,
                   args.out_collection, filename=args.filename)
    else:
        raise ValueError('Incorrect arguments either (--ra, --dec, --size)'
                         'or --filename, but not both.  Values are:\n'
                         f'--ra: {args.ra}\n'
                         f'--dec: {args.dec}\n'
                         f'--size: {args.size}\n'
                         f'--filename: {args.filename}')
