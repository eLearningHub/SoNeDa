from setuptools import setup

setup(
    name='sncli',
    version='0.0.0',
    py_modules=['sncli'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'sncli = sncli:main',
        ],
    },
)
