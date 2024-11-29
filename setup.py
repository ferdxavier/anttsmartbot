from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        install.run(self)

setup(
    description="Robô que digita listas de passageiro na ANTT",
    #data_files=[("bin", ["bin/ANTTSMARTBOT"])],
    include_package_data=True,
    #scripts=["bin/ANTTSMARTBOT"],
    packages=find_packages(where='src', include=['anttsmartbot*']),
    package_dir={'': 'src'},
    cmdclass={
        "install": CustomInstallCommand,
    }, 
)

"""

name="anarci",
    version="1.3",
    description="Antibody Numbering and Receptor ClassIfication",
    author="James Dunbar",
    author_email="opig@stats.ox.ac.uk",
    url="http://opig.stats.ox.ac.uk/webapps/ANARCI",
    packages=["anarci"],
    package_dir={"anarci": "lib/python/anarci"},
    data_files=[("bin", ["bin/muscle", "bin/muscle_macOS", "bin/ANARCI"])],
    include_package_data=True,
    scripts=["bin/ANARCI"],
    cmdclass={
        "install": CustomInstallCommand,
    }, 
    
    """