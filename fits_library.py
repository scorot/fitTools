"""
This script create a CSV file listing all the data available in
the fit header for each fit file inside a directory.
"""
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import os
import os.path
import pandas as pd
import numpy as np
import click


def fits_library(dirname: str, csv: str) -> None:
    fits_array = []
    for root, dirs, files in os.walk(dirname,
                                     topdown=False):
        for name in files:
            if os.path.join(root, name).endswith("fit"):
                # print(os.path.join(root, name))
                fits_file = os.path.join(root, name)
                d = dict(fits.getheader(fits_file))
                d.update({'FILENAME': name})
                d.update({'DIRNAME': root})
                fits_array.append(dict(d))

    if len(fits_array) != 0:
        df = pd.DataFrame(fits_array)

        # df[column_name].replace(
        #   [old_value1, old_value2, old_value3],
        #   [new_value1, new_value2, new_value3])
        df['FILTER'] = df['FILTER'].replace(
            ['Bleu', 'Rouge', 'Vert', 'Filter 1', 'Filter 5', 'Filter 6', 'Filter 7'],
            ['Blue', 'Red', 'Green', 'Luminance', 'Ha', 'OIII', 'SII'])

        # Sometimes the name of the targeted objet is not present in the fit header
        # for this we find the name in the directory where the fit files reside.
        # The code below supposes that the subdirectories of dirname contains
        # objects names.
        basedir = os.path.split(os.path.normpath(dirname))[-1]
        df[['Col1', 'Object1']] = df['DIRNAME'].str.split(basedir, expand=True)
        df[['OBJECT_', 'Col2']] = df['Object1'].str.split('/', n=1, expand=True)

        df['OBJECT'] = df['OBJECT'].str.strip()
        # df["OBJECT"].fillna('empty', inplace = True)
        df['OBJECT'] = np.where(df['OBJECT'].isnull(), df['OBJECT_'], df['OBJECT'])

        # Delete useless columns
        df.drop(['Col1', 'Object1', 'Col2', 'OBJECT_'], axis=1, inplace=True)

        df.to_csv(csv, decimal='.')


@click.command()
@click.option('--dirname', default='./',
              help="The directory where fit files are located")
@click.option('--csv', default='fits_library.csv', help="The output csv file")
def main(dirname, csv):
    if not os.path.exists(dirname):
        raise click.BadParameter(
            f'Directory {dirname} does not exists.',
            param_hint=["--dirname"], )
    click.echo(f"Scanning directory {dirname}...")
    fits_library(dirname, csv)


if __name__ == '__main__':
    main()
