from distutils.core import setup
import setuptools

with open('README.md') as readme_file: 
    #readme_file.readline()
    readme = readme_file.read()
exec(open('torchfit/version.py').read())


setup(
  name = 'torchfit',
  packages = setuptools.find_packages(),
  version = __version__,
  license='MIT',
  description = 'TorchFit is a simple, easy-to-use, and minimalistic training-helper for PyTorch',
  long_description = readme,
  long_description_content_type = 'text/markdown',
  author = 'Arun S. Maiya',
  author_email = 'arun@maiya.net',
  url = 'https://github.com/amaiya/torchfit',
  keywords = ['pytorch', 'deep learning', 'machine learning'],
  install_requires=[
          'numpy',
          'matplotlib >= 3.0.0',
          'torch-lr-finder',
          'ipython',
      ],
  classifiers=[  # Optional
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 4 - Beta',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',

    # Pick your license as you wish
    'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
