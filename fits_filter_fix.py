from astropy.io import fits
import os
import click


def filter_fix(dirname: str) -> None:
    for root, dirs, files in os.walk(dirname, topdown=False):
        for name in files:
            if os.path.join(root, name).endswith("fits"):
                # print(os.path.join(root, name))
                fits_file = os.path.join(root, name)
                d = dict(fits.getheader(fits_file))
                # print(d)
                if "FILTER" not in d:
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


@click.command()
@click.option('--dirname', default='./',
              help="The directory where fit files are located")
def main(dirname):
    if not os.path.exists(dirname):
        raise click.BadParameter(
            f'Directory {dirname} does not exists.',
            param_hint=["--dirname"], )
    click.echo(f"Scanning directory {dirname}...")
    filter_fix(dirname)


if __name__ == '__main__':
    main()
