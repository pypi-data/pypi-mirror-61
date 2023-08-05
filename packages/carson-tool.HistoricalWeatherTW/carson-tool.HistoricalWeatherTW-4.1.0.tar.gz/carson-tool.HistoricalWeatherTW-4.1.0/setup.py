from distutils.core import setup
from pathlib import Path

VERSION_NUMBER = '4.1.0'
DOWNLOAD_VERSION = '4.1.0'
# LIST_SCRIPTS = [str(script_file) for script_file in Path('Scripts').glob('*.*')]
GITHUB_URL = 'https://github.com/CarsonSlovoka/HistoricalWeatherTW/tree/master'
SETUP_NAME = 'carson-tool.HistoricalWeatherTW'

with open('README.rst', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open('requirements.txt') as req_txt:
    LIST_REQUIRES = [line.strip() for line in req_txt if not line.startswith('#') and line.strip() != '']

setup(
    name=SETUP_NAME,
    version=VERSION_NUMBER,  # x.x.x.{dev, a, b, rc}
    packages=['Carson', 'Carson/Tool',
              'Carson/Tool/HistoricalWeatherTW', 'Carson/Tool/HistoricalWeatherTW/src'],
    package_data={'Carson/Tool/HistoricalWeatherTW': ['config/*.yaml', 'CSV/station.csv']},
    license="MIT",

    author='Carson',
    author_email='jackparadise520a@gmail.com',

    # scripts=LIST_SCRIPTS,  # xxx.bat

    install_requires=LIST_REQUIRES,

    url=GITHUB_URL,

    description='Bezier curve simulation (including reductions the dimension from 3 to 2)',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/x-rst',  # text/markdown
    keywords=['templates'],

    download_url=f'{GITHUB_URL}/tarball/v{DOWNLOAD_VERSION}',
    python_requires='>=3.6.2,',

    zip_safe=False,
    classifiers=[  # https://pypi.org/classifiers/
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Hydrology',
        'Intended Audience :: Science/Research',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: English',
        'Operating System :: Microsoft',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
