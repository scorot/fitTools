"""
This script create a CSV file listing all the data available in
the fit header for each fit file inside a directory.
"""
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import os
import pandas as pd
import numpy as np

fits_array = []
for root, dirs, files in os.walk("/home/seb/Pictures/Astronomie/",
                                 topdown=False):
    for name in files:
        if os.path.join(root, name).endswith("fit"):
            # print(os.path.join(root, name))
            fits_file = os.path.join(root, name)
            d = dict(fits.getheader(fits_file))
            d.update({'FILENAME': name})
            d.update({'DIRNAME': root})
            fits_array.append(dict(d))

df = pd.DataFrame(fits_array)

# df[column_name].replace(
#   [old_value1, old_value2, old_value3],
#   [new_value1, new_value2, new_value3])
df['FILTER'] = df['FILTER'].replace(
    ['Bleu', 'Rouge', 'Vert', 'Filter 1', 'Filter 5', 'Filter 6', 'Filter 7'],
    ['Blue', 'Red', 'Green', 'Luminance', 'Ha', 'OIII', 'SII'])

# Traitement des noms d'objets manquants dans les entetes des fichiers fit
# on se sert du nom trouvé dans le dossier
df[['Col1', 'Object1']] = df['DIRNAME'].str.split('Astronomie/', expand=True)
df[['OBJECT_', 'Col2']] = df['Object1'].str.split('/', n=1, expand=True)

df['OBJECT'] = df['OBJECT'].str.strip()
# df["OBJECT"].fillna('empty', inplace = True)
df['OBJECT'] = np.where(df['OBJECT'].isnull(), df['OBJECT_'], df['OBJECT'])

# Suppresion des colonnes inutiles
df.drop(['Col1', 'Object1', 'Col2', 'OBJECT_'], axis=1, inplace=True)

df.to_csv('fits_library.csv', decimal=',')
