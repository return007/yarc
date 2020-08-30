import os
from setuptools import setup


README_PATH = os.path.join(os.path.dirname(__file__), 'README.md')
with open(README_PATH) as f:
    README_DATA = f.read()


# This call to setup() does all the work
setup(
    name                          = 'yarc-server',
    version                       = '0.1.0',
    description                   = 'Yet Another Remote Control',
    long_description              = README_DATA,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/return007/yarc',
    author                        = 'return007',
    author_email                  = 'glalchandanig@gmail.com',
    packages                      = ['yarc'],
    include_package_data          = True,
    python_requires               = '>=3.6',
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
