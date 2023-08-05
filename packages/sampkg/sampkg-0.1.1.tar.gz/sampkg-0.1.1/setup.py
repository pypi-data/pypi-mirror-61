from setuptools import setup, find_packages

__version__ = '0.1.1'
url = 'https://github.com/pgtgrly/'

install_requires = [
    'numpy',
]
setup_requires = ['pytest-runner']
tests_require = ['pytest', 'pytest-cov', 'mock']

setup(
    name='sampkg',
    version=__version__,
    description='A sample Python package',
    author='Pranav Garg',
    author_email='pranavgarg@gmail.com',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, __version__),
    keywords=[
        'python', 'example'
    ],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    packages=find_packages())
