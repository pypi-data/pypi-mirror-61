import os
from setuptools import setup

# ineedyou
# I need you, but you need me too.


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="ineedyou",
    version="0.0.2",
    description="I need you, but you need me too.",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3",
    keywords="circular",
    url="https://bitbucket.org/johannestaas/ineedyou",
    packages=['ineedyou'],
    package_dir={'ineedyou': 'ineedyou'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'youneedme',
    ],
    entry_points={
        'console_scripts': [
            'ineedyou=ineedyou:main',
        ],
    },
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    # package_data={
    #     'ineedyou': ['templates/*.html'],
    # },
    # include_package_data=True,
)
