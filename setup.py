from setuptools import find_namespace_packages, setup


with open('README.md') as fp:
    long_description = fp.read()


setup(
    name='gong',
    version='0.1.0',
    description='Gong Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jim Rosser',
    packages=find_namespace_packages(include=['gong', 'gong.*']),
    install_requires=[
        'requests',
    ],
    python_requires='>=3.10',
    classifiers=[
        'License :: MIT',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Topic :: Sales :: Productivity Software',
        'Topic :: Gong',
        'Topic :: Gong.io',
        'Typing :: Typed',
    ],
)
