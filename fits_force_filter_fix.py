from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import os

base_dir = "/home/astroberry/Pictures/Astronomy/Calibration/"
# fits_array = []
for root, dirs, files in os.walk(base_dir, topdown=False):
    for name in files:
        if os.path.join(root, name).endswith("fits"):
            # print(os.path.join(root, name))
            fits_file = os.path.join(root, name)
            d = dict(fits.getheader(fits_file))
            # print(d)
            if 'Rouge' in name:
                print("set Rouge for {}".format(name))
                fits.setval(fits_file, 'FILTER', value='Rouge')
            elif 'Vert' in name:
                print("set Vert for {}".format(name))
                fits.setval(fits_file, 'FILTER', value='Vert')
            elif 'Bleu' in name:
                print("set Bleu for {}".format(name))
                fits.setval(fits_file, 'FILTER', value='Bleu')
            elif 'Luminance2' in name:
                print("set Luminance2 for {}".format(name))
                fits.setval(fits_file, 'FILTER', value='Luminance2')
            elif '_Ha_' in name:
                print("set Ha for {}".format(name))
                fits.setval(fits_file, 'FILTER', value='Ha')
            elif '_OIII_' in name:
                print("set OIII for {}".format(name))
                fits.setval(fits_file, 'FILTER', value='OIII')
            elif '_SII_' in name:
                print("set SII for {}".format(name))
                fits.setval(fits_file, 'FILTER', value='SII')
            else:
                print("No changes in {}".format(name))
