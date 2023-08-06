import os
from setuptools import setup

install_requires = ['matplotlib', 'numpy', 'pandas','seaborn']

try:
    with open('README.md') as readme:
        long_description = readme.read()
except IOError:
    long_description = 'See https://pypi.python.org/pypi/wfmap'

distmeta = {}

for line in open(os.path.join(os.path.dirname(__file__),'wfmap', '__init__.py')):
    try:
        field, value = (x.strip() for x in line.split('='))
    except ValueError:
        continue
    if field == '__version_info__':
        value = value.strip('[]()')
        value = '.'.join(x.strip(' \'"') for x in value.split(','))
    else:
        value = value.strip('\'"')
    distmeta[field] = value
print(long_description)
setup(
    name='wfmap',
    version=distmeta['__version_info__'],
    description='Wafer heatmaps from Pandas DataFrame',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=distmeta['__author__'],
    author_email=distmeta['__contact__'],
    url=distmeta['__homepage__'],
    license='MIT License',
    platforms=['any'],
    packages=['wfmap'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',        
        'Topic :: Scientific/Engineering']
)
