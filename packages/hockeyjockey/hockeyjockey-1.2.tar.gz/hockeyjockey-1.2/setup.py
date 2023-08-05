from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hockeyjockey',
    version='1.2',
    packages=['hockeyjockey', 'hockeyjockey.api', 'hockeyjockey.automation', 'hockeyjockey.exceptions',
              'hockeyjockey.models', 'hockeyjockey.utilities'],
    install_requires=['decorest', 'ansicolors', 'mysql-connector-python', 'menyou'],
    url='https://gitlab.com/ricoflow/hockeyjockey',
    license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    author='Randall Speake',
    author_email='ranspeake@gmail.com',
    description='A menu-driven console-based application for analyzing NHL hockey games.',
    long_description_content_type='text/markdown',
    long_description=long_description,
)
