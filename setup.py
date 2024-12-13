from setuptools import setup
from setuptools.command.install import install

setup(
    version="1.0.0",
    description="Robô que digita listas de passageiro na ANTT",
    author="Fernando Xavier",
    author_email="ferd@gmail.com",
    packages=['anttsmartbot'],
    package_dir={'anttsmartbot': 'src/anttsmartbot'},
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'anttsmartbot=src.anttsmartbot.anttsmartbot:init',
        ],
    },
)