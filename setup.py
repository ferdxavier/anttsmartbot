from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
   def run(self):
       install.run(self)

setup(
    version="1.0.0",
    description="Robô que digita listas de passageiro na ANTT",
    author="Fernando Xavier",
    author_email="ferd@gmail.com",
    include_package_data=True,
    packages=['anttsmartbot', 'models'],
    package_dir={'anttsmartbot': 'src/anttsmartbot', 'models': 'src/anttsmartbot/models'},
    cmdclass={"install": CustomInstallCommand, },
)