import os

from setuptools import setup, find_packages, Command


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.egg-info')

setup(
    name='callgraph',
    version='0.0.1',
    description='Generate a call graph based on test executions.',
    long_description='CallGraph data collector for COMFORT',
    url='https://github.com/comfort-framework/comfort-callgraph/tree/master/comfort-callgraph',
    packages=find_packages(),
    author='Fabian Trautsch',
    author_email='trautsch@cs.uni-goettingen.de',
    license='Apache',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'nose',
        'pytest'
    ],
    entry_points={
        'nose.plugins.0.10': [
            'callgraph = callgraph.nose_plugin:CallGraphPlugin',
        ],
        'pytest11': [
            'callgraph = callgraph.pytest_plugin',
        ]
    },
    package_data={
        '': ["*.callgraph*", "*.tests*"],
    },
    cmdclass={
        'clean': CleanCommand,
    }
)
