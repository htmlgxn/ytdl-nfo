from setuptools import setup, find_packages

setup(
    name='ytdl-nfo',
    version='1.0.0',
    author='Ben Chitty',
    author_email='htmlgxn@protonmail.com',
    description='A tool to download YouTube videos, along with thumbnails and .nfo metadata files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/htmlgxn/ytdl-nfo',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['yt-dlp'],
    entry_points={
        'console_scripts': [
            'ytdl-nfo=ytdl_nfo.ytdl_nfo:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
)
