

from setuptools import find_packages, setup

setup(
    name='pynancial',
    version='0.1.0',
    author='Aaron Schlegel',
    author_email='aaron@aaronschlegel.me',
    description='Financial engineering functions and algorithms',
    packages=find_packages(exclude=['docs', 'notebooks', 'tests*', '*.egg-info', 'data']),
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['numpy>=1.13.0', 'scipy>=1.1.0'],
    home_page='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
