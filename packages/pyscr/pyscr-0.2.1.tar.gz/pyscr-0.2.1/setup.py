from setuptools import setup

setup(name='pyscr',
      version='0.2.1',
      description='A Python library for RNAseq analysis',
      url='https://github.com/aneeshpanoli/pyscr',
      author='Aneesh aneeshpanoli',
      author_email='topanoli@gmail.com',
      license='MIT',
      install_requires=[
      'pyspark[sql]',
      ],
      packages=['pyscr'],
      zip_safe=False)
