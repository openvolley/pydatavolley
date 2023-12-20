from setuptools import setup, find_packages

setup(
    name='pydatavolley',
    description='A python set of code for reading volleyball scouting files in DataVolley format (*.dvw)',
    url='https://github.com/openvolley/pydatavolley',
    author='Tyler Widdison',
    license='MIT',
    version='2.2.6',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.3',
        'pandas>=1.5.0',
    ],
    entry_points={
        'console_scripts': [
            'pydatavolley=datavolley.read_dv:main',
        ],
    },
)
