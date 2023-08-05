from setuptools import find_packages, setup
setup(
    name='gen_names_magdalena',
    version='0.1.0',
    author='Magdalena Smoktunowicz',
    autho_email='magda.smoktunowicz@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    descripton='Generate random names with lenght magdalena',
    long_description='Generate random names with lenght magdalena',
    url='https://github.com/',
    install_requires=['names'],
    scripts=['gen_names_magdalena/gen_names_magdalena.py', 'bin/gen_name_magdalena.bat']
    
)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("gender", help="set male or female")
args = parser.parse_args()

name = names.get_full_name(gender=args.gender)

print(name, len(name)-1)

