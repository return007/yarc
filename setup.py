import pathlib
from setuptools import setup

HERE   = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setup(
    name                          = 'yarc-server',
    version                       = '0.1.0',
    description                   = 'Yet Another Remote Control',
    long_description              = README,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/return007/yarc',
    author                        = 'return007',
    author_email                  = 'glalchandanig@gmail.com',
    packages                      = ['yarc'],
    include_package_data          = True,
    install_requires = [
        'pyautogui',
        'flask',
        'qrcode',
        'asyncio',
        'websockets'
    ],
    entry_points = {
        "console_scripts": [
            "yarc=yarc.launch:main",
        ]
    },
)
