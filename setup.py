import ast

from setuptools import setup, find_packages


with open('.project_metadata.py') as meta_file:
    project_metadata = ast.literal_eval(meta_file.read())


setup(
    name=project_metadata['name'],
    version=project_metadata['release'],
    author=project_metadata['author'],
    author_email=project_metadata['author_email'],
    description=project_metadata['description'],
    license=project_metadata['license'],
    install_requires=[
        'click',
        'logbook',
        'pendulum',
        'py-buzz',
        'redbaron',
        'toposort',
    ],
    extras_require={
        'dev': [
            'alembic',
            'flake8',
            'pytest',
        ],
    },
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ambix-flatten = ambix.tools:flatten',
            'ambix-prune = ambix.tools:prune',
        ],
    },
)
