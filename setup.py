from setuptools import setup


setup(
    name = 'pygres',
    packages = ['pygres'], 
    version = '1.4.0',
    description = 'Postgres simple connector',
    author = 'Rodrigo Gamba',
    author_email = 'gamba.lavin@gmail.com',
    url = 'https://github.com/rogamba/pygres', 
    download_url = 'https://github.com/rogamba/pygres/tarball/0.1', 
    keywords = ['postgres', 'psql', 'postgresql'],
    install_requires=[
        'psycopg2>=2.6.2',
    ],
    classifiers = [],
)
