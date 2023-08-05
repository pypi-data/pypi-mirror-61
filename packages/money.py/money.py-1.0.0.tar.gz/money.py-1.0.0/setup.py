from setuptools import setup

long_description = open('README.md').read()


def find_version(*file_paths):
    """
    Find package version in file.
    """
    import re
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    content = open(os.path.join(here, *file_paths)).read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


setup(name='money.py',
      version=find_version('moneypy', '__init__.py'),
      description='money.py is a library to handle money.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/cryptgar/money.py',
      author='Edgar Luque',
      author_email='blog@anonim.cat',
      license='MIT',
      packages=['moneypy'],
      zip_safe=False,
      keywords=['money'],
      test_suite="tests",
      tests_require=["pytest>=5.0"],
      python_requires='>=3.6',
      classifiers=[
          # How mature is this project? Common values are
          #   1 - Planning
          #   2 - Pre-Alpha
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 2 - Pre-Alpha',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Utilities',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ])
