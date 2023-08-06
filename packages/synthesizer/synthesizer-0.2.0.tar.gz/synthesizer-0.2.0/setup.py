from setuptools import setup, find_packages
version = '0.2.0'

setup(
    name='synthesizer',
    version=version,
    description="A simple virtual analog synthesizer.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Multimedia :: Sound/Audio :: MIDI",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        ],
    keywords='analog synthesizer',
    author='Yuma Mihira',
    author_email='info@yurax2.com',
    url='https://github.com/yuma-m/synthesizer',
    license='GPLv3',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    zip_safe=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    test_suite='nose.collector',
    install_requires=[
        'enum34>=1.1.6',
        "numpy>=1.13.3",
        # TODO: commented out to build document on ReadTheDocs
        # 'PyAudio>=0.2.11',
        'scipy>=0.19.1',
    ],
)
