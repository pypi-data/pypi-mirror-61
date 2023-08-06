from setuptools import setup, find_packages

dependencies = ['requests']
test_dependencies = ['nose']

setup(
    name="pyfinnotech",
    version='0.2.0',
    author="mahdi13",
    tests_require=test_dependencies,
    extras_require={'test': test_dependencies},
    install_requires=dependencies,
    packages=find_packages(),
    test_suite="pyfinnotech.tests"
)
