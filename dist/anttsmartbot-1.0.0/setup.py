from setuptools import setup, find_packages

setup(
    version="1.0.0",
    description="Robô que digita listas de passageiro na ANTT",
    author="Fernando Xavier",
    author_email="ferd@gmail.com",
    include_package_data=True,
    #data_files=[("bin", ["bin/ANTTSMARTBOT"])],
    #scripts=["bin/ANTTSMARTBOT"],
    packages=['anttsmartbot', 'models'],
    package_dir={'anttsmartbot': 'src/anttsmartbot', 'models': 'src/models'},
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