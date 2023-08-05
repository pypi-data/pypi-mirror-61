# pylint: disable=line-too-long, invalid-name, missing-docstring

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="signal_transformation",
    version="1.1.5",
    author="Eugene Ilyushin",
    author_email="eugene.ilyushin@gmail.com",
    description="The package allows performing a transformation of an audio signal using TensorFlow or LibROSA",
    long_description="The package allows performing a transformation of an audio signal using TensorFlow or LibROSA",
    long_description_content_type="text/markdown",
    url="https://github.com/Ilyushin/signal-transformation",
    packages=['signal_transformation'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pydub',
        'pylint',
        'librosa',
        'ffmpeg',
        'webrtcvad'
    ],
)
