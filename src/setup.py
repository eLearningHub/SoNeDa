from setuptools import setup

setup(
    name='soneda',
    version='0.0.0',
    py_modules=['soneda'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'soneda = soneda:main',
        ],
    },
)
