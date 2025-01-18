from setuptools import setup

setup(
    version="1.0.0",
    description="Robô que digita listas de passageiro na ANTT",
    author="Fernando Xavier",
    author_email="ferd@gmail.com",
    packages=['anttsmartbot', 'anttsmartbot.models', 'anttsmartbot.tools'],
    package_dir={'anttsmartbot': 'src/anttsmartbot', 
                 'anttsmartbot.models': 'src/anttsmartbot/models', 
                 'anttsmartbot.tools': 'src/anttsmartbot/tools'}, 
    #data_files = [ ('src/anttsmartbot', ['src/anttsmartbot/json_pages_map.json']) ],
    include_package_data = True,
    install_requires=['openpyxl==3.1.5', 'pandas==2.2.3', 'selenium==4.27.1', 'pillow==11.1.0'],
    entry_points={
        'console_scripts': [
            'anttsmartbot=anttsmartbot.anttbot:init',
        ],
    },
)