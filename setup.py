from setuptools import setup, find_packages

setup(
    # ... outros argumentos ...
    packages=find_packages(where='src', include=['anttsmartbot*']),
    package_dir={'': 'src'}
)