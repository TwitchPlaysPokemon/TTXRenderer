
from setuptools import setup
setup(
    name="ttxrenderer",
    version="1.0",
    packages=["ttxrenderer"],
    install_requires=['pygame','pillow'],

    author="Phil Pemberton, TPP",
    description="Converts teletext pages to images",
    url="https://github.com/TwitchPlaysPokemon/ttxrenderer",
    package_data={'ttxrenderer': ['fonts/*']},
    include_package_data=True
)
