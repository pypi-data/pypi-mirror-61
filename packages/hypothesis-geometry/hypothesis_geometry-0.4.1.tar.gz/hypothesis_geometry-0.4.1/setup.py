from pathlib import Path

from setuptools import (find_packages,
                        setup)

import hypothesis_geometry

project_base_url = 'https://github.com/lycantropos/hypothesis_geometry/'

setup(name=hypothesis_geometry.__name__,
      packages=find_packages(exclude=('tests', 'tests.*')),
      version=hypothesis_geometry.__version__,
      description=hypothesis_geometry.__doc__,
      long_description=Path('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      classifiers=[
          'Framework :: Hypothesis',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],
      license='MIT License',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      python_requires='>=3.5',
      install_requires=Path('requirements.txt').read_text(encoding='utf-8'))
